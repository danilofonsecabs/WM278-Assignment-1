DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    image BLOB NOT NULL,
    price INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    in_stock BOOLEAN,
    FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE grocery (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    expiration_data DATE,
    category TEXT,
    FOREIGN KEY (product_id) REFERENCES product(id)
)
