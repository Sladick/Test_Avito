from requests import request


def get_euro():
    req = request(url='https://www.cbr-xml-daily.ru/latest.js', method='GET')
    info = req.json()
    euro = float(info['rates']['EUR'])
    return euro


if __name__ == '__main__':
    get_euro()