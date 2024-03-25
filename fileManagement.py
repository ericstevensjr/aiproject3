filePath = 'attributes.txt'
with open(filePath, 'r') as file:
    for line in file:
        attribute, values = line.strip().split(':')