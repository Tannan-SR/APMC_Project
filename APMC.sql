create database apmc_2;
use apmc_2;
drop schema apmc_2;
show tables;
CREATE TABLE `apmc_2`.`market` (
  `idmarket` INT NOT NULL, 
  `market_name` VARCHAR(45) NULL,
  `location` VARCHAR(45) NULL,
  `timings` VARCHAR(45) NULL,
  PRIMARY KEY (`idmarket`));
  
  CREATE TABLE `apmc_2`.`farmer` (
  `idfarmer` INT NOT NULL,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `contact_no` VARCHAR(45) NULL,
  `address` VARCHAR(45) NULL,
  PRIMARY KEY (`idfarmer`));

CREATE TABLE `apmc_2`.`trader` (
  `idtrader` INT NOT NULL,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `contact_no` VARCHAR(45) NULL,
  `address` VARCHAR(45) NULL,
  PRIMARY KEY (`idtrader`));
  
CREATE TABLE `apmc_2`.`commodity` (
  `idcommodity` INT NOT NULL,
  `commodity_name` VARCHAR(45) NULL,
  `desc` VARCHAR(45) NULL,
  `pricing_trend` DECIMAL(2) NULL,
  PRIMARY KEY (`idcommodity`));
Alter table apmc_2.commodity
add highest_bid decimal(8,2) NULL;

Alter table apmc_2.commodity
drop column pricing_trend ;

ALTER TABLE `apmc_2`.`commodity`
CHANGE COLUMN `desc` `description` VARCHAR(45) NULL;

ALTER TABLE `apmc_2`.`commodity`
ADD INDEX `idx_commodity_name` (`commodity_name`);

  drop table transaction;
CREATE TABLE `apmc_2`.`transaction` (
  `idtransaction` INT NOT NULL AUTO_INCREMENT,
  `farmer_name` VARCHAR(45) NULL,
  `quantity` INT NULL,
  `quality` VARCHAR(45) NULL,  -- Assuming quality is a string, update the data type accordingly
  `description` VARCHAR(255) NULL,  -- Adjust the length based on your needs
  `market_id` INT NOT NULL,
  `trader_id` INT NOT NULL,
  `commodity_id` INT NOT NULL,
  
  PRIMARY KEY (`idtransaction`),
  FOREIGN KEY (`market_id`) REFERENCES `apmc_2`.`market` (`idmarket`),
  FOREIGN KEY (`trader_id`) REFERENCES `apmc_2`.`trader` (`idtrader`),
  FOREIGN KEY (`commodity_id`) REFERENCES `apmc_2`.`commodity` (`idcommodity`)
);
ALTER TABLE `apmc_2`.`transaction`
ADD COLUMN `commodity_name` VARCHAR(45) NULL,
ADD CONSTRAINT `fk_transaction_commodity`
FOREIGN KEY (`commodity_name`) REFERENCES `apmc_2`.`commodity` (`commodity_name`);
select * from transaction;

 


Alter table transaction
Add transaction_date Datetime(2) NULL;


drop table quality_assessment;
CREATE TABLE `apmc_2`.`quality_assessment` (
  `quality_score` INT NULL,
  `comments` MEDIUMTEXT NULL);


Alter table apmc_2.quality_assessment
modify quality_score VARCHAR(45) NULL;

Alter table apmc_2.quality_assessment
add name_commodity VARCHAR(45) NULL;

SELECT t.idtrader, t.first_name, t.last_name, c.idcommodity, c.commodity_name, c.description, COALESCE(SUM(tr.quantity), 0) AS available_quantity
    FROM trader t
    LEFT JOIN transaction tr ON t.idtrader = tr.trader_id
    LEFT JOIN commodity c ON tr.commodity_id = c.idcommodity
    WHERE t.market_id = 1
    GROUP BY t.idtrader, c.idcommodity;




CREATE TABLE `apmc_2`.`payment` (
  `idpayment` INT NOT NULL,
  `transaction_id` INT NULL,
  `amount` DECIMAL(2) NULL,
  `payment_date` DATETIME(2) NULL,
  PRIMARY KEY (`idpayment`));
  ALTER TABLE payment
ADD foreign key (transaction_id) references transaction(idtransaction);

CREATE TABLE bid (
    idbid INT PRIMARY KEY AUTO_INCREMENT,
    bid_date DATETIME NOT NULL,
    bid_amount DECIMAL(8, 2) NOT NULL,
    commodity_id INT NOT NULL,
    trader_id INT NOT NULL,
    market_id INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (commodity_id) REFERENCES commodity(idcommodity),
    FOREIGN KEY (trader_id) REFERENCES trader(idtrader),
    FOREIGN KEY (market_id) REFERENCES market(idmarket)
);

