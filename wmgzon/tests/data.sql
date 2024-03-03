INSERT INTO user (username, password, is_admin)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', True),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', True);

INSERT INTO product (title, price, description, author_id, image_filename)
VALUES
  ('test title','300', 'test description', 1, 'WGMZon Logo.png');

INSERT INTO category (product_id, category)
VALpipUES
  (1, 'grocery');

INSERT INTO grocery (product_id, baby_foods, bestseller, beer_wine, frozen, home_care, food_cupboard, gluten_free, vegan, dairy_free)
VALUES
  (1, 0, 0, 0, 0, 0, 1, 0, 0, 1);

INSERT INTO stock_information (product_id, current_stock, starting_stock)
VALUES
    (1, 20, 22)