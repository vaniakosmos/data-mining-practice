reader = open("./datasets/balance-scale.csv", 'r')
writer = open("./datasets/balance.csv", 'w')

for line in reader:
    row = line.split(",")
    row[-1] = row[-1][0]  # delete `\n`
    row = ",".join(row[1:] + [row[0]])
    writer.write(row + '\n')
