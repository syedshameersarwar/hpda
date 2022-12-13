import sys

filename = sys.argv[1]

with open(filename, 'r') as file:
    lines = file.readlines()

data = []
for line in lines:
    data.append(line.strip().split(','))

means = []
for col_index in range(len(data[0])):
    total = 0
    for row in data[1:]:
        total += float(row[col_index])
    mean = total / len(data[1:])
    means.append(mean)

print(means)
