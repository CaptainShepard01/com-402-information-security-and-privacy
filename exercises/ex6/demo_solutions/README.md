# Solutions

## Binex

The `solution.py` script is the pwntools script that contains the exploit code for all challenge binaries.

Below are short explanations for each.

## Web

The *_fixed.php files are the fixed versions that prevent the injection attacks.

### Command Injection

User input is read from the URL and appended to the "ping -c 4 " string. The string built this way is then passed to the shell_exec function that just executes the input argument as a shell command.
This allows executing arbitrary shell commands by adding a shell control character that "escapes" the ping command, for example `; && || `. The following user input executes the `ls` command. `8.8.8.8 && ls`.

### SQL Injection (users.php)

The goal is the read the password of the admin user.

User input is read from the URL and inserted into the `$query = "SELECT * FROM users WHERE username = '$username'";` string. 
This query is then executed. An attacker can pass SQL control characters in the input such as a single quote `'` and thus the attacker can extend the logic of the SQL query. The user input `' OR 1=1; #` will result in the following SQL query: `SELECT * FROM users WHERE username = '' OR 1=1; #` which will fetch all rows of the table, including the admin row.

### SQL Injection (exams.php)

User input is read from the URL and inserted into the `$query = "SELECT * FROM exams WHERE year = '$year'";` string. This string is then directly executed as an SQL query.
However unlike in the previous SQL injection the injection takes place in the exams table. In order to still retrieve data from the users table the attacker can use the SQL injection to build a UNION SQL query.
The user input `' UNION SELECT * FROM users; #` will result in the following SQL query: `SELECT * FROM exams WHERE year = '' UNION SELECT * FROM users; #`, which will fetch all rows from the users table including the admin row.
