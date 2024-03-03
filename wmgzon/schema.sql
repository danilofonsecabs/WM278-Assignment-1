DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS stock_information;
DROP TABLE IF EXISTS grocery;

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL
);

CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    image_filename TEXT,
    FOREIGN KEY (author_id) REFERENCES user (id)

);

CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    category TEXT,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE grocery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER UNIQUE NOT NULL,
    baby_foods BOOLEAN NOT NULL,
    bestseller BOOLEAN NOT NULL,
    beer_wine BOOLEAN NOT NULL,
    frozen BOOLEAN NOT NULL,
    home_care BOOLEAN NOT NULL,
    food_cupboard BOOLEAN NOT NULL,
    gluten_free BOOLEAN NOT NULL,
    vegan BOOLEAN NOT NULL,
    dairy_free BOOLEAN NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE stock_information (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER UNIQUE NOT NULL,
    current_stock INTEGER NOT NULL,
    starting_stock INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id)
);