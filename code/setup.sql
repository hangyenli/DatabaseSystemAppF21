DROP DATABASE IF EXISTS app_database;
CREATE DATABASE app_database;

DROP USER IF EXISTS app_admin;
CREATE USER app_admin WITH PASSWORD 'admin_password';

GRANT ALL PRIVILEGES ON DATABASE app_database TO app_admin;
