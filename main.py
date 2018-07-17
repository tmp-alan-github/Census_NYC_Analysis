from collections import defaultdict, Counter
from pprint import pprint

import pandas as pd

from count_incidents import count_borough_incidents, count_zip_incidents
from util import clean_strings, clean_to_int


def json_url_to_dataframe():
	# URL takes advantage of 'floating timestamps' that query between two dates (2017), possible to push this further in hopes of limiting scope
	# Then is shoved into a dataframe to be return back to counter method
	url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?$where=due_date%20between%20%272017-01-01T12:19:54.000%27%20and%20%272017-12-31T12:19:54.000%27'
	dataframe = pd.read_json(url, orient="columns")
	dataframe = pd.DataFrame.from_records(dataframe)
	return dataframe


# Primary counting logic of the user's chosen attribute.
def counter_processing( size, zip_root ):
	pd.set_option('display.max_columns', 100000)

	d = json_url_to_dataframe()

	nested_dict = defaultdict(Counter)

	# Primary loop to locate, and increment. Cleanse functions are used here.
	for row in range(len(d)):
		z = d.loc[row, 'incident_zip']
		c = d.loc[row, 'complaint_type']
		b = d.loc[row, 'borough']

		z = clean_to_int(z)
		c = clean_strings(c)
		b = clean_strings(b)

		print(b, " - ", c, " - ", z)

		if (zip_root):  # Option 1 at menu (Zip is parent/root)
			nested_dict[z][c] += 1
		elif ('unspecified' not in b):  # Option 2
			nested_dict[b][c] += 1

	print("\n" * 5, " -------- \n")
	pprint(dict(nested_dict))  # Print out final structure


# Start the program and menu system, main call
if __name__ == "__main__":
	zip_root = None
	print("\n---Written by Alan Steinberg---\n")

	while (True):
		print("\n1.Aggregate incidents per zip code")
		print("2. Aggregate incidents per boroughs")
		print("3. Analyze incidents per 10k capita by zip")
		print("4. Analyze incidents per 10k capita  by Borough")

		kb_user = input(" Enter Choice:").lower().strip()  #Menu needs some cleaning up, too much redundnacy.
		if (kb_user == "1"):
			zip_root = True
			counter_processing(1, zip_root)
		elif (kb_user == "2"):
			zip_root = False
			counter_processing(1, zip_root)
		elif (kb_user == "3"):
			count_zip_incidents('data/311.csv', )
		elif (kb_user == "4"):
			count_borough_incidents('data/311.csv', )
		else:
			print("Bad input! Either (1,2,3,4) are to be chosen.")
	counter_processing(1, zip_root)
