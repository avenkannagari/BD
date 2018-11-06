import json
import csv
import pandas as pd

#Read source_data.json file
str_data = open('source_data.json').read()
json_data = json.loads(str_data)

#json list variables
json_npi_lst = []
json_name_addr_lst = []
json_practice_lst = []

for entry in json_data:
# Read the JSON file to get NPI for each dotor
    json_npi_lst.append(entry["doctor"].get("npi"))
# Read the JSON file to get first name + last name + practice full address for each dotor
    for each_practice in entry["practices"]:
        json_name_addr_lst.append(entry["doctor"].get("first_name").lower() + " " + entry["doctor"].get("last_name").lower() + " " +
                                   each_practice.get("street").lower() + " " + each_practice.get("street_2").lower() + " " +
                                   each_practice.get("zip") + " " + each_practice.get("city").lower() + " " + each_practice.get("state").lower())
# Read the JSON file to get practice full address
        json_practice_lst.append(each_practice.get("street").lower() + " " + each_practice.get("street_2").lower() + " " +
                               each_practice.get("zip") + " " + each_practice.get("city").lower() + " " + each_practice.get("state").lower())

#Read match_file.csv file
csv_data = pd.read_csv('match_file.csv')
#Replace space with " "
new_csv = csv_data.fillna(" ")
#create a new file new_match_file.csv
new_csv.to_csv('new_match_file.csv',index=False)
ifile  = open('new_match_file.csv')
readCSV = csv.reader(ifile)
#Skip the header row
next(readCSV)

#csv list variables
csv_npi_lst = []
csv_name_addr_lst = []
csv_practice_lst = []

for row in readCSV:
# Read the CSV data to get NPI for each dotor
        csv_npi_lst.append(row[2])
# Read the JSON file to get first name + last name + full address for each dotor
        csv_name_addr_lst.append(row[0].lower() + " " + row[1].lower() + " " + row[3].lower()+ " " + row[4].lower() + " " + row[7] + " " + row[5].lower() + " " + row[6].lower())
# Read the JSON file to get practice full address for each dotor
        csv_practice_lst.append(row[3].lower()+ " " + row[4].lower() + " " + row[7] + " " + row[5].lower() + " " + row[6].lower())

# of Doctors matched with NPI
npi_match = []
no_npi_match = []
for each_npi in json_npi_lst:
    if each_npi in csv_npi_lst: npi_match.append(each_npi)
    else: no_npi_match.append(each_npi)

# of Doctors matched with name and address
name_addr_match = []
no_name_addr_match = []
for each_doctor in json_name_addr_lst:
    if each_doctor in csv_name_addr_lst: name_addr_match.append(each_doctor)
    else: no_name_addr_match.append(each_doctor)

# of Practice matched with address
practice_match = []
no_practice_match = []
for each_practice in json_practice_lst:
    if each_practice in csv_practice_lst: practice_match.append(each_practice)
    else: no_practice_match.append(each_practice)

print("# of total documents scanned:" ,len(json_data))
print("# of Doctors matched with NPI:" ,len(npi_match))
print('# of Doctors matched with name and address:' , len(name_addr_match))
print('# of Practice matched with address:' ,len(practice_match))
print("# of Doctors not matched with NPI:" ,len(no_npi_match))
print('# of Doctors not matched with name and address:' , len(no_name_addr_match))
print('# of Practice not matched with address:' ,len(no_practice_match))
