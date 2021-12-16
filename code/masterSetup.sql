DROP DATABASE IF EXISTS master_database;
CREATE DATABASE master_database;

DROP USER IF EXISTS master_admin;
CREATE USER master_admin WITH PASSWORD 'master_password';

GRANT ALL PRIVILEGES ON DATABASE master_database TO master_admin;
