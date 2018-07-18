def get_population_from_zip( zip_code ):
	# zips_pop_nyc is a generated csv with syntax of  zip:population
	# Grab the population from input zip
	with open("data/zips_pop_nyc.csv", "r") as f:
		for line in f:
			split = line.strip().split(":")
			if int(split[0]) == int(zip_code):
				return int(split[1])


def count_borough_incidents( dataframe ):
	# Below total true  populations grabbed from Census.gov, https://bit.ly/2mrBYQl
	population_dict = {"BRONX": 1471160, "BROOKLYN": 2648771, "MANHATTAN": 1664727, 'QUEENS': 23585832,
	                   'STATEN ISLAND': 479558}

	# Count borough values from the dataframe, turn into dict after for simple dict iterating
	d = (dataframe['borough'].value_counts())
	borough_counter = dict(d)

	# counting_dict_testing = {'BRONX': 31576, 'BROOKLYN': 52929, 'MANHATTAN': 34820, 'QUEENS': 40339,'STATEN ISLAND': 9088}

	print("\n--- Complaints per 10,000 people in Boroughs --- \n")
	for key in population_dict.keys():
		result = float("{0:.2f}".format(borough_counter[key] / (population_dict[key]) * 100000))
		print(key, " - ", result)


def count_zip_incidents( dataframe ):
	d = dataframe['incident_zip'].value_counts()

	zip_counter = dict(d)
	for zip_tmp in zip_counter:
		try:
			# Grab population from zip csv, then do per 10k people on the incidents each zip
			zip_pop = float(str(get_population_from_zip(zip_tmp)).strip())
			zip_counter[zip_tmp] = (float(zip_counter[zip_tmp]) / (zip_pop)) * 10000.0
		except Exception as e:
			print(e, zip_tmp)
	print("\n ----Sorted by most complaint/population per 10k people (top 10)  ---- \n")
	for w in sorted(zip_counter, key=zip_counter.get, reverse=True)[0:10]:
		print(int(w), " - ", '{0:.3f}'.format(zip_counter[w]))
