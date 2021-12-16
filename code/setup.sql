DROP DATABASE IF EXISTS app_database;
CREATE DATABASE app_database;

DROP USER IF EXISTS app_admin;
CREATE USER app_admin WITH PASSWORD 'admin_password';

GRANT ALL PRIVILEGES ON DATABASE app_database TO app_admin;

DROP DATABASE IF EXISTS app_database2;
CREATE DATABASE app_database2;

DROP USER IF EXISTS app_admin2;
CREATE USER app_admin2 WITH PASSWORD 'admin_password2';

GRANT ALL PRIVILEGES ON DATABASE app_database2 TO app_admin2;
