import os
import csv

# directory = 'F:\\working\\python\\scrapping\\Location_Marco\\result\\DELIVERY_EB_1_05'
directory = 'F:\\working\\python\\scrapping\\Location_Marco\\Newly\\TOSCB_1M_2\\M1_2'
# directory = 'F:\\working\\python\\scrapping\\Location_Marco\\thatsthem\\output'

total = []
available = []

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


for file in os.listdir(directory):
    if 'Not' in file:
        continue
    elif 'phones' in file:
        path = os.path.join(directory, file)
        with open(file=path, encoding='utf-8') as reader:
            each_result = list(csv.reader(reader))[1:]
            total.extend(each_result)
    else:
        path = os.path.join(directory, file)
        print(path)
        with open(file=path, encoding='utf-8') as reader:
            try:
                each_result = list(csv.reader(reader))[1:]
                # for e in each_result:
                    # if e not in available:
                        # available.append(each_result)
                available.extend(each_result)
            except:
                continue

print('Total: ', len(total))
print('Available: ', len(available))
# write_csv(lines=available, filename='TOSCB_1M_1.csv')