alter table bid
add bid_quantity DECIMAL(8, 2) NOT NULL;

alter table bid
drop status;








ALTER TABLE farmer
ADD market_id INT NULL;
ALTER TABLE farmer
ADD CONSTRAINT fk_farmer_market FOREIGN KEY (market_id) REFERENCES market(idmarket);

ALTER TABLE trader
ADD market_id INT NULL;
ALTER TABLE trader
ADD CONSTRAINT fk_trader_market FOREIGN KEY (market_id) REFERENCES market(idmarket);




ALTER TABLE payment
ADD CONSTRAINT fk_payment_transaction FOREIGN KEY (transaction_id) REFERENCES transaction(idtransaction);

select*from farmer;
select idtrader from trader where first_name = "Sumukh";
delete  from farmer where idfarmer = 2;



select * from market;


SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'trader' AND TABLE_SCHEMA = 'apmc_2';

-- Filling Values from here on

    
INSERT INTO market (idmarket, market_name, location, timings) VALUES
(1, 'Mandi apmc_2', 'Delhi', '9:00 AM - 6:00 PM'),
(2, 'Kisan Bazaar', 'Mumbai', '8:00 AM - 5:00 PM'),
(3, 'Krishi Vikas', 'Bangalore', '10:00 AM - 7:00 PM'),
(4, 'Sabzi Mandi', 'Kolkata', '8:30 AM - 5:30 PM'),
(5, 'Agricultural Hub', 'Chennai', '9:30 AM - 6:30 PM');

INSERT INTO farmer (idfarmer, first_name, last_name, contact_no, address, market_id) VALUES
(1, 'Rajesh', 'Kumar', '9876543210', 'Village1, District1, Maharashtra', 1),
(2, 'Suman', 'Verma', '8765432109', 'Village2, District2, Maharashtra', 1),
(3, 'Amit', 'Singh', '7654321098', 'Village3, District3, Karnataka', 2),
(4, 'Priya', 'Yadav', '6543210987', 'Village4, District4, Karnataka', 2),
(5, 'Neha', 'Sharma', '7890123456', 'Village5, District5, Tamil Nadu', 3);

INSERT INTO trader (idtrader, first_name, last_name, contact_no, address, market_id) VALUES
(1, 'Amit', 'Sharma', '7654321098', 'Mumbai, Maharashtra', 1),
(2, 'Priya', 'Singh', '6543210987', 'Pune, Maharashtra', 1),
(3, 'Rahul', 'Verma', '5432109876', 'Bangalore, Karnataka', 2),
(4, 'Anjali', 'Yadav', 'Mysuru', 'Karnataka', 2),
(5, 'Suresh', 'Kumar', '3210987654', 'Chennai, Tamil Nadu', 3);


-- Insert into commodity table
INSERT INTO commodity (idcommodity, commodity_name, `description`) VALUES
(1, 'Rice', 'Basmati Rice from Northern India'),
(2, 'Wheat', 'Indian Whole Wheat Flour'),
(3, 'Potatoes', 'Fresh Potatoes'),
(4, 'Tomatoes', 'Organic Tomatoes'),
(5, 'Onions', 'Red Onions');
-- Update commodity table with correct pricing trends
-- UPDATE commodity SET pricing_trend = 0.05 WHERE idcommodity = 1;
-- UPDATE commodity SET pricing_trend = 0.03 WHERE idcommodity = 2;
-- UPDATE commodity SET pricing_trend = 0.02 WHERE idcommodity = 3;
-- UPDATE commodity SET pricing_trend = 0.04 WHERE idcommodity = 4;
-- UPDATE commodity SET pricing_trend = 0.01 WHERE idcommodity = 5;


INSERT INTO transaction (farmer_name, transaction_date, quantity, quality, description, market_id, trader_id, commodity_id)
VALUES
('Farmer 1', '2023-11-11 12:00:00', 100, 'High', 'Transaction 1 description', 1, 1, 1),
('Farmer 2', '2023-11-12 14:30:00', 150, 'Medium', 'Transaction 2 description', 2, 2, 2),
('Farmer 3', '2023-11-13 15:45:00', 80, 'Low', 'Transaction 3 description', 3, 3, 3),
('Farmer 4', '2023-11-14 10:30:00', 120, 'High', 'Transaction 4 description', 4, 4, 4),
('Farmer 5', '2023-11-15 11:15:00', 200, 'Medium', 'Transaction 5 description', 5, 5, 5);

