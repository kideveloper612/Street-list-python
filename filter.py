import os
import csv
from bs4 import BeautifulSoup as bs
import requests as send
import time


def send_request(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        res = session_request.get(url=url, headers=headers)
        if res is not None:
            return res
        return None
    except Exception as e:
        print(e)
        time.sleep(10)
        return session_request.get(url)



def write_csv(lines, filename):
    with open(filename, 'a', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)


def main():
    global total_count
    global phone_list_count
    response = send_request(base_url)
    if response is not None:
        soup = bs(response.text, 'html5lib')
        states = soup.select('td.area-codes')
        for state in states:
            state_code = state.text.strip()
            state_codes = state_code.split('-')
            for s in state_codes:
                s_code = s.strip()
                state_url = os.path.join(base_url, '+1-{}/'.format(s_code))
                state_res = send_request(state_url)
                if state_res is not None and state_res.status_code == 200:
                    state_soup = bs(state_res.text, 'html5lib')
                    sub_codes = state_soup.select('ul.inline-list.cf a')
                    for sub_code in sub_codes:
                        sub_code_value = sub_code.text.strip()
                        sub_code_url = 'https://numberville.com' + sub_code['href']
                        sub_code_res = send_request(sub_code_url)
                        if sub_code_res is not None and sub_code_res.status_code == 200:
                            sub_code_soup = bs(sub_code_res.text, 'html5lib')
                            stat_list = sub_code_soup.select('.stats-list .color-blue')[0].text.strip()
                            total_count += int(stat_list)
                            phone_list_soup = sub_code_soup.select('.inline-list.cf a')
                            phone_list_count += len(phone_list_soup)
                            line = [s_code, sub_code_value, stat_list]
                            print(total_count, phone_list_count, line)
                            write_csv(lines=[line], filename='Result.csv')


if __name__ == '__main__':
    base_url = 'https://numberville.com/usa/'
    total_count = 0
    phone_list_count = 0
    session_request = send.session()
    main()
    print('total_count: ', total_count)
    print('phone_list: ', phone_list_count)
