import csv
from numpy import ones, dtype, array, NaN
import pandas as pd
from time import time
from pprint import pprint
from collections import defaultdict, Counter
from count_incidents import count_borough_incidents, count_zip_incidents


def write_set( zipset ):
	with open('nyc_zips.txt', 'w') as f:
		for i in zipset:
			f.write(str(i) + "\n")


def write_dict_to_csv( tmp_dict, out_f="output.csv" ):
	with open(out_f, 'w') as f:  # Just use 'w' mode in 3.x
		w = csv.DictWriter(f, tmp_dict.keys())
		w.writeheader()
		w.writerow(tmp_dict)


# MAIN Parsing logic - ending results in CSV created to map Zip Codes, Incident Occurences
def preprocessing_csv( in_f, size, is_zip_root ):
	start_timer = time()
	zip_set = set()

	# Default dict with a collection counter to assist
	master_dict = defaultdict(lambda: defaultdict(lambda: Counter()))

	# Much room for improvement among these parameters
	reader = pd.read_csv(in_f, sep=',', skip_blank_lines=True, memory_map=True, chunksize=size)
	for chunk in reader:
		complaint = str(chunk['Complaint Type'].values[0]).split(",")[0].strip().replace("DOF", '')
		if (is_zip_root):
			zip = str(chunk['Incident Zip'].values[0]).split(",")[0].strip()
			root = zip
		else:
			borough = str(chunk['Borough'].values[0]).strip()
			root = borough

		if ("nan" not in root.lower() and "unspecified" not in root.lower()):
			try:
				if root in zip_set:
					master_dict[root][complaint] += 1
				else:
					master_dict[root] = {complaint: 1}
					zip_set.add((root))
			except KeyError:
				# print("KEY ERROR", master_dict[root])
				# print(root, " ", complaint)
				master_dict[root][complaint] = 1  # print(root, " ", complaint)

		# Refresh Rate of Prints (.5 seconds)
		if time() - start_timer > .5:
			pprint(dict(master_dict))
			start_timer = time()

	# Write dictionary accumulated into csv upon completion of parsing
	if (is_zip_root):
		write_set(zip_set)
		write_dict_to_csv(master_dict)

# Start the function call
def main():
	zip_root = None
	print("\n---Written by Alan Steinberg---\n")
	while (True):
		print("\n1. Aggregate incidents per zip code")
		print("2. Aggregate incidents per boroughs")
		print("3. Analyze incidents per 10k capita by zip")
		print("4. Analyze incidents per 10k capita  by Borough")

		kb_user = input("   Enter Choice:").lower().strip()

		if (kb_user == "1"):
			zip_root = True
			break
		elif (kb_user == "2"):
			zip_root = False
			break
		elif (kb_user == "3"):
			count_zip_incidents('data/311.csv', )
		elif (kb_user == "4"):
			count_borough_incidents('data/311.csv', )
		else:
			print("Bad input! Either (1,2,3,4) are to be chosen.")
		preprocessing_csv("data/311.csv", 1, zip_root)


main()
