-- show and add orders
SELECT
    *
FROM
    orders;

SELECT
    *
FROM
    items;

INSERT INTO
    orders (item_name, number)
VALUES
    ('apple', 1);

INSERT INTO
    orders (item_name, number)
VALUES
    ('orange', 2);

INSERT INTO
    orders (item_name, number)
VALUES
    ('banana', 3);

SELECT
    "--";

SELECT
    *
FROM
    orders;

SELECT
    *
FROM
    items;