import threading
import json
import requests
import time
from requests.exceptions import ConnectTimeout, ConnectionError
from datetime import datetime
from bs4 import BeautifulSoup
import os
import csv
traffic_size = 0
proxy_requests_count = 0
pass_records = 0
success_records = 0
failed_records = 0
start_time = time.time()
csv_header = [['NAME', 'ADDRESS', 'PHONE NUMBER', 'IP ADDRESS', 'ESTIMATED INCOME', 'OCCUPATION', 'AGE']]


class myThread(threading.Thread):
    def __init__(self, threadID, phone_list, file_name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.phone_list = phone_list
        self.file_name = file_name

    def run(self):
        print("Starting to working on {} thread ".format(self.threadID))
        rotate(self.phone_list, self.file_name)


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


def write_phones(lines, file_name):
    with open('output/%s' % file_name, 'a', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)
    csv_file.close()


def read_pass_phones():
    file = 'output/pass_phones.csv'
    if not os.path.isfile(file):
        write_phones(lines=[[]], file_name='pass_phones.csv')
    phone = []
    with open(file=file, encoding='utf-8') as reader:
        rows = reader.readlines()
        for row in rows:
            phone.append(row.strip())
    return phone


def rotate(phone_list, file):
    global pass_records
    global failed_records
    global success_records
    global traffic_size
    proxy = get_proxy()
    read_phones = read_pass_phones()
    read_phones_len = len(read_phones)
    for p in phone_list:
        flag = True
        phone = p[0]
        if phone in read_phones:
            continue
        while flag:
            that_res = thread_run(phone, proxy)
            if that_res is not None:
                name, address, ip, income, occupation, age = '', '', '', '', '', ''
                results = []
                try:
                    if that_res.url == 'https://thatsthem.com/?rl=true':
                        proxy = get_proxy()
                        print('Proxy Terminated')
                        continue
                    pass_records += 1
                    print('Total records: ', pass_records + read_phones_len, ', Success records: ', success_records + 1,
                          ', Total traffic size: ', traffic_size, ', Failed records: ', failed_records, proxy)
                    write_phones(lines=[[phone]], file_name='pass_phones.csv')
                    soup = BeautifulSoup(that_res.text, 'html5lib')
                    cards = soup.find_all(attrs={'class': 'ThatsThem-record'})
                    if not cards:
                        print('Success, but We did not find the data.')
                        write_csv(lines=[[phone]], filename='Not_Found.csv')
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
                            if card.find(attrs={'class': 'ThatsThem-record-age'}) and card.find(
                                    attrs={'class': 'ThatsThem-record-age'}).find('span', {'class': 'active'}):
                                age = card.find(attrs={'class': 'ThatsThem-record-age'}).find('span', {
                                    'class': 'active'}).text.strip()
                            row = [name, address, phone, ip, income, occupation, age]
                            print(row)
                            results.append(row)
                    success_records += 1
                except Exception as e:
                    failed_records += 1
                    write_phones(lines=[[phone]], file_name='failed_phones.csv')
                write_csv(lines=results, filename=file)
                flag = False
            else:
                proxy = get_proxy()


def thread_run(number, proxy, retry_count=0):
    global traffic_size
    print('Current Number: ', number, ', Current Proxy: ', proxy, ', Trying Count: ', retry_count)
    try:
        req_number = '{}-{}-{}'.format(number[1:4], number[4:7], number[7:11])
        url = 'https://thatsthem.com/phone/{}'.format(req_number)
        res = requests.get(url=url, proxies=proxy)
        # res = requests.get(url=url)
        traffic_size += len(res.content)
        print('Once traffic size: ', len(res.content), '')
        return res
    except Exception as e:
        if retry_count == 2:
            return None
        return thread_run(number=number, proxy=proxy, retry_count=retry_count + 1)


def get_proxy():
    global proxy_requests_count
    proxy_requests_count += 1
    try:
        url = 'http://falcon.proxyrotator.com:51337/'
        params = dict(
            apiKey='qngGXNmhAkM7634trSxLeuyDwKQcJdRb'
        )
        resp = requests.get(url=url, params=params)
        print('Proxy request count: ', proxy_requests_count, ', Passed time: ', time.time() - start_time)
        if resp.status_code == 200:
            json_data = json.loads(resp.text)
            if 'error' in json_data:
                print(json_data['error'])
                time.sleep(3600 - (time.time()-start_time))
                return get_proxy()
            elif 'proxy' in json_data:
                # available_proxy = check_ip(json_data['proxy'])
                # if available_proxy is not None:
                success_proxy = {
                    'http': 'http://{}'.format(json_data['proxy']),
                    'https': 'https://{}'.format(json_data['proxy'])
                }
                return success_proxy
        else:
            time.sleep(3)
            return get_proxy()
    except ConnectionError as e:
        time.sleep(10)
        return get_proxy()


def check_ip(rand):
    url = 'https://httpbin.org/ip'
    proxy = {
        'http': 'http://{}'.format(rand),
        'https': 'https://{}'.format(rand)
    }
    try:
        ip_res = requests.get(url=url, proxies=proxy)
        print('Traffic size for ip check: ', len(ip_res.content))
        return proxy
    except ConnectionError as e:
        print('Failed in checking proxy ip: ', e)
        return None


def source(path):
    with open(file=path, encoding='utf-8') as reader:
        p_numbers = list(csv.reader(reader))[1:]
    number_list = []
    i = len(p_numbers) // 100 + 1
    for j in range(100):
        number_list.append(p_numbers[j * i:(j + 1) * i])
    return number_list


if __name__ == '__main__':
    date = datetime.today().strftime('%Y_%m_%d')
    thread_number_list = source(path='source/TOSCB 1M_1.csv')

    threads = []

    # Create new threads
    thread1 = myThread(1, thread_number_list[0], '{}_1.csv'.format(date))
    thread2 = myThread(2, thread_number_list[1], '{}_2.csv'.format(date))
    thread3 = myThread(3, thread_number_list[2], '{}_3.csv'.format(date))
    thread4 = myThread(4, thread_number_list[3], '{}_4.csv'.format(date))
    thread5 = myThread(5, thread_number_list[4], '{}_5.csv'.format(date))
    thread6 = myThread(6, thread_number_list[5], '{}_6.csv'.format(date))
    thread7 = myThread(7, thread_number_list[6], '{}_7.csv'.format(date))
    thread8 = myThread(8, thread_number_list[7], '{}_8.csv'.format(date))
    thread9 = myThread(9, thread_number_list[8], '{}_9.csv'.format(date))
    thread10 = myThread(10, thread_number_list[9], '{}_10.csv'.format(date))
    thread11 = myThread(11, thread_number_list[10], '{}_11.csv'.format(date))
    thread12 = myThread(12, thread_number_list[11], '{}_12.csv'.format(date))
    thread13 = myThread(13, thread_number_list[12], '{}_13.csv'.format(date))
    thread14 = myThread(14, thread_number_list[13], '{}_14.csv'.format(date))
    thread15 = myThread(15, thread_number_list[14], '{}_15.csv'.format(date))
    thread16 = myThread(16, thread_number_list[15], '{}_16.csv'.format(date))
    thread17 = myThread(17, thread_number_list[16], '{}_17.csv'.format(date))
    thread18 = myThread(18, thread_number_list[17], '{}_18.csv'.format(date))
    thread19 = myThread(19, thread_number_list[18], '{}_19.csv'.format(date))
    thread20 = myThread(20, thread_number_list[19], '{}_20.csv'.format(date))
    thread21 = myThread(21, thread_number_list[20], '{}_21.csv'.format(date))
    thread22 = myThread(22, thread_number_list[21], '{}_22.csv'.format(date))
    thread23 = myThread(23, thread_number_list[22], '{}_23.csv'.format(date))
    thread24 = myThread(24, thread_number_list[23], '{}_24.csv'.format(date))
    thread25 = myThread(25, thread_number_list[24], '{}_25.csv'.format(date))
    thread26 = myThread(26, thread_number_list[25], '{}_26.csv'.format(date))
    thread27 = myThread(27, thread_number_list[26], '{}_27.csv'.format(date))
    thread28 = myThread(28, thread_number_list[27], '{}_28.csv'.format(date))
    thread29 = myThread(29, thread_number_list[28], '{}_29.csv'.format(date))
    thread30 = myThread(30, thread_number_list[29], '{}_30.csv'.format(date))
    thread31 = myThread(31, thread_number_list[30], '{}_31.csv'.format(date))
    thread32 = myThread(32, thread_number_list[31], '{}_32.csv'.format(date))
    thread33 = myThread(33, thread_number_list[32], '{}_33.csv'.format(date))
    thread34 = myThread(34, thread_number_list[33], '{}_34.csv'.format(date))
    thread35 = myThread(35, thread_number_list[34], '{}_35.csv'.format(date))
    thread36 = myThread(36, thread_number_list[35], '{}_36.csv'.format(date))
    thread37 = myThread(37, thread_number_list[36], '{}_37.csv'.format(date))
    thread38 = myThread(38, thread_number_list[37], '{}_38.csv'.format(date))
    thread39 = myThread(39, thread_number_list[38], '{}_39.csv'.format(date))
    thread40 = myThread(40, thread_number_list[39], '{}_40.csv'.format(date))
    thread41 = myThread(41, thread_number_list[40], '{}_41.csv'.format(date))
    thread42 = myThread(42, thread_number_list[41], '{}_42.csv'.format(date))
    thread43 = myThread(43, thread_number_list[42], '{}_43.csv'.format(date))
    thread44 = myThread(44, thread_number_list[43], '{}_44.csv'.format(date))
    thread45 = myThread(45, thread_number_list[44], '{}_45.csv'.format(date))
    thread46 = myThread(46, thread_number_list[45], '{}_46.csv'.format(date))
    thread47 = myThread(47, thread_number_list[46], '{}_47.csv'.format(date))
    thread48 = myThread(48, thread_number_list[47], '{}_48.csv'.format(date))
    thread49 = myThread(49, thread_number_list[48], '{}_49.csv'.format(date))
    thread50 = myThread(50, thread_number_list[49], '{}_50.csv'.format(date))
    thread51 = myThread(51, thread_number_list[50], '{}_51.csv'.format(date))
    thread52 = myThread(52, thread_number_list[51], '{}_52.csv'.format(date))
    thread53 = myThread(53, thread_number_list[52], '{}_53.csv'.format(date))
    thread54 = myThread(54, thread_number_list[53], '{}_54.csv'.format(date))
    thread55 = myThread(55, thread_number_list[54], '{}_55.csv'.format(date))
    thread56 = myThread(56, thread_number_list[55], '{}_56.csv'.format(date))
    thread57 = myThread(57, thread_number_list[56], '{}_57.csv'.format(date))
    thread58 = myThread(58, thread_number_list[57], '{}_58.csv'.format(date))
    thread59 = myThread(59, thread_number_list[58], '{}_59.csv'.format(date))
    thread60 = myThread(60, thread_number_list[59], '{}_60.csv'.format(date))
    thread61 = myThread(61, thread_number_list[60], '{}_61.csv'.format(date))
    thread62 = myThread(62, thread_number_list[61], '{}_62.csv'.format(date))
    thread63 = myThread(63, thread_number_list[62], '{}_63.csv'.format(date))
    thread64 = myThread(64, thread_number_list[63], '{}_64.csv'.format(date))
    thread65 = myThread(65, thread_number_list[64], '{}_65.csv'.format(date))
    thread66 = myThread(66, thread_number_list[65], '{}_66.csv'.format(date))
    thread67 = myThread(67, thread_number_list[66], '{}_67.csv'.format(date))
    thread68 = myThread(68, thread_number_list[67], '{}_68.csv'.format(date))
    thread69 = myThread(69, thread_number_list[68], '{}_69.csv'.format(date))
    thread70 = myThread(70, thread_number_list[69], '{}_70.csv'.format(date))
    thread71 = myThread(71, thread_number_list[70], '{}_71.csv'.format(date))
    thread72 = myThread(72, thread_number_list[71], '{}_72.csv'.format(date))
    thread73 = myThread(73, thread_number_list[72], '{}_73.csv'.format(date))
    thread74 = myThread(74, thread_number_list[73], '{}_74.csv'.format(date))
    thread75 = myThread(75, thread_number_list[74], '{}_75.csv'.format(date))
    thread76 = myThread(76, thread_number_list[75], '{}_76.csv'.format(date))
    thread77 = myThread(77, thread_number_list[76], '{}_77.csv'.format(date))
    thread78 = myThread(78, thread_number_list[77], '{}_78.csv'.format(date))
    thread79 = myThread(79, thread_number_list[78], '{}_79.csv'.format(date))
    thread80 = myThread(80, thread_number_list[79], '{}_80.csv'.format(date))
    thread81 = myThread(81, thread_number_list[80], '{}_81.csv'.format(date))
    thread82 = myThread(82, thread_number_list[81], '{}_82.csv'.format(date))
    thread83 = myThread(83, thread_number_list[82], '{}_83.csv'.format(date))
    thread84 = myThread(84, thread_number_list[83], '{}_84.csv'.format(date))
    thread85 = myThread(85, thread_number_list[84], '{}_85.csv'.format(date))
    thread86 = myThread(86, thread_number_list[85], '{}_86.csv'.format(date))
    thread87 = myThread(87, thread_number_list[86], '{}_87.csv'.format(date))
    thread88 = myThread(88, thread_number_list[87], '{}_88.csv'.format(date))
    thread89 = myThread(89, thread_number_list[88], '{}_89.csv'.format(date))
    thread90 = myThread(90, thread_number_list[89], '{}_90.csv'.format(date))
    thread91 = myThread(91, thread_number_list[90], '{}_91.csv'.format(date))
    thread92 = myThread(92, thread_number_list[91], '{}_92.csv'.format(date))
    thread93 = myThread(93, thread_number_list[92], '{}_93.csv'.format(date))
    thread94 = myThread(94, thread_number_list[93], '{}_94.csv'.format(date))
    thread95 = myThread(95, thread_number_list[94], '{}_95.csv'.format(date))
    thread96 = myThread(96, thread_number_list[95], '{}_96.csv'.format(date))
    thread97 = myThread(97, thread_number_list[96], '{}_97.csv'.format(date))
    thread98 = myThread(98, thread_number_list[97], '{}_98.csv'.format(date))
    thread99 = myThread(99, thread_number_list[98], '{}_99.csv'.format(date))
    thread100 = myThread(100, thread_number_list[99], '{}_100.csv'.format(date))

    # Start new Threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()
    thread9.start()
    thread10.start()
    thread11.start()
    thread12.start()
    thread13.start()
    thread14.start()
    thread15.start()
    thread16.start()
    thread17.start()
    thread18.start()
    thread19.start()
    thread20.start()
    thread21.start()
    thread22.start()
    thread23.start()
    thread24.start()
    thread25.start()
    thread26.start()
    thread27.start()
    thread28.start()
    thread29.start()
    thread30.start()
    thread31.start()
    thread32.start()
    thread33.start()
    thread34.start()
    thread35.start()
    thread36.start()
    thread37.start()
    thread38.start()
    thread39.start()
    thread40.start()
    thread41.start()
    thread42.start()
    thread43.start()
    thread44.start()
    thread45.start()
    thread46.start()
    thread47.start()
    thread48.start()
    thread49.start()
    thread50.start()
    thread51.start()
    thread52.start()
    thread53.start()
    thread54.start()
    thread55.start()
    thread56.start()
    thread57.start()
    thread58.start()
    thread59.start()
    thread60.start()
    thread61.start()
    thread62.start()
    thread63.start()
    thread64.start()
    thread65.start()
    thread66.start()
    thread67.start()
    thread68.start()
    thread69.start()
    thread70.start()
    thread71.start()
    thread72.start()
    thread73.start()
    thread74.start()
    thread75.start()
    thread76.start()
    thread77.start()
    thread78.start()
    thread79.start()
    thread80.start()
    thread81.start()
    thread82.start()
    thread83.start()
    thread84.start()
    thread85.start()
    thread86.start()
    thread87.start()
    thread88.start()
    thread89.start()
    thread90.start()
    thread91.start()
    thread92.start()
    thread93.start()
    thread94.start()
    thread95.start()
    thread96.start()
    thread97.start()
    thread98.start()
    thread99.start()
    thread100.start()

    # Add threads to thread list
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    threads.append(thread4)
    threads.append(thread5)
    threads.append(thread6)
    threads.append(thread7)
    threads.append(thread8)
    threads.append(thread9)
    threads.append(thread10)
    threads.append(thread11)
    threads.append(thread12)
    threads.append(thread13)
    threads.append(thread14)
    threads.append(thread15)
    threads.append(thread16)
    threads.append(thread17)
    threads.append(thread18)
    threads.append(thread19)
    threads.append(thread20)
    threads.append(thread21)
    threads.append(thread22)
    threads.append(thread23)
    threads.append(thread24)
    threads.append(thread25)
    threads.append(thread26)
    threads.append(thread27)
    threads.append(thread28)
    threads.append(thread29)
    threads.append(thread30)
    threads.append(thread31)
    threads.append(thread32)
    threads.append(thread33)
    threads.append(thread34)
    threads.append(thread35)
    threads.append(thread36)
    threads.append(thread37)
    threads.append(thread38)
    threads.append(thread39)
    threads.append(thread40)
    threads.append(thread41)
    threads.append(thread42)
    threads.append(thread43)
    threads.append(thread44)
    threads.append(thread45)
    threads.append(thread46)
    threads.append(thread47)
    threads.append(thread48)
    threads.append(thread49)
    threads.append(thread50)
    threads.append(thread51)
    threads.append(thread52)
    threads.append(thread53)
    threads.append(thread54)
    threads.append(thread55)
    threads.append(thread56)
    threads.append(thread57)
    threads.append(thread58)
    threads.append(thread59)
    threads.append(thread60)
    threads.append(thread61)
    threads.append(thread62)
    threads.append(thread63)
    threads.append(thread64)
    threads.append(thread65)
    threads.append(thread66)
    threads.append(thread67)
    threads.append(thread68)
    threads.append(thread69)
    threads.append(thread70)
    threads.append(thread71)
    threads.append(thread72)
    threads.append(thread73)
    threads.append(thread74)
    threads.append(thread75)
    threads.append(thread76)
    threads.append(thread77)
    threads.append(thread78)
    threads.append(thread79)
    threads.append(thread80)
    threads.append(thread81)
    threads.append(thread82)
    threads.append(thread83)
    threads.append(thread84)
    threads.append(thread85)
    threads.append(thread86)
    threads.append(thread87)
    threads.append(thread88)
    threads.append(thread89)
    threads.append(thread90)
    threads.append(thread91)
    threads.append(thread92)
    threads.append(thread93)
    threads.append(thread94)
    threads.append(thread95)
    threads.append(thread96)
    threads.append(thread97)
    threads.append(thread98)
    threads.append(thread99)
    threads.append(thread100)

    # thread1 = myThread(1, thread_number_list[0], '{}_1.csv'.format(date))
    # thread1.start()
    # threads.append(thread1)

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print("Exiting Main Thread")
