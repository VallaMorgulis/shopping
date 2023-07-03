import requests
import csv
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    products = soup.find_all('div', class_='catalog__product')
    for product in products:
        name = product.find('div', class_='product-item__link').text
        price = product.find('div', class_='product-item-price').text.replace(' ', '')
        image = product.find('div', class_='product-item__content').find('a').find('picture').find('img').get(
            'data-src')
        image = 'https:' + image

        item = {
            'Name': name,
            'Price': price,
            'Image': image
        }

        data.append(item)

    return data

# def parse_and_save_data(request):
#     # Парсинг данных с использованием BeautifulSoup
#     # ...
#
#     # Создание экземпляра модели и заполнение его данными
#     my_model = MyModel()
#     my_model.field1 = parsed_data['field1']
#     my_model.field2 = parsed_data['field2']
#     # ...
#
#     # Сохранение экземпляра модели в базу данных
#     my_model.save()
#
#     return render(request, 'success.html')

def save_to_csv(data):
    with open('ekobambuk.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Price', 'Image'])
        for item in data:
            writer.writerow([item['Name'], item['Price'], item['Image']])

    print('Данные сохранены в файл ekobambuk.csv')


def main():
    url = 'https://ekobambuk.ru/products/category/bambukovye-polotenca?page=1'
    html = get_html(url)
    data = parse_page(html)
    print(data)
    save_to_csv(data)


if __name__ == '__main__':
    main()