desc quality_assessment;

INSERT INTO quality_assessment ( quality_score, comments) VALUES
( 'A', 'High quality produce'),
( 'B', 'Average quality produce'),
( 'S', 'Excellent quality potatoes'),
( 'C', 'Satisfactory quality tomatoes'),
( 'S', 'Top-grade onions');

ALTER TABLE payment MODIFY COLUMN amount DECIMAL(8, 2);

INSERT INTO payment (idpayment, transaction_id, amount, payment_date) VALUES
(1, 1, 5000.00, '2023-11-12 15:00:00'),
(2, 2, 6750.00, '2023-11-13 10:00:00'),
(3, 3, 2400.00, '2023-11-14 12:30:00'),
(4, 4, 4800.00, '2023-11-15 11:45:00'),
(5, 5, 5000.00, '2023-11-16 09:30:00');

show tables;

-- commodity
-- farmer
-- market
-- payment
-- quality_assessment
-- trader
-- transaction
-- Update trader table to fix the city name for id = 4
UPDATE trader SET address = 'Mysuru, Karnataka' WHERE idtrader = 4;
-- Update trader table to fix the contact number and city name for id = 4
UPDATE trader SET contact_no = '4321098765' WHERE idtrader = 4;

select * from trader;

-- User's Table
CREATE TABLE users (
    id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role VARCHAR(20) NOT NULL
);
INSERT INTO users (id,first_name, last_name, role) VALUES
(1,'Amit', 'Sharma', 'trader'),
(2,'Priya', 'Singh', 'trader');
-- Admin users
INSERT INTO users (id,first_name, last_name, role) VALUES
(3,'Siddharth', 'Mishra', 'admin'),
(4,'Neha', 'Bansal', 'admin');

-- Bidder users
INSERT INTO users (id,first_name, last_name, role) VALUES
(5,'Vikram', 'Pillai', 'bidder'),
(6,'Meera', 'Khanna', 'bidder');

DELIMITER //

CREATE PROCEDURE update_highest_bid(IN commodity_id INT)
BEGIN
    DECLARE highest_bid_amount DECIMAL(8, 2);

    -- Find the highest bid amount for the given commodity
    SELECT MAX(bid_amount) INTO highest_bid_amount
    FROM bid
    WHERE commodity_id = commodity_id;

    -- Update the commodity table with the highest bid amount
    UPDATE commodity
    SET highest_bid = highest_bid_amount
    WHERE idcommodity = commodity_id;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER after_bid_insert
AFTER INSERT
ON bid FOR EACH ROW
BEGIN
    -- Call the stored procedure to update the highest bid
    CALL update_highest_bid(NEW.commodity_id);
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER after_transaction_insert
AFTER INSERT ON transaction
FOR EACH ROW
BEGIN
    DECLARE commodity_name VARCHAR(255);
    DECLARE commodity_quality VARCHAR(45);
    DECLARE commodity_description VARCHAR(255);

    -- Retrieve commodity details based on the inserted commodity_id
    SELECT  description
    INTO  commodity_description
    FROM commodity
    WHERE idcommodity = NEW.commodity_id;

    -- Set quality from the transaction table
    SET commodity_quality = NEW.quality;
    SET commodity_name = NEW.commodity_name;
    
    -- Insert the extracted details into the quality_assessment table
    INSERT INTO quality_assessment (name_commodity, quality_score, comments)
    VALUES (commodity_name, commodity_quality, commodity_description);
END;
//

DELIMITER ;

drop trigger after_transaction_insert;











select * from commodity;
select * from quality_assessment;
select*from transaction;
INSERT INTO transaction (farmer_name, commodity_id, quantity, quality, description, market_id, trader_id, transaction_date)
        VALUES ("rajesh", 1, 10, "S", "Good", 1, 1, "2023-11-11 12:00:11.11");

 select tr.idtrader, tr.first_name, tr.last_name, rght.commodity_name, rght.quantity
                from trader tr
                left join
                (select C.commodity_name, T.quantity, T.trader_id
                from transaction T
                left join commodity C
                on T.commodity_id = C.idcommodity) as rght
                on tr.idtrader = rght.trader_id
                where tr.market_id = 1; 


select * from bid;
truncate table quality_assessment;

desc bid;
desc commodity;
desc farmer;
desc market;
desc payment;
desc quality_assessment;
desc trader;
desc transaction;
desc users;

 
select * from commodity;
