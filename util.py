# Early and primative sanitizing of inputs
def clean_to_int( num ):
	try:
		tmp = int(num)
		return tmp
	except Exception as e:  # Still looking into this
		tmp = int(str(num).strip().isnumeric())
		print("BAD NUM:", tmp, " Original : ", num)


def clean_strings( st ):
	return st.lower().strip().replace("dof", "")


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
