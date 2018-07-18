from collections import defaultdict, Counter
from pprint import pprint

import pandas as pd

from count_incidents import count_borough_incidents, count_zip_incidents
from util import clean_string, verify_clean_zip, string_similarity, get_jsons_list


def json_url_to_dataframe():
	dfs = []
	json_files = get_jsons_list()

	# Then is shoved into a dataframe to be return back to counter method
	for file in json_files:
		dataframe = pd.read_json(file, orient="columns", dtype={'incident_zip': int})
		dfs.append(dataframe)

	dataframe = pd.concat(dfs)
	dataframe = pd.DataFrame.from_records(dataframe)
	print(dataframe.shape)
	return dataframe


# Helper function, likely to be removed
def handle_similarity_debug( set_tmp ):
	if len(set_tmp) > 0:
		string_similarity(set_tmp)


# Primary counting logic of the user's chosen attribute.
def counter_processing( dataframe, is_zip_root, sanitize_dev=False ):
	word_set_diff = set()  # Used for storing words/phrases to later be similarilty checked
	d = dataframe

	# Dict to aggregate counts
	nested_dict = defaultdict(Counter)

	# Primary loop to locate, and increment. Cleanse functions are used here.
	for row in range(len(d)):

		# Yank
		zip = d.loc[row, 'incident_zip']
		complaint = d.loc[row, 'complaint_type']
		borough = d.loc[row, 'borough']

		# Clean
		zip = verify_clean_zip(zip)
		complaint = clean_string(complaint)
		borough = clean_string(borough)

		#Dev - String Similarity sets
		word_set_diff.add(borough)
		word_set_diff.add(complaint)

		print(borough, " - ", complaint, " - ", zip)  # Raw print as rows iterate

		if (is_zip_root):  # Option 1 at menu (Zip is parent/root)
			nested_dict[zip][complaint] += 1
		elif ('unspecified' not in borough):  # Option 2  - with unspecified check
			nested_dict[borough][complaint] += 1
		elif ("unspecified" in borough):
			print("UNSPECIFIED", borough, zip)  #Adding zip cross-reference check soon
	print("\n" * 5, " -------- \n")
	pprint(dict(nested_dict))  # Print out final structure

	# Kicks off fuzzy-wuzzy checking (Option 5)
	if sanitize_dev:
		print("\n\n-- FUZZY CHECKING --")
		handle_similarity_debug(word_set_diff)


# Start the program and menu system, main call
if __name__ == "__main__":
	is_zip_root = None
	print("\n---Written by Alan Steinberg---\n")

	# Dataframe being generated from the numerous JSONs to be passed throughout
	df = json_url_to_dataframe()


	while (True):
		print("\n1. Aggregate incidents per zip code")
		print("2. Aggregate incidents per boroughs")
		print("3. Analyze incidents per 10k capita by zip")
		print("4. Analyze incidents per 10k capita  by Borough")
		print("5. (DEV) - String Similarity Comparison FuzzyWuzzy")

		kb_user = input("Enter Choice: ").lower().strip()  # Menu needs some cleaning up, too much redundnacy.
		if (kb_user == "1"):
			is_zip_root = True
			counter_processing(df, is_zip_root)
		elif (kb_user == "2"):
			is_zip_root = False
			counter_processing(df, is_zip_root)
		elif (kb_user == "3"):
			count_zip_incidents(df)  # to be fixed
		elif (kb_user == "4"):
			count_borough_incidents(df)  # to be fixed
		elif (kb_user == "5"):
			counter_processing(df, is_zip_root, sanitize_dev=True)
		else:
			print("Bad input! Either (1,2,3,4,5) are to be chosen.")
