create database clothing_store;
show databases;


use clothing_store;
create table inventory(
id int primary key,
brand varchar(100) not null,
category varchar(50),
size varchar(10),
cost_price varchar(20),
sell_price varchar(20),
stock_quantity varchar(20),
last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

show tables;
select * from inventory;	
alter table inventory
modify id int auto_increment;
describe inventory;

<<<<<<< HEAD
=======
select * from sales;	

>>>>>>> a6065a2 (Saving local work before syncing with remote)
CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    brand varchar(100),
    category varchar(50),
    quantity INT,
    total_price DECIMAL(10, 2),
<<<<<<< HEAD
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES inventory(id)
);
=======
    profit DECIMAL(10, 2),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES inventory(id)
);
ALTER TABLE inventory MODIFY cost_price DECIMAL(10, 2);
ALTER TABLE inventory MODIFY sell_price DECIMAL(10, 2);
>>>>>>> a6065a2 (Saving local work before syncing with remote)

alter table sales
modify total_price int;


<<<<<<< HEAD
=======
ALTER TABLE inventory MODIFY cost_price DECIMAL(10, 2);
ALTER TABLE inventory MODIFY sell_price DECIMAL(10, 2);
ALTER TABLE sales MODIFY total_price DECIMAL(10, 2);
ALTER TABLE sales MODIFY profit DECIMAL(10, 2);
>>>>>>> a6065a2 (Saving local work before syncing with remote)

