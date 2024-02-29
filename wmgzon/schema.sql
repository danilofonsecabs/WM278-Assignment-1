DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS stock_information;

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    image_filename TEXT,
--     rating INTEGER NOT NULL,
--     in_stock BOOLEAN,
--     image BLOB NOT NULL,
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