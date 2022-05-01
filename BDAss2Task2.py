import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="slavalox",
                                  host="127.0.0.1",
                                  port="5432")
    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # Удаляем старую таблицу и меняем на новую
    drop = '''DROP TABLE Customers'''
    cursor.execute(drop)
    # Creation of tables. In customers table I included field "product_id", because otherwise it would be impossible to understand what product customer ordered.
    sql_create_customers = '''CREATE TABLE Customers
                             (customer_pkey SERIAL PRIMARY KEY,
                              customer_id INTEGER,
                              customer_name char(20),
                              address char(40),
                              review text,
                              product_id INTEGER);'''
    cursor.execute(sql_create_customers)
    sql_create_purchases = '''CREATE TABLE Purchases
                              (purchase_id SERIAL PRIMARY KEY,
                               customer_id INTEGER);'''
    cursor.execute(sql_create_purchases)
    sql_create_purchases_products_list = '''CREATE TABLE Purchases_products_list
                                            (purchases_products_list_id SERIAL PRIMARY KEY,
                                             purchase_id INTEGER,
                                             product_id INTEGER);'''
    cursor.execute(sql_create_purchases_products_list)

    sql_create_products = '''CREATE TABLE products
                             (product_id SERIAL PRIMARY KEY,
                              product_name TEXT,
                              details TEXT,
                              price FLOAT(2),
                              product_type TEXT);'''
    cursor.execute(sql_create_products)

    sql_create_sales = '''CREATE TABLE Sales
                          (sales_id SERIAL PRIMARY KEY,
                           product_sales_type TEXT,
                           discount INTEGER);'''
    cursor.execute(sql_create_sales)
    # filling tables with values
    sql_fill_customers = '''INSERT INTO Customers (customer_id, customer_name, address, review, product_id) VALUES
                            (1, 'Ilya Razbezhkin', 'Universitetskaya 1 k.2', 'Great chair! Enjoy seating on it very much.', 1),
                            (1, 'Ilya Razbezhkin', 'Universitetskaya 1 k.2', 'Awfull vape. Broke in a week.', 2),
                            (2, 'Slava Ribalchenko', 'Universitetskaya 12 k.1', 'Average vape, it is good, but not more.', 2),
                            (3, 'Danila Kuzmin', 'Universitetskaya 1 k.1', 'Amazing notebook! The design is fantastic.', 3);'''
    cursor.execute(sql_fill_customers)

    sql_fill_purchases = '''INSERT INTO Purchases (customer_id)
                            (SELECT customer_id FROM Customers GROUP BY customer_id)'''
    cursor.execute(sql_fill_purchases)

    sql_fill_products = '''INSERT INTO Products (product_name, details, price, product_type) VALUES
                           ('Chair', 'Wooden', 20, 'Furniture'),
                           ('Vape', 'HQD', 15, 'Smoking'),
                           ('Laptop', 'HP', 800, 'Technique');'''
    cursor.execute(sql_fill_products)

    sql_fill_purchases_products_list = '''INSERT INTO Purchases_products_list (purchase_id, product_id)
                                          WITH p1 AS (SELECT purchase_id FROM purchases), p2 AS (SELECT product_id FROM products)
                                          SELECT p1.purchase_id, p2.product_id FROM p1, p2;'''
    cursor.execute(sql_fill_purchases_products_list)

    sql_fill_sales = '''INSERT INTO Sales (product_sales_type, discount) VALUES
                        ('Furniture', 20),
                        ('Smoking', 10),
                        ('Technique', 0);'''
    cursor.execute(sql_fill_sales)

    # Queries
    products_with_discount = '''SELECT product_name, product_type, customer_name FROM purchases
                                RIGHT JOIN customers USING(customer_id)
                                INNER JOIN products USING(product_id)
                                INNER JOIN sales ON product_sales_type = product_type WHERE discount > 0 GROUP BY product_name, product_type, customer_name;'''
    cursor.execute(products_with_discount)

    find_saved_money = '''SELECT customer_name, SUM(price*discount/100) AS saved_money FROM customers
                          INNER JOIN products USING(product_id)
                          INNER JOIN sales ON product_sales_type = product_type GROUP BY customer_name'''
    cursor.execute(find_saved_money)

    # indexes
    index_creation = '''CREATE INDEX type_product ON products (type);
                        CREATE INDEX type_sales ON sales (type);'''

    selected = cursor.fetchall()
    for row in selected:
        print(row)
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
