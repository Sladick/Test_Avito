import time
from bs4 import BeautifulSoup
import json
from get_euro import get_euro

price_euro = get_euro()
start_time = time.time()
headers = {
    'Accep': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',

}
# for i in range(1, 101):
#     url = f'https://www.avito.ru/novosibirsk/bytovaya_elektronika?p={i}'
#     req = requests.get(url=url, headers=headers)
#     src = req.text
#     with open(f'avito/url_html/tovar{i}.html', "w", encoding='UTF-8') as file:
#         file.write(src)


info_products = []
for i in range(1, 101):
    with open(f'avito/url_html/tovar{i}.html', encoding='UTF-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    products_url = soup.find_all('div', class_='iva-item-root-Nj_hb')
    for product in products_url:
        try:
            product_url = 'https://www.avito.ru/' + product.find('a', class_='link-link-MbQDP').get('href')
        except:
            product_url = 'нету url'
        try:
            product_name = product.find('h3', class_='title-root-j7cja').text.strip()
        except:
            product_name = 'нет имени'
        try:
            product_price = product.find('span', class_='price-text-E1Y7h').text.strip('₽').split()
            product_price = int(''.join(product_price))
        except:
            product_price = 0
        try:
            product_description = product.find('div', class_='iva-item-text-_s_vh').text.strip()
            rep = [" ", '\n']
            for item in rep:
                if item in product_description:
                    product_description = product_description.replace(item, "")
        except:
            product_description = 'нет описания'
        try:
            product_category = product.find('span', class_='iva-item-text-_s_vh').text.strip()
        except:
            product_category = 'нету категории'
        try:
            product_address = product.find('div', class_='geo-georeferences-Yd_m5').text.split(',')[0]
        except:
            product_address = 'нету адреса'
        try:
            product_owner_name = product.find('div', class_='styles-root-JMoCE').text
        except:
            product_owner_name = 'нет имени'
        try:
            product_img = product.find('img', class_='photo-slider-image-_Dc4I').get('src')
        except:
            product_img = 'нет фото'

        info_products.append(
            {
                'Название товара': product_name,
                'Ссылка на товар': product_url,
                'Цена': product_price,
                'Цена в евро': round(product_price*price_euro, 2),
                'Категория товара': product_category,
                'Описание товара': product_description,
                'Фото': product_img,
                'Адрес': product_address,
                'Имя владельца': product_owner_name
            }
        )
    print(f'Обработано {i} из 100 страниц')
with open(f"avito/avito_products.json", "a", encoding="utf-8") as file:
        json.dump(info_products, file, indent=4, ensure_ascii=False)

finish_time = time.time() - start_time
print(f"Затраченное на работу скрипта время: {finish_time}")

