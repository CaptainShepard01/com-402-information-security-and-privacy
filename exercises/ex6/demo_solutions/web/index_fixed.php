<!DOCTYPE html>
<html>
<head>
    <title>COM402 Webapp</title>
</head>
<body>
    <h1>COM402 Webapp</h1>
    
    <h2>Retrieve your password</h2>
    <form action="users_fixed.php" method="GET">
        <label for="user">Enter Username:</label>
        <input type="text" id="user" name="user">
        <input type="submit" value="Search">
    </form>

     <h2>Retrieve exams</h2>
    <form action="exams_fixed.php" method="GET">
        <label for="year">Enter year:</label>
        <input type="text" id="year" name="year">
        <input type="submit" value="Search">
    </form>

    <h2>Ping a host</h2>
    <form action="ping_fixed.php" method="GET">
        <label for="host">Enter host to ping:</label>
        <input type="text" id="host" name="host">
        <input type="submit" value="Execute">
    </form>
</body>
</html>
