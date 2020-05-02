import os
import csv

directory = 'output'
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
        with open(file=path, encoding='utf-8') as reader:
            each_result = list(csv.reader(reader))[1:]
            available.extend(each_result)

print('Total: ', len(total))
print('Available: ', len(available))
# write_csv(lines=total, filename='Total.csv')
