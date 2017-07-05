from pprint import pprint

res = []
name = 'test'

classes = [
        'Математичний аналiз, диференцiальнi рiвняння',
        'Алгебра та геометрія, дослідження операцій',
        'Математична логіка та Дискретна математика',
        'Програмування'
]

with open(f'{name}.txt') as file:
    lines = file.readlines()
    offset = 0

    for c in range(2):
        clas = lines[offset].strip()
        count = int(lines[offset+1])
        for i in range(count):
            res.append(str(classes.index(clas)) + " " + lines[offset + i + 2])
        offset += count + 3

with open(f'{name}1.txt', 'w') as file:
    for r in res:
        file.write(r)
