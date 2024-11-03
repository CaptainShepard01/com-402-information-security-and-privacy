<?php
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['host'])) {
    $cmd = $_GET['host'];
    echo "<h2>Ping result</h2>";
    echo "<pre>";
    $output = shell_exec("ping -c 4 " . escapeshellarg($cmd));
    echo htmlspecialchars($output); 
    echo "</pre>";
} else {
    echo "No host provided.<br>";
}
?>

