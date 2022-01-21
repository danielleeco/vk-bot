import sqlite3

from bakery_bot.database import SessionLocal
from bakery_bot import models


def sqlite_():
    try:
        sqlite_connection = sqlite3.connect('bakery.db')
        cursor = sqlite_connection.cursor()
        # cursor.execute("SELECT * FROM sections")
        # sec = "выпечка"
        # cursor.execute(f"SELECT product_name FROM products WHERE section = '{sec}' ")
        sec = "булочка с корицей"
        cursor.execute(f"SELECT product_name, price, weight, picture FROM products WHERE product_name = '{sec}' ")
        rows = cursor.fetchall()
        print(rows)
        for i in range(len(rows)):
            for item in rows[i]:
                print(item)

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return rows


def get_db():
    db = SessionLocal()
    sections = [i.section for i in db.query(models.Sections).all()]
    names_from_sections = [
        i.product_name for i in db.query(models.Products)
        .filter(models.Products.section == 'выпечка').all()
    ]
    item_card = [
        (i.product_name, i.price, i.weight, i.picture) for i in db.query(models.Products)
        .filter(models.Products.product_name == 'булочка с корицей').all()
    ]
    print(sections)
    print(names_from_sections)
    print(item_card)


get_db()
