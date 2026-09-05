<?php
// Create or remove an administrator preview attempt for an import-guard test.
// Usage: php rehearsal-attempt.php <create|remove> <course shortname> <quiz name>

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->libdir . '/clilib.php');
require_once($CFG->dirroot . '/mod/quiz/locallib.php');

if (count($argv) !== 4 || !in_array($argv[1], ['create', 'remove'], true)) {
    cli_error('Usage: php rehearsal-attempt.php <create|remove> <course shortname> <quiz name>');
}
[, $action, $shortname, $quizname] = $argv;

$admin = get_admin();
\core\session\manager::set_user($admin);
$course = $DB->get_record('course', ['shortname' => $shortname], '*', MUST_EXIST);
$quiz = $DB->get_record('quiz', ['course' => $course->id, 'name' => $quizname], '*', MUST_EXIST);

if ($action === 'create') {
    $quizsettings = \mod_quiz\quiz_settings::create($quiz->id, $admin->id);
    $attempt = quiz_prepare_and_start_new_attempt($quizsettings, 1, false);
    echo "Created preview attempt {$attempt->id}\n";
} else {
    $attempts = $DB->get_records('quiz_attempts', [
        'quiz' => $quiz->id,
        'userid' => $admin->id,
        'preview' => 1,
    ]);
    foreach ($attempts as $attempt) {
        quiz_delete_attempt($attempt, $quiz);
    }
    echo 'Removed ' . count($attempts) . " preview attempt(s)\n";
}
