CREATE DATABASE restaurant_db;
USE restaurant_db;

CREATE TABLE restaurants_list (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

SELECT * FROM restaurants_list;

USE restaurant_db;

CREATE TABLE menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    rating FLOAT NULL,
    rating_count INT NULL
);

SELECT * FROM menu_items;

ALTER TABLE menu_items MODIFY COLUMN price DECIMAL(10,2);
