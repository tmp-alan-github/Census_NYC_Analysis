import unicodedata

from fuzzywuzzy import fuzz


# Early and primative sanitizing of inputs
def clean_to_int( num ):
	try:
		tmp = int(num)
		if (len(str(tmp)) == 5):
			return tmp
		else:
			print(tmp, " NOT ZIP CODE LENGTH ", len(tmp))
			raise Exception
	except Exception as e:  # Still looking into this
		tmp = int(str(num).strip().isnumeric())
		print("BAD NUM:", tmp, " Original : ", num)


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
