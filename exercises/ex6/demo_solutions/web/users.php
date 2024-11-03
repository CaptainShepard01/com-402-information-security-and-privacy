<?php
$db = new PDO('sqlite:/var/www/html/database.db');

$db->exec("CREATE TABLE IF NOT EXISTS exams (id INTEGER PRIMARY KEY, year TEXT, content TEXT);");
$db->exec("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT);");
$db->exec("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'SECRETPASSWORD123');");
$db->exec("INSERT OR IGNORE INTO users (id, username, password) VALUES (2, 'user', 'password123');");
$db->exec("INSERT OR IGNORE INTO exams (id, year, content) VALUES (1, '2023', 'many questions...');");
$db->exec("INSERT OR IGNORE INTO exams (id, year, content) VALUES (2, '2022', 'many questions...');");
$db->exec("INSERT OR IGNORE INTO exams (id, year, content) VALUES (3, '2024', 'TODO');");

if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['user'])) {
    $username = $_GET['user'];
    if($username === "admin"){
    	echo "nope<br>";
    }
    else{
	$query = "SELECT * FROM users WHERE username = '$username'";
	$result = $db->query($query);
	// echo $query;
	echo "<h2>User data</h2>";
	if ($row = $result->fetch()) {
	echo "User: " . $row['username'] . "<br>";
	echo "Password: " . $row['password'] . "<br>";
	} else {
	echo "User not found.<br>";
	} 
    }
} else {
    echo "No user parameter provided.<br>";
}
?>

