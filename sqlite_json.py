import sqlite3
import json
import xlsxwriter

conn = sqlite3.connect('avito/orders.db')
cur = conn.cursor()


def create_db():
    cur.execute("""CREATE TABLE "Avito_product" (
        'Название товара'  TEXT,
        'Ссылка на товар' TEXT,
        'Цена' INTEGER,
        'Цена в евро' REAL,
        'Категория товара' TEXT,
        'Описание товара' TEXT,
        'Фото' TEXT,
        'Адрес' TEXT,
        'Имя владельца' TEXT
    );""")


def commit_db():
    with open('avito/avito_products.json', 'r', encoding='UTF-8') as file:
        text = json.load(file)
        for product in text:
            cur.execute("Insert into Avito_product values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                        product['Название товара'], product['Ссылка на товар'], product['Цена'], product['Цена в евро'],
                        product['Категория товара'], product['Описание товара'], product['Фото'],
                        product['Адрес'], product['Имя владельца']))
            conn.commit()


def download_to_xlsx():
    with open('avito/avito_products.json', 'r', encoding='UTF-8') as file:
        text = json.load(file)

        workbook = xlsxwriter.Workbook('avito/data.xlsx')
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0
        for key in text[0].keys():
            worksheet.write(row, col, key)
            col += 1
        for product in text:
            row += 1
            col = 0
            for key in product.keys():
                worksheet.write(row, col, product[key])
                col += 1
        workbook.close()


if __name__ == '__main__':
    # create_db()
    # commit_db()
    download_to_xlsx()
