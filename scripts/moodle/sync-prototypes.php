<?php
// Update a course's existing CodeRunner prototypes from its manifest.
// Unchanged prototypes are left alone. Changed prototypes become a new Moodle
// question version, preserving the bank entry used by the course.
// Usage: php sync-prototypes.php <manifest.json> <xml directory>

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->libdir . '/clilib.php');
require_once($CFG->libdir . '/questionlib.php');
require_once($CFG->dirroot . '/question/format.php');
require_once($CFG->dirroot . '/question/format/xml/format.php');

if (count($argv) !== 3) {
    cli_error('Usage: php sync-prototypes.php <manifest.json> <xml directory>');
}
[, $manifestpath, $xmldir] = $argv;

if (!is_readable($manifestpath)) {
    cli_error("Cannot read the manifest at {$manifestpath}");
}
$manifest = json_decode(file_get_contents($manifestpath));
if ($manifest === null) {
    cli_error("The manifest at {$manifestpath} is not valid JSON");
}

\core\session\manager::set_user(get_admin());

$course = $DB->get_record('course', ['shortname' => $manifest->course->shortname], '*', MUST_EXIST);
$cm = \core_question\local\bank\question_bank_helper::get_default_open_instance_system_type($course, true);
$context = context_module::instance($cm->id);
$forceupdate = getenv('MOODLE_SYNC_PROTOTYPE_TEST_FORCE_UPDATE') === '1';

foreach ($manifest->prototypes ?? [] as $file) {
    $path = rtrim($xmldir, '/') . '/' . $file;
    if (!is_readable($path)) {
        cli_error("Cannot read the prototype at {$path}");
    }

    $qformat = new qformat_xml();
    $qformat->setContexts([$context]);
    $qformat->setCourse($course);
    $qformat->setStoponerror(1);
    $qformat->set_display_progress(false);
    $questions = $qformat->readquestions(file($path));
    if (!is_array($questions) || count($questions) !== 1) {
        cli_error("Expected exactly one prototype question in {$path}");
    }
    $desired = reset($questions);
    if ($desired->qtype !== 'coderunner' || empty($desired->prototypetype) || empty($desired->coderunnertype)) {
        cli_error("The question in {$path} is not a named CodeRunner prototype");
    }

    $records = $DB->get_records_sql("\n        SELECT q.id\n          FROM {question} q\n          JOIN {question_versions} qv ON qv.questionid = q.id\n          JOIN {question_bank_entries} qbe ON qbe.id = qv.questionbankentryid\n          JOIN {question_categories} qc ON qc.id = qbe.questioncategoryid\n          JOIN {question_coderunner_options} qco ON qco.questionid = q.id\n         WHERE qc.contextid = :contextid\n           AND qco.coderunnertype = :coderunnertype\n           AND qco.prototypetype != 0\n           AND qv.version = (SELECT MAX(qv2.version)\n                               FROM {question_versions} qv2\n                              WHERE qv2.questionbankentryid = qbe.id)", [
        'contextid' => $context->id,
        'coderunnertype' => $desired->coderunnertype,
    ]);
    if (count($records) !== 1) {
        cli_error("Expected one current {$desired->coderunnertype} prototype, found " . count($records));
    }

    $currentid = (int)reset($records)->id;
    $currentoptions = $DB->get_record('question_coderunner_options', ['questionid' => $currentid], '*', MUST_EXIST);
    if (!$forceupdate && $currentoptions->template === $desired->template) {
        echo "Prototype {$desired->coderunnertype} is current.\n";
        continue;
    }

    $current = $DB->get_record('question', ['id' => $currentid], '*', MUST_EXIST);
    $bankentry = get_question_bank_entry($currentid);
    $desired->category = $bankentry->questioncategoryid . ',' . $context->id;
    $desired->idnumber = $bankentry->idnumber;
    $desired->status = \core_question\local\bank\question_version_status::QUESTION_STATUS_READY;
    $desired->questiontext = [
        'text' => $desired->questiontext,
        'format' => $desired->questiontextformat,
        'itemid' => 0,
    ];
    $desired->generalfeedback = [
        'text' => $desired->generalfeedback,
        'format' => $desired->generalfeedbackformat,
        'itemid' => 0,
    ];

    $saved = question_bank::get_qtype('coderunner')->save_question($current, $desired);
    question_bank::notify_question_edited($saved->id);
    echo "Updated prototype {$desired->coderunnertype} from question {$currentid} to {$saved->id}.\n";
}
