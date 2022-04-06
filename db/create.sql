-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    category VARCHAR(255)
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Product_Feedback(
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    ratings INT NOT NULL,
    review VARCHAR(3000) NOT NULL,
    time_submitted timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    vote INT NOT NULL DEFAULT 0
);

CREATE TABLE Seller_Feedback(
    uid INT NOT NULL REFERENCES Users(id),
    sid INT NOT NULL REFERENCES Users(id),
    ratings INT NOT NULL,
    review VARCHAR(3000) NOT NULL,
    time_submitted timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    vote INT NOT NULL DEFAULT 0
);
------------------------------------
-- below are changes for users


ALTER TABLE users
ADD COLUMN address TEXT;

ALTER TABLE users
ADD COLUMN balance INT;

UPDATE users SET balance = 0 WHERE balance is NULL;

------------------------------------
-- below are changes for inventory


CREATE TABLE Inventory (
    pid INT NOT NULL,
    sid INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    quantity INT NOT NULL,
    description VARCHAR(255)
);

ALTER TABLE ONLY inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (pid, sid);

ALTER TABLE ONLY inventory
    ADD CONSTRAINT inventory_pid_fkey FOREIGN KEY (pid) REFERENCES products(id);

ALTER TABLE ONLY inventory
    ADD CONSTRAINT inventory_sid_fkey FOREIGN KEY (sid) REFERENCES users(id);
    
------------------------------------
-- below are changes for cart

CREATE TABLE Cart (
    uid INT NOT NULL,
    pid INT NOT NULL,
    sid INT NOT NULL,
    quantity INT NOT NULL
);

ALTER TABLE ONLY Cart
    ADD CONSTRAINT cart_pkey PRIMARY KEY (uid, pid, sid);

ALTER TABLE ONLY Cart
    ADD CONSTRAINT cart_uid_fkey FOREIGN KEY (uid) REFERENCES Users(id);

ALTER TABLE ONLY Cart
    ADD CONSTRAINT cart_pid_fkey FOREIGN KEY (pid) REFERENCES Products(id);

ALTER TABLE ONLY Cart
    ADD CONSTRAINT cart_sid_fkey FOREIGN KEY (sid) REFERENCES Users(id);

------------------------------------
-- below are changes for feedback
ALTER TABLE ONLY Product_Feedback
    ADD CONSTRAINT Product_Feedback_pkey PRIMARY KEY (uid, pid);

ALTER TABLE ONLY Seller_Feedback
    ADD CONSTRAINT Seller_Feedback_pkey PRIMARY KEY (uid, sid);
