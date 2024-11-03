FROM php:7.4-apache

COPY index.php /var/www/html/
COPY users.php /var/www/html/
COPY ping.php /var/www/html/
COPY exams.php /var/www/html/

RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev  iputils-ping && docker-php-ext-install pdo pdo_sqlite

RUN touch /var/www/html/database.db && chmod 777 /var/www/html/database.db

EXPOSE 80

CMD ["apache2-foreground"]
