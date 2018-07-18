import glob
import unicodedata
from os.path import getsize

import requests
from fuzzywuzzy import fuzz


# Early and primative sanitizing of inputs
def verify_clean_zip( num ):
	try:
		zip_tmp = int(num)
		# Min,Max of ranges shown by DoH - ZIP Code Definitions https://on.ny.gov/1RnUmTz
		# Below if to check length is proper and that zip is within NYC ranges
		if len(str(zip_tmp)) == 5 and (10001 <= zip_tmp and zip_tmp <= 11697):
			return zip_tmp
		elif (10001 > zip_tmp or zip_tmp > 11697):
			print(zip_tmp, " NOT ZIP CODE WITHIN NYC RANGE ")
		else:
			print(zip_tmp, " NOT ZIP CODE OF LENGTH 5: ", len(zip_tmp))

	except Exception as e:  # Still looking into this
		zip_tmp = int(str(num).strip().isnumeric())
		print("BAD ZIP:", zip_tmp, " Original : ", num)


def attempt_borough_from_zip( zip ):
	pass  # Working on

# Multiple bombs dropped on misbehaving strings (and still more to come)
def clean_string( st ):
	s = st.lower().strip().replace("dof", "").replace("  ", "")
	s = s.translate(str.maketrans("", "", ",.-'\"():;+/?$°@"))
	s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
	return s


# Fuzzy search to help detect words that are very similar, possible typos/redundancy can be found.
# Threshhold at 75 similarity. Number of searches can be reduced if time allows.
def string_similarity( word_set ):
	word_set = list(word_set)
	print("FUZZY LIST - CANDIDATES OVER THRESHHOLD")
	for s1 in word_set:
		for s2 in word_set:
			if s1 != s2:
				proximity = fuzz.ratio(s1, s2)
				if proximity > 75:
					print(proximity, " ==  ", s1, "-- ", s2)
	print("\n\n")


# Write out functions, will find more use for them in staging and potential cache scenarios.
def write_set( zipset ):
	with open('nyc_zips.txt', 'w') as f:
		for i in zipset:
			f.write(str(i) + "\n")


def write_dict_to_csv( tmp_dict, out_f="output.csv" ):
	with open(out_f, 'w') as f:  # Just use 'w' mode in 3.x
		w = csv.DictWriter(f, tmp_dict.keys())
		w.writeheader()
		w.writerow(tmp_dict)


def download_jsons():
	for i in range(100):  # range 100 is arbitrarly high, break occurs at about 23~
		# URL takes advantage of 'floating timestamps' that query between two dates (2017) and only selects what is needed
		url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?$query=SELECT%20incident_zip,due_date,borough,complaint_type%20WHERE%20due_date%20between%20%272017-01-01T12:19:54.000%27%20and%20%272017-12-30T12:19:54.000%27%20LIMIT%2050000%20OFFSET%20'
		# Downloaded in increments because of 50k line limit, break upon smaller file increment
		url_offset = url + str(i * 50000)
		response = requests.get(url_offset, stream=True)
		handle = open(f'data/data{i}.json', "wb")
		print(f'Downloading data{i}.json ...')
		for chunk in response.iter_content(chunk_size=512):
			if chunk and len(chunk) > 3:  # filter out keep-alive new chunks
				handle.write(chunk)
		if getsize(f'data/data{i}.json') < (1024 * 1024 * 4):  # Last increment if below 4mb
			break
	print("Finished Download Increments")


def get_jsons_list():  # Retrieve list of jsons, if none then download
	read_files = glob.glob("data/data*.json")
	if not read_files:
		print("Data is not found! Downloading JSONs")
		download_jsons()
	return glob.glob("data/data*.json")
