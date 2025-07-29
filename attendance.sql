create database attendance
use attendance
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Hashed
    role ENUM('student', 'admin') DEFAULT 'student'
);
CREATE TABLE fingerprints (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    fingerprint_template TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE attendance (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    location_verified BOOLEAN DEFAULT FALSE,
    method ENUM('fingerprint', 'manual') DEFAULT 'fingerprint',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE wifi_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    ssid VARCHAR(100),
    mac_address VARCHAR(100),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
INSERT INTO users (name, email, password, role) VALUES
('Amna Saleem', 'amna@example.com', 'hashed_password_1', 'admin'),
('Ali Raza', 'ali@example.com', 'hashed_password_2', 'student'),
('Fatima Noor', 'fatima@example.com', 'hashed_password_3', 'student');
INSERT INTO fingerprints (user_id, fingerprint_template) VALUES
(1, 'template_data_admin'),
(2, 'template_data_ali'),
(3, 'template_data_fatima');
INSERT INTO attendance (user_id, timestamp, location_verified, method) VALUES
(2, NOW(), TRUE, 'fingerprint'),
(3, NOW(), FALSE, 'manual');
INSERT INTO wifi_logs (user_id, ssid, mac_address) VALUES
(2, 'University-WiFi', '00:1A:2B:3C:4D:5E'),
(3, 'Home-WiFi', '11:22:33:44:55:66');
INSERT INTO wifi_logs (user_id, ssid, mac_address) VALUES
(1, 'Home-WiFi', '11:22:33:44:55:66');
















