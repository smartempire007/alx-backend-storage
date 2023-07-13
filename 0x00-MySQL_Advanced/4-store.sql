-- Create a trigger that decreases the quantity of
-- an item after adding a new order.
-- New & OLD MySQL extensions to triggers
-- https://stackoverflow.com/questions/11321677/mysql-trigger-new-old-tables
CREATE TRIGGER `decrease_quantity`
AFTER
INSERT
    ON `orders` FOR EACH ROW
UPDATE
    `items`
SET
    `quantity` = `quantity` - NEW.number
WHERE
    `name` = NEW.item_name;