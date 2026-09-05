<?php
// Print stable course, quiz, question, and slot state for rehearsal comparisons.
// Usage: php course-state.php <course shortname>

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->libdir . '/clilib.php');
require_once($CFG->libdir . '/questionlib.php');

if (count($argv) !== 2) {
    cli_error('Usage: php course-state.php <course shortname>');
}
[, $shortname] = $argv;

$course = $DB->get_record('course', ['shortname' => $shortname], '*', MUST_EXIST);
$cm = \core_question\local\bank\question_bank_helper::get_default_open_instance_system_type($course, true);
$context = context_module::instance($cm->id);
$categories = $DB->get_records('question_categories', ['contextid' => $context->id], '', 'id');
$categoryids = array_keys($categories);

$questions = [];
if ($categoryids) {
    [$insql, $params] = $DB->get_in_or_equal($categoryids);
    $records = $DB->get_records_sql("
        SELECT q.id, q.name
          FROM {question} q
          JOIN {question_versions} qv ON qv.questionid = q.id
          JOIN {question_bank_entries} qbe ON qbe.id = qv.questionbankentryid
         WHERE qbe.questioncategoryid {$insql}
           AND qv.status <> 'hidden'
           AND qv.version = (SELECT MAX(qv2.version) FROM {question_versions} qv2
                               WHERE qv2.questionbankentryid = qbe.id)
      ORDER BY q.name", $params);
    foreach ($records as $record) {
        $questions[$record->name] = (int)$record->id;
    }
}

$quizzes = [];
foreach ($DB->get_records('quiz', ['course' => $course->id], 'name') as $quiz) {
    $quizzes[$quiz->name] = [
        'id' => (int)$quiz->id,
        'slots' => $DB->count_records('quiz_slots', ['quizid' => $quiz->id]),
    ];
}

echo json_encode([
    'course_id' => (int)$course->id,
    'question_bank_id' => (int)$cm->id,
    'questions' => $questions,
    'quizzes' => $quizzes,
], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
