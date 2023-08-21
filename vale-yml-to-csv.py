import os
import yaml
import csv

input_dir = './vale/styles/MongoDB'
output_filename = 'output.csv'

data_list = []

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.yml'):
            with open(os.path.join(root, file), 'r') as f:
                data = yaml.safe_load(f)
                data['filename'] = file
                data_list.append(data)

fieldnames = set()
for item in data_list:
    fieldnames.update(item.keys())

with open(output_filename, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for data_item in data_list:
        writer.writerow({key: value for key, value in data_item.items()})

