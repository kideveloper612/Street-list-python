import requests
import csv
import time
from bs4 import BeautifulSoup
import os

csv_header = [['Store Address', 'Title', 'Alexa', 'Theme', 'Country']]


def write_direct_csv(lines, filename):
    """
    Write real data on csv file
    :param lines: records for writing
    :param filename: file name for saving
    :return:
    """
    with open('output/%s' % filename, 'a', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)
    csv_file.close()


def write_csv(lines, filename):
    """
    Call write_direct_csv function
    :param lines: records for writing
    :param filename: file name for saving
    :return:
    """
    if not os.path.isdir('output'):
        os.mkdir('output')
    if not os.path.isfile('output/%s' % filename):
        write_direct_csv(lines=csv_header, filename=filename)
    write_direct_csv(lines=lines, filename=filename)


def get_data(url):
    res = requests.get(url=url)
    try:
        if res.status_code == 200:
            return res.text
        else:
            return None
    except ConnectionError as e:
        time.sleep(5)
        return get_data(url=url)

def main():
    base_url = 'https://www.shopistores.com/shopify-theme-testament/'
    flag = True
    page = 0
    while flag:
        page += 1
        url = base_url + str(page)
        response = get_data(url=url)
        if response is not None:
            soup = BeautifulSoup(response, 'html5lib')
            soup_records = soup.select('table.table tbody tr')
            for soup_record in soup_records:
                address = soup_record.find('td', attrs={'data-title': 'Store Address'}).a['href']
                title = soup_record.find('td', attrs={'data-title': 'Title'}).text.strip()
                rank = soup_record.find('td', attrs={'data-title': 'Alexa Rank'}).text.strip()
                selling = soup_record.find('td', attrs={'data-title': 'Theme'}).text.strip()
                country = soup_record.find('td', attrs={'data-title': 'Country'}).text.strip()
                line = [address, title, rank, selling, country]
                print(line)
                write_csv(lines=[line], filename='theme_testament.csv')
        else:
            flag = False


if __name__ == "__main__":
    print('----------- Start -------------')
    main()
    print('----------- The End -----------')