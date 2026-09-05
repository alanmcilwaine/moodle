<?php
// Run stored sample answers through CodeRunner and print the raw grading result.
// Usage: php diagnose-question.php [--answer-file=<path>] <question id> [<question id> ...]

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->libdir . '/clilib.php');
require_once($CFG->libdir . '/questionlib.php');

$questionids = [];
$answerfile = null;
foreach (array_slice($argv, 1) as $arg) {
    if (str_starts_with($arg, '--answer-file=')) {
        if ($answerfile !== null) {
            cli_error('Specify --answer-file once.');
        }
        $answerfile = substr($arg, strlen('--answer-file='));
    } else {
        $questionids[] = $arg;
    }
}
if (count($questionids) === 0) {
    cli_error('Usage: php diagnose-question.php [--answer-file=<path>] <question id> [<question id> ...]');
}
if ($answerfile !== null && !is_readable($answerfile)) {
    cli_error("Cannot read the answer file at {$answerfile}");
}

\core\session\manager::set_user(get_admin());

foreach ($questionids as $rawid) {
    $questionid = clean_param($rawid, PARAM_INT);
    if ((string)$questionid !== $rawid || $questionid <= 0) {
        cli_error("Invalid question id: {$rawid}");
    }

    $question = question_bank::load_question($questionid);
    $question->start_attempt(null);
    $response = $question->get_correct_response();
    if ($answerfile !== null) {
        $response['answer'] = file_get_contents($answerfile);
    }
    [$fraction, $state, $cache] = $question->grade_response($response, false, false, false);
    $outcome = unserialize($cache['_testoutcome']);

    echo "question {$question->id}: {$question->name}\n";
    echo "type: {$question->coderunnertype}\n";
    echo "fraction: {$fraction}\n";
    echo "outcome status: {$outcome->status}\n";
    if ($outcome->errormessage !== '') {
        echo "outcome error: {$outcome->errormessage}\n";
    }
    foreach ($outcome->testresults as $index => $result) {
        $number = $index + 1;
        echo "test {$number}: " . ($result->iscorrect ? 'PASS' : 'FAIL') . "\n";
        echo 'expected: ' . json_encode($result->expected) . "\n";
        echo 'got: ' . json_encode($result->got) . "\n";
    }
    echo "---\n";
}
