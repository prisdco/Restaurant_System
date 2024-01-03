import mysql.connector

def Initialize():
    conn = mysql.connector.connect(user="root", password="admin", database="restaurantdb",host="localhost")

    #conn = sqlite3.connect("restaurantdb.db")    
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE  IF NOT EXISTS `restaurantdb`;")
    cursor.close
    cursor.execute("USE `restaurantdb`;")
    cursor.close
    cursor.execute("CREATE TABLE IF NOT EXISTS restaurant_info (restaurantId INT NOT NULL,RestaurantName VARCHAR(90) NOT NULL,Cuisine VARCHAR(45) NULL,Zone VARCHAR(45) NULL,Category VARCHAR(45) NULL,Store INT NULL,Manager VARCHAR(45) NULL,Years_as_manager INT NULL,Email VARCHAR(45) NULL, Address LONGTEXT NULL,PRIMARY KEY (restaurantId));")
    cursor.close
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (orderId VARCHAR(50) NOT NULL,restaurantId int NOT NULL, first_customer_name varchar(45) DEFAULT NULL,order_date datetime DEFAULT NULL, quantity_of_item int DEFAULT NULL, order_amount decimal(8,2) DEFAULT NULL, payment_mode varchar(45) DEFAULT NULL,delivery_time_taken int DEFAULT NULL,customer_rating_food int DEFAULT NULL,  customer_rating_delivery int DEFAULT NULL, credit_card varchar(45) DEFAULT NULL,debit_card varchar(45) DEFAULT NULL,card_provider varchar(45) DEFAULT NULL, last_customer_name varchar(45) DEFAULT NULL,delivery_staff varchar(45) DEFAULT NULL,delivery_vehicle varchar(45) DEFAULT NULL,PRIMARY KEY (orderId),KEY RestaurantId_idx (restaurantId),CONSTRAINT RestaurantId FOREIGN KEY (restaurantId) REFERENCES restaurant_info (restaurantId));")
    cursor.close
    

    try:
        cursor.execute("SELECT delivery_staff FROM orders")
        fetchColNum = cursor.fetchall()        
    except:
        cursor.execute("ALTER TABLE orders ADD COLUMN delivery_staff VARCHAR(45) NULL AFTER last_customer_name, ADD COLUMN delivery_vehicle VARCHAR(45) NULL AFTER delivery_staff;")
    
    cursor.execute("SHOW INDEX FROM orders where Key_name='RestaurantId_idx'")
    checkIndex = cursor.fetchall()
    checkIndexNum = int(cursor.rowcount)
    if(checkIndexNum < 1):
        cursor.execute("ALTER TABLE orders ADD INDEX RestaurantId_idx (restaurantId ASC) VISIBLE;")

    cursor.execute("SELECT * FROM  information_schema.table_constraints WHERE  table_schema = schema() AND table_name = 'orders' AND CONSTRAINT_NAME='RestaurantId';")
    fetchData = cursor.fetchall()
    fetchDataNum = int(cursor.rowcount)
    if(fetchDataNum < 1):
        cursor.execute("ALTER TABLE orders ADD CONSTRAINT RestaurantId FOREIGN KEY (restaurantId) REFERENCES restaurant_info (restaurantId) ON DELETE NO ACTION ON UPDATE NO ACTION;")
    conn.commit()

    conn.close()

def GetAllRestaurantRecords():
    conn = mysql.connector.connect(user="root", password="admin", database="restaurantdb",host="localhost")

    #conn = sqlite3.connect("restaurantdb.db")    
    cursor = conn.cursor()
    cursor.execute("Select * FROM restaurant_info")
    rows = cursor.fetchall()
    return rows

def GetRestaurantRecord(RestaurantId):
    conn = mysql.connector.connect(user="root", password="admin", database="restaurantdb",host="localhost")

    #conn = sqlite3.connect("restaurantdb.db")    
    cursor = conn.cursor()
    cursor.execute(f"Select * FROM restaurant_info WHERE restaurantId={RestaurantId}")
    rows = cursor.fetchall()
    return rows

def InsertIntoRestaurant(restaurantId, RestaurantName, Cuisine, Zone, Category, Store, Manager, Years_as_manager, Email, Address):    
    conn = mysql.connector.connect(user="root", password="admin", database="restaurantdb",host="localhost")
    cursor = conn.cursor()
    sql = f"INSERT INTO restaurant_info (restaurantId, RestaurantName, Cuisine, Zone, Category, Store, Manager, Years_as_manager, Email, Address) VALUES({restaurantId}, '{RestaurantName}', '{Cuisine}', '{Zone}', '{Category}', {Store}, '{Manager}', {Years_as_manager}, '{Email}', '{Address}')"
    cursor.execute(sql)
    conn.commit()
    conn.close

