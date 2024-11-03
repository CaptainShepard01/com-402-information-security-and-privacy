<?php
$db = new PDO('sqlite:/var/www/html/database.db');

$db->exec("CREATE TABLE IF NOT EXISTS exams (id INTEGER PRIMARY KEY, year INTEGER, content TEXT);");
$db->exec("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT);");
$db->exec("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'SECRETPASSWORD123');");
$db->exec("INSERT OR IGNORE INTO users (id, username, password) VALUES (2, 'user', 'password123');");
$db->exec("INSERT OR IGNORE INTO exams (id, year, content) VALUES (1, 2023, 'many questions...');");
$db->exec("INSERT OR IGNORE INTO exams (id, year, content) VALUES (2, 2022, 'many questions...');");
$db->exec("INSERT OR IGNORE INTO exams (id, year, content) VALUES (3, 2024, 'TODO');");

if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['year'])) {
	$year = $_GET['year'];
	$query = "SELECT * FROM exams WHERE year = :year";
    $stmt = $db->prepare($query);
    $stmt->bindParam(':year', $year, PDO::PARAM_INT);
    $stmt->execute();
	echo "<h2>Exams:</h2>";
	if ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
		echo "Year: " . $row['year'] . "<br>";
		echo "Content: " . $row['content'] . "<br>";
	} else {
		echo "Exam not found.<br>";
	} 
} else {
	$query = "SELECT * FROM exams";
	$result = $db->query($query);
	echo "<h2>Exams:</h2>";
	foreach ($result as $row) {
	echo "Year: " . $row['year'] . "<br>";
	echo "Content: " . $row['content'] . "<br>";
	
	}
}
?>

