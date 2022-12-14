import psycopg2
from psycopg2 import extensions
from threading import Thread


#  Многопоточность, 2 connection на 2 потока

def serializable_connect():
    try:
        connection = psycopg2.connect(
            dbname="semestr_work_db",
            user="postgres",
            password="1737",
            host="localhost",
            port=5432,
        )
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)

        connection.autocommit = False
        cursor = connection.cursor()

        select_query = "SELECT price FROM products WHERE colour='silver';"
        cursor.execute(select_query)
        silver_prod_price = cursor.fetchone()[0]
        amount_to_up = 100
        change_query = f"UPDATE products SET price={silver_prod_price + amount_to_up} WHERE colour='silver'"
        cursor.execute(change_query)
        connection.commit()
        cursor.close()
        connection.close()
        print("Транзакция успешно завершена")

    except (Exception, psycopg2.DatabaseError) as error:
    # except ValueError as error:
        print(f"Транзакция прервана в связи с возникшей ошибкой. Откат до последней версии...")


for i in range(2):
    th = Thread(target=serializable_connect)
    th.start()








# try:
#     connection = psycopg2.connect(
#         dbname="semestr_work_dbs",
#         user="postgres",
#         password="1737",
#         host="localhost",
#         port=5432,
#     )
#     connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
#
#     connection.autocommit = False
#     cursor1 = connection.cursor()
#     cursor2 = connection.cursor()
#
#     select_query = "SELECT price FROM products WHERE colour='silver';"
#     cursor1.execute(select_query)
#     silver_prod_price = cursor1.fetchone()[0]
#     print(silver_prod_price)
#     #  The current price is {silver_prod_price} rubles
#
#     amount_to_up = 100
#     change_query = f"UPDATE products SET price={silver_prod_price + amount_to_up} WHERE colour='silver'"
#     #  Trying to execute second cursor
#     cursor2.execute(change_query)
#     cursor1.execute(select_query)
#     silver_prod_price = cursor1.fetchone()[0]
#     print(silver_prod_price)
#     #  The current price is {silver_prod_price} rubles. Price changed.
#
#     #  Trying to execute first cursor
#     cursor1.execute(change_query)
#
#     connection.commit()
#     print("Транзакция успешно завершена")
#
# except (Exception, psycopg2.DatabaseError) as error:
#     print(f"Транзакция прервана в связи с возникшей ошибкой. Откат до последней версии...")

# Транзакции
# 1 SELECT | 2 UPDATE
# 3 SELECT | 5 END (COMMIT)
# 4 UPDATE |
#
