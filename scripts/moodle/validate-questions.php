<?php
// CLI validation of every CodeRunner question in a course's default question bank:
// runs each question's sample answer against its test cases via Jobe.
// Usage: php validate-questions.php <course id or shortname> [<question id> ...]

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->libdir . '/clilib.php');
require_once($CFG->libdir . '/questionlib.php');

if (count($argv) < 2) {
    cli_error("Usage: php validate-questions.php <course id or shortname> [<question id> ...]");
}
[, $coursekey] = $argv;
$questionids = [];
foreach (array_slice($argv, 2) as $rawid) {
    $questionid = clean_param($rawid, PARAM_INT);
    if ((string)$questionid !== $rawid || $questionid <= 0) {
        cli_error("Invalid question id: {$rawid}");
    }
    $questionids[] = $questionid;
}

\core\session\manager::set_user(get_admin());

$course = ctype_digit($coursekey)
    ? get_course((int)$coursekey)
    : $DB->get_record('course', ['shortname' => $coursekey], '*', MUST_EXIST);
$cm = \core_question\local\bank\question_bank_helper::get_default_open_instance_system_type($course, true);
$context = context_module::instance($cm->id);

// repeatrandomonly=0 tests every question. clearcachefirst=1 and usecache=0 make
// the run genuinely fresh, so a stale grading cache cannot report a false failure.
$tester = new \qtype_coderunner\bulk_tester($context, null, -1, 0, 1, 1, 0);
ob_start();
$tester->run_tests($questionids);
ob_end_clean();

echo "passes: {$tester->numpasses}\n";
echo "fails: " . count($tester->failedtestdetails) . "\n";
echo "missing answers: " . count($tester->missinganswerdetails) . "\n";
foreach ($tester->failedquestionids as $questionid) {
    $question = question_bank::load_question($questionid);
    echo "FAIL: {$question->name} (V{$question->version}, id {$question->id})\n";
    echo "  Inspect: php /tmp/diagnose-question.php {$question->id}\n";
}
foreach ($tester->missinganswerdetails as $detail) {
    echo 'MISSING: ' . trim(html_entity_decode(strip_tags($detail))) . "\n";
}
exit(count($tester->failedtestdetails) + count($tester->missinganswerdetails) > 0 ? 1 : 0);
