import requests
from bs4 import BeautifulSoup
import os
import csv


csv_header = [['NAME', 'ADDRESS', 'PHONE']]


def write_direct_csv(lines, filename):
    with open('output/%s' % filename, 'a', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)
    csv_file.close()


def write_csv(lines, filename):
    if not os.path.isdir('output'):
        os.mkdir('output')
    if not os.path.isfile('output/%s' % filename):
        write_direct_csv(lines=csv_header, filename=filename)
    write_direct_csv(lines=lines, filename=filename)


def main():
    count = 0
    for page in range(1804):
        url = 'https://www.locatefamily.com/Street-Lists/United-States-of-America/index-{}.html'.format(str(page + 1))
        print(url)
        res = requests.request(method='GET', url=url).text
        soup = BeautifulSoup(res, 'html5lib')
        rows = soup.find_all('li', {'class': 'list-group-item'})
        for row in rows:
            address, name, phone = '', '', ''
            address_d = row.find('li', attrs={'itemprop': "address"})
            givenName_d = row.find(attrs={'itemprop': "givenName"})
            familyName_d = row.find(attrs={'itemprop': "familyName"})
            phone_d = row.find(attrs={'itemprop': "telephone"})
            if address_d:
                address = address_d.text.replace('\n', '').strip()
            if givenName_d and familyName_d:
                name = givenName_d.text.strip() + ' ' + familyName_d.text.strip()
            if phone_d:
                phone = phone_d.text.strip()
            line = [address, name, phone]
            write_csv(lines=[line], filename='USA.csv')
            print(count, line)
            count += 1


if __name__ == '__main__':
    main()