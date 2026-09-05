<?php
// Build a whole course from a manifest: create it, import every module, add one
// quiz per module, and tidy the empty sections Moodle creates by default.
// Idempotent. A course that already exists is left alone.
//
// Usage: php bootstrap-course.php <manifest.json> <xml directory>

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->libdir . '/clilib.php');
require_once($CFG->dirroot . '/course/lib.php');
require_once($CFG->dirroot . '/question/format.php');
require_once($CFG->dirroot . '/question/format/xml/format.php');
require_once($CFG->dirroot . '/mod/quiz/locallib.php');
require_once($CFG->libdir . '/questionlib.php');

if (count($argv) !== 3) {
    cli_error("Usage: php bootstrap-course.php <manifest.json> <xml directory>");
}
[, $manifestpath, $xmldir] = $argv;

if (!is_readable($manifestpath)) {
    cli_error("Cannot read the manifest at {$manifestpath}");
}
$manifest = json_decode(file_get_contents($manifestpath));
if ($manifest === null) {
    cli_error("The manifest at {$manifestpath} is not valid JSON");
}
$failafterimports = getenv('MOODLE_BOOTSTRAP_TEST_FAIL_AFTER_IMPORTS');
if ($failafterimports !== false && (!ctype_digit($failafterimports) || (int)$failafterimports < 1)) {
    cli_error('MOODLE_BOOTSTRAP_TEST_FAIL_AFTER_IMPORTS must be a positive integer');
}

\core\session\manager::set_user(get_admin());

$shortname = $manifest->course->shortname;
$existing = $DB->get_record('course', ['shortname' => $shortname]);
if ($existing) {
    $url = new moodle_url('/course/view.php', ['id' => $existing->id]);
    echo "Course {$shortname} already exists.\n";
    echo "Open {$url}\n";
    exit(0);
}

// Fail before any database mutation if a file the manifest needs is missing.
$files = $manifest->prototypes ?? [];
foreach ($manifest->modules as $module) {
    $files[] = $module->file;
}
foreach ($files as $file) {
    $path = rtrim($xmldir, '/') . '/' . $file;
    if (!is_readable($path)) {
        cli_error("Cannot read the question file at {$path}");
    }
}

$course = null;
try {
    // 1. Create the course.
    $category = $DB->get_field_sql("SELECT MIN(id) FROM {course_categories}");
    $course = create_course((object)[
        'fullname' => $manifest->course->fullname,
        'shortname' => $shortname,
        'category' => $category,
        'format' => 'topics',
    ]);
    echo "Created course {$course->shortname} (id {$course->id})\n";

    // 2. Import every module into the course question bank.
    $cm = \core_question\local\bank\question_bank_helper::get_default_open_instance_system_type($course, true);
    $context = context_module::instance($cm->id);
    $defaultcategory = question_make_default_categories([$context]);

    $import = function (string $file) use ($xmldir, $context, $course, $defaultcategory) {
        $path = rtrim($xmldir, '/') . '/' . $file;

        $qformat = new qformat_xml();
        $qformat->setContexts([$context]);
        $qformat->setCourse($course);
        $qformat->setCategory($defaultcategory);
        $qformat->setFilename($path);
        $qformat->setRealfilename($file);
        $qformat->setMatchgrades('error');
        $qformat->setCatfromfile(0);
        $qformat->setContextfromfile(0);
        $qformat->setStoponerror(1);
        $qformat->set_display_progress(false);

        if (!$qformat->importpreprocess() || !$qformat->importprocess()) {
            throw new \Exception("Import failed for {$file}");
        }
        $qformat->importpostprocess();
        echo "Imported {$file}\n";
    };

    // Question-type prototypes must exist in the bank before any question of that
    // type is imported, so the manifest lists them separately and they go first.
    foreach ($manifest->prototypes ?? [] as $file) {
        $import($file);
    }
    $importedmodules = 0;
    foreach ($manifest->modules as $module) {
        $import($module->file);
        $importedmodules++;
        if ($failafterimports !== false && $importedmodules === (int)$failafterimports) {
            throw new \Exception("Injected failure after importing {$importedmodules} module(s)");
        }
    }

    // 3. Add one quiz per module and fill it with that module's questions.
    $questions = $DB->get_records_sql("
        SELECT q.id, q.name
          FROM {question} q
          JOIN {question_versions} qv ON qv.questionid = q.id
          JOIN {question_bank_entries} qbe ON qbe.id = qv.questionbankentryid
         WHERE qbe.questioncategoryid = :cat
      ORDER BY q.name", ['cat' => $defaultcategory->id]);

    foreach ($manifest->modules as $module) {
        $quiz = create_module((object)[
            'modulename' => 'quiz',
            'course' => $course->id,
            'section' => 1,
            'name' => $module->title,
            'visible' => 1,
            'introeditor' => ['text' => '', 'format' => FORMAT_HTML, 'itemid' => 0],
            // quiz_process_options copies quizpassword onto the NOT NULL password
            // column, so a programmatic call has to supply the form field name.
            'quizpassword' => '',
            'subnet' => '',
            // CodeRunner renders its results table (Expected/Got, stdout) as the
            // question's specific feedback. Without these flags the Check button
            // grades silently and the student never sees their output.
            'specificfeedbackduring' => 1,
            'specificfeedbackimmediately' => 1,
            'specificfeedbackopen' => 1,
            'specificfeedbackclosed' => 1,
        ]);

        $added = 0;
        foreach ($questions as $q) {
            if (!preg_match('/^WAT\s+(\d+)/', $q->name, $m)) {
                continue;
            }
            $number = (int)$m[1];
            if ($number < $module->from || $number > $module->to) {
                continue;
            }
            quiz_add_quiz_question($q->id, $DB->get_record('quiz', ['id' => $quiz->instance]));
            $added++;
        }
        \mod_quiz\quiz_settings::create($quiz->instance)->get_grade_calculator()->recompute_quiz_sumgrades();
        echo "Built quiz {$module->title} with {$added} questions\n";
    }

    // 4. Remove the empty sections Moodle creates by default and name the one in use.
    $course = get_course($course->id);
    $modinfo = get_fast_modinfo($course);
    $empty = [];
    foreach ($modinfo->get_section_info_all() as $section) {
        if ($section->section == 0) {
            continue;
        }
        if (empty($modinfo->sections[$section->section])) {
            $empty[] = $section->section;
        }
    }
    rsort($empty);
    foreach ($empty as $number) {
        course_delete_section($course, $number, true);
    }

    $modinfo = get_fast_modinfo(get_course($course->id));
    foreach ($modinfo->get_section_info_all() as $section) {
        if ($section->section == 0) {
            continue;
        }
        course_update_section($course, $section, (object)[
            'id' => $section->id,
            'name' => $manifest->course->section,
        ]);
    }

    $url = new moodle_url('/course/view.php', ['id' => $course->id]);
    echo "Done. Open {$url}\n";
} catch (\Throwable $e) {
    if ($course !== null) {
        // Remove the partial course so the shortname check does not skip a retry.
        delete_course($course, false);
        cli_error($e->getMessage() . " The partial course was removed; setup can be rerun.");
    }
    cli_error($e->getMessage());
}
