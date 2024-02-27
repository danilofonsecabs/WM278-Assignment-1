DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS grocery;

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

CREATE TABLE grocery (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    expiration_data DATE,
    category TEXT,
    FOREIGN KEY (product_id) REFERENCES product(id)
)
