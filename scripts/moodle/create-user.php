<?php
// Create a learner account and enrol it in a course as a student.
// Usage: php create-user.php <username> <password> <courseid> [firstname] [lastname]
// Re-running with an existing username resets that account's password and
// makes sure the enrolment is in place, so the command is safe to repeat.

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->libdir . '/clilib.php');
require_once($CFG->dirroot . '/user/lib.php');
require_once($CFG->libdir . '/enrollib.php');

if (count($argv) < 4 || count($argv) > 6) {
    cli_error("Usage: php create-user.php <username> <password> <courseid> [firstname] [lastname]");
}
$username = trim($argv[1]);
$password = $argv[2];
$courseid = (int)$argv[3];
$firstname = $argv[4] ?? ucfirst($username);
$lastname = $argv[5] ?? 'Learner';

if ($username === 'guest' || $username === 'admin') {
    cli_error("The username '{$username}' is reserved by Moodle. Pick another one.");
}

\core\session\manager::set_user(get_admin());

$course = get_course($courseid);
$user = $DB->get_record('user', ['username' => $username, 'mnethostid' => $CFG->mnet_localhost_id]);

if ($user) {
    echo "User {$username} already exists (id {$user->id}).\n";
} else {
    $new = new stdClass();
    $new->username = $username;
    $new->firstname = $firstname;
    $new->lastname = $lastname;
    $new->email = $username . '@example.invalid';
    $new->confirmed = 1;
    $new->mnethostid = $CFG->mnet_localhost_id;
    $new->auth = 'manual';
    $new->policyagreed = 1;
    $userid = user_create_user($new, false, false);
    $user = $DB->get_record('user', ['id' => $userid], '*', MUST_EXIST);
    echo "Created user {$username} (id {$user->id}).\n";
}

// Set the password directly, so a simple shared password is not blocked by policy.
update_internal_user_password($user, $password);
echo "Password set.\n";

// Enrol as a student on the manual enrolment instance.
$instance = $DB->get_record('enrol', ['courseid' => $course->id, 'enrol' => 'manual'], '*', IGNORE_MISSING);
if (!$instance) {
    cli_error("Course {$course->shortname} has no manual enrolment method.");
}
$plugin = enrol_get_plugin('manual');
$studentrole = $DB->get_record('role', ['shortname' => 'student'], '*', MUST_EXIST);
$plugin->enrol_user($instance, $user->id, $studentrole->id);

$url = new moodle_url('/course/view.php', ['id' => $course->id]);
echo "Enrolled {$username} in {$course->fullname} as a student.\n";
echo "Send them {$CFG->wwwroot} and the login {$username} / {$password}\n";
echo "Course: {$url}\n";
