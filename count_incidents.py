def get_population_from_zip( zip_code ):
	# CSV from ZCTA (https://bit.ly/2x8dH6c)
	# Grab the population from input zip
	with open("data/zips_pop_nyc.csv", "r") as f:
		for line in f:
			census_list = line.strip().split(",")
			if int(census_list[0]) == int(zip_code):
				return int(census_list[1])  # Corresponding population
	return -1


def count_borough_incidents( dataframe ):
	# Below total true  populations grabbed from Census.gov, https://bit.ly/2mrBYQl
	population_dict = {"BRONX": 1471160, "BROOKLYN": 2648771, "MANHATTAN": 1664727, 'QUEENS': 23585832,
	                   'STATEN ISLAND': 479558}

	# Count borough values from the dataframe, turn into dict after for simple dict iterating
	d = dataframe['borough'].value_counts()
	borough_counter = dict(d)


	print("\n--- Complaints per 10,000 people in Boroughs --- \n")
	for key in population_dict.keys():
		result = float("{0:.2f}".format(borough_counter[key] / (population_dict[key]) * 100000))
		print(key, " - ", result)


def count_zip_incidents( dataframe ):
	# dataframe[column_list] = dataframe[column_list].apply(pd.to_numeric, errors='coerce')
	d = dataframe['incident_zip'].astype(int, errors='ignore')
	zip_counter = d.value_counts().to_dict()

	for zip_tmp in zip_counter:
		try:
			# Grab population from zip csv, then do per 10k people on the incidents each zip
			zip_pop = float(str(get_population_from_zip(zip_tmp)).strip())
			if zip_pop < 10:  ##Low population skews results too much, filtering with min of 10
				zip_pop = 0.0
			zip_counter[zip_tmp] = (float(zip_counter[zip_tmp]) / (zip_pop)) * 10000.0
		except Exception as e:
			pass
	print("\n -  Sorted by most complaint/population per 10k people (top 20) - \n")
	for w in sorted(zip_counter, key=zip_counter.get, reverse=True)[0:20]:  # Sort, grab top 20
		try:
			print(int(w), " - ", '{0:.3f}'.format(zip_counter[w]))
		except Exception as e:
			print(e, "Bad zip : ", w)  #Rare
