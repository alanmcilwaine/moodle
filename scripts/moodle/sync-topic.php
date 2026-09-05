<?php
// Replace one module's questions in a course's question bank and rebuild its
// quiz, atomically: every check runs before any write, and the delete, import,
// slot rebuild, orphan purge, and grade recompute run in one transaction.
// Refuses to run while the quiz has attempts. After committing, validates the
// imported questions through Jobe.
// Usage: php sync-topic.php <file.xml> <manifest.json>
// Runs inside the moodle container.

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->libdir . '/clilib.php');
require_once($CFG->dirroot . '/question/format.php');
require_once($CFG->dirroot . '/question/format/xml/format.php');
require_once($CFG->dirroot . '/mod/quiz/locallib.php');
require_once($CFG->libdir . '/questionlib.php');

if (count($argv) !== 3) {
    cli_error("Usage: php sync-topic.php <file.xml> <manifest.json>");
}
[, $xmlfile, $manifestpath] = $argv;
if (!is_readable($xmlfile)) {
    cli_error("Cannot read $xmlfile");
}

\core\session\manager::set_user(get_admin());

// --- Preflight: every failure here happens before any database mutation. ---

$manifest = json_decode(file_get_contents($manifestpath));
if ($manifest === null) {
    cli_error("The manifest at {$manifestpath} is not valid JSON");
}
$basename = basename($xmlfile);
$module = null;
foreach ($manifest->modules as $candidate) {
    if ($candidate->file === $basename) {
        $module = $candidate;
        break;
    }
}
if ($module === null) {
    cli_error("The manifest at {$manifestpath} lists no module with file {$basename}");
}

$xml = simplexml_load_file($xmlfile);
if ($xml === false) {
    cli_error("{$basename} is not valid XML");
}
$names = [];
foreach ($xml->question as $qx) {
    if ((string)$qx['type'] !== 'coderunner') {
        continue;
    }
    $names[] = trim((string)$qx->name->text);
}
if (count($names) !== (int)$module->questions) {
    cli_error("{$basename} declares {$module->questions} questions but contains " . count($names));
}
$seen = [];
foreach ($names as $name) {
    if (!preg_match('/^WAT (\d+)\.(\d+):/', $name, $m)) {
        cli_error("{$basename}: question name '{$name}' does not match 'WAT <topic>.<n>: <title>'");
    }
    $topic = (int)$m[1];
    if ($topic < $module->from || $topic > $module->to) {
        cli_error("{$basename}: question '{$name}' is topic {$topic}, outside the module range [{$module->from}, {$module->to}]");
    }
    if (isset($seen[$name])) {
        cli_error("{$basename}: question name '{$name}' appears more than once");
    }
    $seen[$name] = true;
}

$course = $DB->get_record('course', ['shortname' => $manifest->course->shortname]);
if (!$course) {
    cli_error("No course with shortname {$manifest->course->shortname}; run the course setup first");
}

$quizzes = $DB->get_records('quiz', ['course' => $course->id, 'name' => $module->title]);
if (count($quizzes) !== 1) {
    cli_error("Found " . count($quizzes) . " quizzes named '{$module->title}' in {$course->shortname}; expected exactly one");
}
$quiz = reset($quizzes);

if ($DB->record_exists('quiz_attempts', ['quiz' => $quiz->id])) {
    cli_error("Quiz '{$quiz->name}' has attempts; nothing was changed. "
        . "Delete the attempt in the Moodle UI, then retry.");
}

$cm = \core_question\local\bank\question_bank_helper::get_default_open_instance_system_type($course, true);
$context = context_module::instance($cm->id);
$defaultcategory = question_make_default_categories([$context]);

// --- Mutation: one transaction, so a failure leaves the bank untouched. ---

