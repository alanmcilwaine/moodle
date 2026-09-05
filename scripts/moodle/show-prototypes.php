<?php
// Report which template each CodeRunner prototype in the bank carries, so a
// stale or cached prototype is visible without opening the UI.
// Usage: php show-prototypes.php
// Runs inside the moodle container.

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->libdir . '/clilib.php');

$rows = $DB->get_records_sql("
    SELECT q.id, q.name, o.template
      FROM {question} q
      JOIN {question_coderunner_options} o ON o.questionid = q.id
     WHERE q.name LIKE 'PROTOTYPE_%'
  ORDER BY q.name, q.id");

if (!$rows) {
    echo "No prototype questions found in the bank.\n";
    exit(1);
}

foreach ($rows as $row) {
    // The old failure handling printed to stderr and exited 1. Its absence
    // marks the template that renders failures into the results table.
    $version = strpos($row->template, 'file=sys.stderr') === false ? 'new' : 'OLD';
    echo "{$row->name} (id {$row->id}): {$version} template\n";
}
