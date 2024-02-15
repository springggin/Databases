
-- -----------------------------------------------------
-- Table `Airline`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Airline` (
  `ID` INT NOT NULL,
  PRIMARY KEY (`ID`))


-- -----------------------------------------------------
-- Table `Airplane`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Airplane` (
  `ID` INT NOT NULL,
  `seats` INT NOT NULL,
  `Airline_ID` INT ZEROFILL NOT NULL,
  `manufacturing company` VARCHAR(45) NULL,
  `model num` VARCHAR(45) NULL,
  `manufacturing date` DATE NULL,
  `age` INT NULL,
  PRIMARY KEY (`ID`),
  FOREIGN KEY (`Airline_ID`)
  REFERENCES `Airline` (`ID`)
);


-- -----------------------------------------------------
-- Table `Airport`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Airport` (
  `code` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `country` VARCHAR(45) NULL,
  `terminal` INT NULL,
  `type` VARCHAR(10) NULL,
  PRIMARY KEY (`code`));


-- -----------------------------------------------------
-- Table `Flight`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Flight` (
  `id Flight` INT NOT NULL,
  `dep_airport` INT NOT NULL,
  `dep_datetime` DATETIME NULL,
  `arr_airport` INT NOT NULL,
  `arr_datetime` DATETIME NULL,
  `base price` INT NULL,
  `status` VARCHAR(45) NULL,
  `Airplane_ID` INT NOT NULL,
  PRIMARY KEY (`id Flight`),
    FOREIGN KEY (`dep_airport`) REFERENCES `Airport` (`code`),
    FOREIGN KEY (`arr_airport`) REFERENCES `Airport` (`code`),
    FOREIGN KEY (`Airplane_ID`) REFERENCES `Airplane` (`ID`));


UPDATE `aironline`.`flight` SET `dep_time` = '10:00', `arr_time` = '10:00' WHERE (`ID` = '1');
UPDATE `aironline`.`flight` SET `dep_time` = '11:00', `arr_time` = '17:00' WHERE (`ID` = '2');
UPDATE `aironline`.`flight` SET `dep_time` = '17:00', `arr_time` = '18:00' WHERE (`ID` = '3');
UPDATE `aironline`.`flight` SET `dep_time` = '18:00', `arr_time` = '17:00' WHERE (`ID` = '4');
UPDATE `aironline`.`flight` SET `dep_time` = '19:00', `arr_time` = '10:00' WHERE (`ID` = '5');
UPDATE `aironline`.`flight` SET `dep_time` = '10:00', `arr_time` = '18:00' WHERE (`ID` = '6');

-- -----------------------------------------------------
-- Table `Ticket`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Ticket` (
  `ID` INT NOT NULL,
  `email` VARCHAR(45) NULL,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `date_of_birth` DATE NULL,
  `Flight_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
    FOREIGN KEY (`Flight_ID`) REFERENCES `Flight` (`id Flight`));



-- -----------------------------------------------------
-- Table `Customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Customer` (
  `email` VARCHAR(45) NOT NULL,
  `fname` VARCHAR(45) NULL,
  `lname` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `date_of_birth` VARCHAR(45) NULL,
  PRIMARY KEY (`email`));


-- -----------------------------------------------------
-- Table `Maintenance`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Maintenance` (
  `id Maintenance` INT NOT NULL,
  `start_datetime` DATETIME NOT NULL,
  `end_datetime` DATETIME NOT NULL,
  `id Airplane` INT NOT NULL,
  PRIMARY KEY (`id Maintenance`),
    FOREIGN KEY (`id Airplane`) REFERENCES `Airplane` (`ID`));


-- -----------------------------------------------------
-- Table `Purchase`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Purchase` (
  `Customer_email` VARCHAR(45) NOT NULL,
  `Ticket_ID` INT NOT NULL,
  `price` INT NULL,
  `card_type` VARCHAR(45) NULL,
  `card_num` INT NULL,
  `card_name` VARCHAR(45) NULL,
  `exp_date` DATE NULL,
  `purchase_time` DATETIME NULL,
  `Purchasecol` VARCHAR(45) NULL,
  PRIMARY KEY (`Customer_email`, `Ticket_ID`),
  FOREIGN KEY (`Customer_email`) REFERENCES `Customer` (`email`),
 FOREIGN KEY (`Ticket_ID`) REFERENCES `Ticket` (`ID`));


-- -----------------------------------------------------
-- Table `rate`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rate` (
  `Customer_email` VARCHAR(45) NOT NULL,
  `Flight_id Flight` INT NOT NULL,
  `rating` INT NULL,
  `comment` VARCHAR(45) NULL,
  PRIMARY KEY (`Customer_email`, `Flight_id Flight`),
  INDEX `fk_Customer_has_Flight_Flight1_idx` (`Flight_id Flight` ASC) VISIBLE,
  INDEX `fk_Customer_has_Flight_Customer1_idx` (`Customer_email` ASC) VISIBLE,
FOREIGN KEY (`Customer_email`) REFERENCES `Customer` (`email`),
FOREIGN KEY (`Flight_id Flight`) REFERENCES `Flight` (`id Flight`));



-- -----------------------------------------------------
-- Table `AirlineStaff`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AirlineStaff` (
  `username` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`username`));


-- -----------------------------------------------------
-- Table `email`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `email` (
  `email` VARCHAR(45) NOT NULL,
  `AirlineStaff_username` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`email`),
FOREIGN KEY (`AirlineStaff_username`) REFERENCES `AirlineStaff` (`username`)
);


-- -----------------------------------------------------
-- Table `Phone_customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Phone_customer` (
  `phone_num` VARCHAR(12) NOT NULL,
  `Customer_email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`phone_num`),
    FOREIGN KEY (`Customer_email`) REFERENCES `Customer` (`email`));


-- -----------------------------------------------------
-- Table `phone_staff`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `phone_staff` (
  `phone_num` VARCHAR(20) NOT NULL,
  `AirlineStaff_username` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`phone_num`),
FOREIGN KEY (`AirlineStaff_username`) REFERENCES `AirlineStaff` (`username`));


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
