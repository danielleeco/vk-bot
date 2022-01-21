import sqlite3

try:
    sqlite_connection = sqlite3.connect('bakery.db')
    sqlite_create_sections = '''CREATE TABLE sections (
                                section TEXT NOT NULL);
                                '''
    sqlite_create_products = '''CREATE TABLE products (
                                id_prod INTEGER PRIMARY KEY AUTOINCREMENT,
                                section TEXT NOT NULL,
                                product_name TEXT NOT NULL,
                                price DOUBLE,
                                weight DOUBLE,
                                picture TEXT);
                                '''
    insert_into_sections = '''
        INSERT INTO sections
            (section)
        VALUES
            ('выпечка'), ('донаты'), ('хлеб'), ('мороженое'), ('напитки');
    '''
    insert_into_products = '''
        INSERT INTO products
            (section, product_name, price, weight, picture)
        VALUES
            ('выпечка', 'булочка с корицей', 110, 90, '-210219798_457239031'),
            ('выпечка', 'булочка с сахарной пудрой', 100, 90, '-210219798_457239031'),
            ('выпечка', 'круассан с семгой', 250, 180, '-210219798_457239032'),
            ('донаты', 'орео донат', 95, 75, '-210219798_457239033'),
            ('донаты', 'клубничный донат', 90, 75, '-210219798_457239033'),
            ('донаты', 'банановый донат', 100, 75, '-210219798_457239033'),
            ('донаты', 'шоколадный донат', 90, 75, '-210219798_457239033'),
            ('хлеб', 'хлеб пшеничный', 45, 110, '-210219798_457239034'),
            ('хлеб', 'хлеб со злаками', 95, 110, '-210219798_457239034'),
            ('хлеб', 'багет парижский', 120, 150, '-210219798_457239034'),
            ('мороженое', 'вишневое мороженое', 120, 90, '-210219798_457239036'),
            ('мороженое', 'ванильное мороженое', 120, 90, '-210219798_457239036'),
            ('мороженое', 'фисташковое мороженое', 120, 90, '-210219798_457239036'),
            ('напитки', 'чай', 75, 200, '-210219798_457239035'),
            ('напитки', 'капучино', 120, 200, '-210219798_457239035'),
            ('напитки', 'вода', 70, 200, '-210219798_457239035'),
            ('напитки', 'свежевыжатый сок', 250, 200, '-210219798_457239035');
    '''

    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")
    cursor.execute(sqlite_create_sections)
    cursor.execute(insert_into_sections)
    print("Таблица sqlite_create_sections создана")
    cursor.execute(sqlite_create_products)
    cursor.execute(insert_into_products)
    print("Таблица sqlite_create_products создана")
    sqlite_connection.commit()
    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")