$transaction = $DB->start_delegated_transaction();
try {
    // Replace, never duplicate: a question still used by a quiz slot is hidden
    // rather than deleted, which is Moodle's own rule inside
    // question_delete_question(). The orphans it leaves are purged below.
    foreach ($names as $name) {
        $ids = $DB->get_fieldset_sql(
            "SELECT q.id FROM {question} q
               JOIN {question_versions} qv ON qv.questionid = q.id
               JOIN {question_bank_entries} qbe ON qbe.id = qv.questionbankentryid
              WHERE qbe.questioncategoryid = ? AND q.name = ?",
            [$defaultcategory->id, $name]
        );
        foreach ($ids as $id) {
            question_delete_question($id);
        }
    }

    if (getenv('MOODLE_SYNC_TEST_FAIL_AFTER_DELETE') === '1') {
        throw new \Exception('Injected failure after deleting the old questions');
    }

    $qformat = new qformat_xml();
    $qformat->setContexts([$context]);
    $qformat->setCourse($course);
    $qformat->setCategory($defaultcategory);
    $qformat->setFilename($xmlfile);
    $qformat->setRealfilename($basename);
    $qformat->setMatchgrades('error');
    $qformat->setCatfromfile(0);
    $qformat->setContextfromfile(0);
    $qformat->setStoponerror(1);
    $qformat->set_display_progress(false);

    if (!$qformat->importpreprocess() || !$qformat->importprocess()) {
        throw new \Exception("Import failed for {$basename}");
    }
    $qformat->importpostprocess();

    // Compute the replacement slot set before any slot is touched, so a bad
    // import aborts with the old quiz still intact inside the transaction.
    $current = $DB->get_records_sql("
        SELECT q.id, q.name
          FROM {question} q
          JOIN {question_versions} qv ON qv.questionid = q.id
          JOIN {question_bank_entries} qbe ON qbe.id = qv.questionbankentryid
         WHERE qbe.questioncategoryid = :cat
           AND qv.status <> 'hidden'
           AND qv.version = (SELECT MAX(qv2.version) FROM {question_versions} qv2
                               WHERE qv2.questionbankentryid = qbe.id)
      ORDER BY q.name", ['cat' => $defaultcategory->id]);

    $slotset = [];
    foreach ($current as $q) {
        if (!preg_match('/^WAT (\d+)\.(\d+):/', $q->name, $m)) {
            continue;
        }
        $topic = (int)$m[1];
        if ($topic < $module->from || $topic > $module->to) {
            continue;
        }
        $slotset[$q->name] = $q->id;
    }
    if (count($slotset) !== (int)$module->questions) {
        throw new \Exception("The bank holds " . count($slotset) . " current questions for {$module->title}"
            . " (WAT {$module->from}-{$module->to}), expected {$module->questions}; slots left untouched");
    }
    foreach ($names as $name) {
        if (!isset($slotset[$name])) {
            throw new \Exception("Imported question '{$name}' is missing from the bank; slots left untouched");
        }
    }

    $existing = $DB->get_records_sql("
        SELECT qs.id AS slotid, qr.id AS refid
          FROM {quiz_slots} qs
          JOIN {question_references} qr
            ON qr.itemid = qs.id AND qr.component = 'mod_quiz' AND qr.questionarea = 'slot'
         WHERE qs.quizid = :quizid", ['quizid' => $quiz->id]);
    foreach ($existing as $slot) {
        $DB->delete_records('question_references', ['id' => $slot->refid]);
    }
    $DB->delete_records('quiz_slots', ['quizid' => $quiz->id]);
    foreach ($slotset as $questionid) {
        quiz_add_quiz_question($questionid, $quiz);
    }

    // Replaced questions still referenced by a slot were hidden, not deleted;
    // the slot rebuild just dropped those references. Purge the orphans, or
    // bulk validation keeps testing them and reports double the real count.
    $orphans = $DB->get_records_sql("
        SELECT q.id, q.name
          FROM {question} q
          JOIN {question_versions} qv ON qv.questionid = q.id
          JOIN {question_bank_entries} qbe ON qbe.id = qv.questionbankentryid
         WHERE qbe.questioncategoryid = :cat
           AND qv.status = 'hidden'
           AND NOT EXISTS (
                 SELECT 1 FROM {question_references} qr
                  WHERE qr.questionbankentryid = qbe.id
               )
    ", ['cat' => $defaultcategory->id]);
    foreach ($orphans as $q) {
        question_delete_question($q->id);
    }

    \mod_quiz\quiz_settings::create($quiz->id)->get_grade_calculator()->recompute_quiz_sumgrades();

    $transaction->allow_commit();
} catch (\Throwable $e) {
    // moodle_transaction::rollback() accepts \Throwable but rethrows it, so
    // swallow the rethrow and let cli_error print one clean line.
    try {
        $transaction->rollback($e);
    } catch (\Throwable $ignored) {
    }
    cli_error("Sync failed and was rolled back; nothing was changed. " . $e->getMessage());
}

// Validate only the imported topic. A failure elsewhere in the course must not
// turn a successful topic replacement into a failed command.
$tester = new \qtype_coderunner\bulk_tester($context, null, -1, 0, 1, 1, 0);
ob_start();
$tester->run_tests(array_values($slotset));
ob_end_clean();

$fails = count($tester->failedtestdetails);
$missing = count($tester->missinganswerdetails);
echo "course: {$course->shortname}\n";
echo "quiz: {$quiz->name}\n";
echo "replaced: " . count($names) . " questions\n";
echo "slots: " . count($slotset) . "\n";
echo "validation passes: {$tester->numpasses}\n";
echo "validation fails: {$fails}\n";
echo "missing answers: {$missing}\n";
foreach ($tester->failedquestionids as $questionid) {
    $question = question_bank::load_question($questionid);
    echo "FAIL: {$question->name} (V{$question->version}, id {$question->id})\n";
    echo "  Inspect: php /tmp/diagnose-question.php {$question->id}\n";
}
foreach ($tester->missinganswerdetails as $detail) {
    echo 'MISSING: ' . trim(html_entity_decode(strip_tags($detail))) . "\n";
}
if ($fails + $missing > 0) {
    cli_error("The sync committed, but the imported topic failed validation.");
}
