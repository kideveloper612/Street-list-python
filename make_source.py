import os
import csv


def read_source():
    global source
    file = open(source, 'r')
    rows = list(csv.reader(file))
    file.close()
    return rows


def get_individaul_source(individual):
    csv_source = read_source()
    result = []
    for i in csv_source:
        if individual in i[0]:
            result.append(i[1])
    return result


def add_letters(p):
    l = 4 - len(p)
    tmp = '0000'
    return '{}{}'.format(tmp[:l], p)


def write_csv(lines, filename):
    global source_folder
    if not os.path.isdir(source_folder):
        os.mkdir(source_folder)
    file = open(os.path.join(source_folder, filename), 'w')
    file.writelines(lines)
    file.close()


def make_phone(pre):
    global purpose
    for p in range(10000):
        if len(str(p)) < 4:
            p = add_letters(str(p))
        phone = purpose + pre + str(p)
        total.append(phone + '\n')


def find_condition(f_pre, s_pre):
    global total_list
    for t in total_list:
        if f_pre in t and s_pre in t:
            return t[2]


def main():
    ind_list = get_individaul_source(purpose)
    for prefix in ind_list:
        t_value = find_condition(f_pre=purpose, s_pre=prefix)
        if int(t_value) > 3000:
            make_phone(prefix)


def get_prefix():
    global source
    file = open(source, 'r')
    rows = list(csv.reader(file))
    file.close()
    array = []
    for i in rows:
        array.append(i[0])
    return list(set(array))


def get_total_list():
    global total_list
    file = open(source, 'r')
    rows = list(csv.reader(file))
    file.close()
    return rows


if __name__ == '__main__':
    source_folder = 'Source'
    source = 'Result.csv'
    prefixs = get_prefix()
    total_list = get_total_list()
    total = []
    for pre in prefixs:
        purpose = pre
        main()
    for i in range(len(total) // 500000 + 1):
        write_csv(lines=total[i*500000:(i+1)*500000], filename='{}.txt'.format(i+1))

