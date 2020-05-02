import requests
import os
import csv
from bs4 import BeautifulSoup
import random
from requests.exceptions import ConnectionError


csv_header = [['NAME', 'ADDRESS', 'PHONE NUMBER', 'IP ADDRESS', 'ESTIMATED INCOME', 'OCCUPATION', 'AGE']]


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


def write_success_phones(lines):
    filename = 'success_phones.csv'
    with open('output/%s' % filename, 'a', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)
    csv_file.close()


def read_success_phones():
    file = 'output/success_phones.csv'
    phone = []
    with open(file=file, encoding='utf-8') as reader:
        rows = reader.readlines()
        for row in rows:
            phone.append(row.strip())
    return phone


def phones():
    path = 'AZ_29k_25_05.txt'
    f = open(path, "r+")
    p_numbers = f.readlines()
    f.close()
    return p_numbers


def get_proxies():
    url = "http://list.didsoft.com/get?email=developer61510@gmail.com&pass=mv3asy&pid=http3000&showcountry=no"
    res = requests.get(url=url).text.split('\n')
    return res


def check_ip(rand):
    url = 'https://httpbin.org/ip'
    print(url)
    proxy = {
        'http': 'http://{}'.format(rand),
        'https': 'https://{}'.format(rand)
    }
    try:
        response = requests.get(url=url, proxies=proxy)
        print('This is response url: ', response.text.strip())
        return proxy
    except ConnectionError as e:
        print(e, 'Trying another proxy')
        return None


def request(number):
    # proxies = get_proxies()
    # while True:
    #     rand = random.choice(proxies)
    #     check = check_ip('176.110.154.59:53499')
    #     print('here: ', check)
    #     if check is not None:
    #         break
    name, address, ip, income, occupation, age = '', '', '', '', '', ''
    results = []
    req_number = '{}-{}-{}'.format(number[1:4], number[4:7], number[7:11])
    url = 'https://thatsthem.com/phone/{}'.format(req_number)
    response = requests.get(url=url)
    if response.url == 'https://thatsthem.com/?rl=true':
        print('Proxy Terminated')
        exit()
    soup = BeautifulSoup(response.text, 'html5lib')
    cards = soup.find_all(attrs={'class': 'ThatsThem-record'})
    for card in cards:
        if card.find(attrs={'itemprop': "name"}):
            name = card.find(attrs={'itemprop': "name"}).text.strip()
            if card.find(attrs={'itemprop': "address"}):
                address = card.find(attrs={'itemprop': "address"}).text.strip()
            if card.find('dt', text="Occupation"):
                occupation = card.find('dt', text="Occupation").find_next('dd').text.strip()
            if card.find('dt', text="Estimated Income"):
                income = card.find('dt', text="Estimated Income").find_next('dd').text.strip()
            if card.find('dt', text="IP Address"):
                ip = card.find('dt', text="IP Address").find_next('dd').text.strip()
            if card.find(attrs={'class': 'ThatsThem-record-age'}) and card.find(attrs={'class': 'ThatsThem-record-age'}).find('span', {'class': 'active'}):
                age = card.find(attrs={'class': 'ThatsThem-record-age'}).find('span', {'class': 'active'}).text.strip()
            row = [name, address, number, ip, income, occupation, age]
            results.append(row)
    return results


def main():
    success_numbers = read_success_phones()
    phone_numbers = phones()
    for p in phone_numbers:
        phone_number = p.strip()
        if phone_number in success_numbers:
            print('Exist')
            continue
        response = request(number=phone_number)
        write_success_phones([[phone_number]])
        if response:
            write_csv(lines=response, filename='Result.csv')
            print(response)


if __name__ == '__main__':
    main()
