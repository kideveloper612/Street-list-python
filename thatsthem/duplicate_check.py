import os

f = open(file='IT_1MM_30_04.txt')
rows = f.readlines()
f.close()

available = []
dup = []
total_count = len(rows)
for row in rows:
    if 'Msisdn' in row:
        continue
    phone = row.strip()
    print(total_count, len(available), len(dup))
    if phone not in available:
        available.append(phone)
        continue
    elif phone not in dup:
        dup.append(phone)
        continue


print('Total Count: ', total_count-1)
print('Available: ', len(available))
print('Duplicated Count: ', len(dup))
# for d in dup:
#     print(d)