def UpdateRestaurantInfo(RestaurantId, RestaurantName, Cuisine, Zone, Category, Store, Manager, Years_as_manager, Email, Address):
    conn = mysql.connector.connect(user="root", password="admin", database="restaurantdb",host="localhost")
    cursor = conn.cursor()
    sql = f"UPDATE restaurant_info SET RestaurantName='{RestaurantName}', Cuisine='{Cuisine}', Zone='{Zone}', Category='{Category}', Store={Store}, Manager='{Manager}', Years_as_manager={Years_as_manager}, Email='{Email}', Address='{Address}' WHERE restaurantId={RestaurantId}"
    print(sql)
    conn.commit()
    conn.close

def DeleteRestaurantInfo(RestaurantId):
    conn = mysql.connector.connect(user="root", password="admin", database="restaurantdb",host="localhost")
    cursor = conn.cursor()
    sql = f"DELETE FROM restaurantdb.restaurant_info WHERE restaurantId={RestaurantId}"
    cursor.execute(sql)
    conn.commit()
    conn.close

#Orders Queries Record
    
def CalculateMeanQuery():
    conn = mysql.connector.connect(user="root", password="admin", database="restaurantdb",host="localhost")  
    cursor = conn.cursor()
    sql = "Select restaurant_info.RestaurantName, COUNT(orders.restaurantId) as Restaurant, SUM(orders.customer_rating_food) as Rating FROM orders inner join restaurant_info on orders.restaurantId=restaurant_info.restaurantId group by orders.restaurantId order by orders.restaurantId"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows
    
    
def GetAllOrdersRecords():
    conn = mysql.connector.connect(user="root", password="admin", database="restaurantdb",host="localhost")

    #conn = sqlite3.connect("restaurantdb.db")    
    cursor = conn.cursor()
    cursor.execute("Select orderId,restaurantId,first_customer_name,order_date,quantity_of_item,order_amount,payment_mode,delivery_time_taken,customer_rating_food,customer_rating_delivery,credit_card,debit_card,card_provider,last_customer_name FROM orders")
    rows = cursor.fetchall()
    return rows

def GetOrderRecord(orderId):
    conn = mysql.connector.connect(user="root", password="admin", database="restaurantdb",host="localhost")

    #conn = sqlite3.connect("restaurantdb.db")    
    cursor = conn.cursor()
    sql=f"Select orderId,restaurantId,first_customer_name,order_date,quantity_of_item,order_amount,payment_mode,delivery_time_taken,customer_rating_food,customer_rating_delivery,credit_card,debit_card,card_provider,last_customer_name FROM orders WHERE orderId='{orderId}'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def InsertIntoOrder(orderId, restaurantId,first_customer_name, order_date, quantity_of_item, order_amount, payment_mode, delivery_time_taken, customer_rating_food, customer_rating_delivery, credit_card, debit_card, card_provider, last_customer_name):    
    conn = mysql.connector.connect(user="root", password="admin", database="restaurantdb",host="localhost")
    cursor = conn.cursor()
    sql = f"INSERT INTO orders (orderId, restaurantId, first_customer_name, order_date, quantity_of_item, order_amount, payment_mode, delivery_time_taken, customer_rating_food, customer_rating_delivery, credit_card, debit_card, card_provider, last_customer_name) VALUES('{orderId}', {restaurantId}, '{first_customer_name}', '{order_date}', {quantity_of_item}, {order_amount}, '{payment_mode}', {delivery_time_taken}, {customer_rating_food}, {customer_rating_delivery}, '{credit_card}', '{debit_card}', '{card_provider}', '{last_customer_name}')"
    cursor.execute(sql)
    conn.commit()
    conn.close

def UpdateOrdersInfo(orderId, restaurantId,first_customer_name, order_date, quantity_of_item, order_amount, payment_mode, delivery_time_taken, customer_rating_food, customer_rating_delivery, credit_card, debit_card, card_provider, last_customer_name):
    conn = mysql.connector.connect(user="root", password="admin", database="restaurantdb",host="localhost")
    cursor = conn.cursor()
    sql = f"UPDATE orders SET restaurantId={restaurantId}, first_customer_name='{first_customer_name}', order_date='{order_date}', quantity_of_item={quantity_of_item}, order_amount={order_amount}, payment_mode='{payment_mode}', delivery_time_taken={delivery_time_taken}, customer_rating_food={customer_rating_food}, customer_rating_delivery={customer_rating_delivery}, credit_card='{credit_card}', debit_card='{debit_card}', card_provider='{card_provider}', last_customer_name='{last_customer_name}'  WHERE orderId='{orderId}'"
    cursor.execute(sql)
    conn.commit()
    conn.close

def DeleteOrderInfo(orderId):
    conn = mysql.connector.connect(user="root", password="admin", database="restaurantdb",host="localhost")
    cursor = conn.cursor()
    sql = f"DELETE FROM restaurantdb.orders WHERE orderId='{orderId}'"
    cursor.execute(sql)
    conn.commit()
    conn.close