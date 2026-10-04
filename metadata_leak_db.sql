-- Create database
CREATE DATABASE IF NOT EXISTS metadata_leak_db;
USE metadata_leak_db;

-- Create tables
CREATE TABLE IF NOT EXISTS file_uploads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45)
);

CREATE TABLE IF NOT EXISTS metadata_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT NOT NULL,
    metadata_key VARCHAR(255) NOT NULL,
    metadata_value TEXT,
    risk_level ENUM('Low', 'Medium', 'High') NOT NULL,
    FOREIGN KEY (file_id) REFERENCES file_uploads(id) ON DELETE CASCADE
);

-- Create user with privileges
CREATE USER IF NOT EXISTS 'metadata_user'@'localhost' IDENTIFIED BY 'securepassword123';
GRANT ALL PRIVILEGES ON metadata_leak_db.* TO 'metadata_user'@'localhost';
FLUSH PRIVILEGES;