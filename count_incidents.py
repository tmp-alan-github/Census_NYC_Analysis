from pprint import pprint
import pandas as pd


def get_population_from_zip( zip_code ):
	with open("data/zips_pop_nyc.csv", "r") as f:
		for line in f:
			split = line.split(":")
			if (split[0]) == zip_code:
				# print(split[0],split[1])
				return split[1]


def count_borough_incidents( in_f='data/311.csv', size=1 ):
	# Below populations grabbed from Census.gov, https://bit.ly/2mrBYQl
	population_dict = {"bronx": 1471160, "brooklyn": 2648771, "manhattan": 1664727, 'queens': 23585832,
	                   'staten island': 479558}

	counting_dict = {"bronx": 0, "brooklyn": 0, "manhattan": 0, 'queens': 0, 'staten island': 0}
	reader = pd.read_table(in_f, sep=',', skip_blank_lines=True, memory_map=True, chunksize=size, nrows=10000)

	for chunk in reader:
		borough = str(chunk['Borough'].values[0]).strip().lower()
		try:
			counting_dict[borough] += 1
		except KeyError:
			print("unspecified: ", borough)
		pprint(dict(counting_dict))
		print("------")

	counting_dict_testing = {'bronx': 31576, 'brooklyn': 52929, 'manhattan': 34820, 'queens': 40339,
	                         'staten island': 9088}

	print("--- Complaints per 10,000 people in Boroughs --- \n")
	for key in population_dict.keys():

		result = float("{0:.2f}".format(counting_dict[key] / (population_dict[key]) * 100000))
		print(key, " - ", result)


def count_zip_incidents( in_f='data/311.csv', size=1 ):
	reader = pd.read_table(in_f, sep=',', skip_blank_lines=True, chunksize=size)
	zip_counter = {}
	zips = 0
	for chunk in reader:
		try:
			zips = (str(float(chunk['Incident Zip'].values[0])).split(",")[0].strip())[:-2]
			print(zips)
		except Exception as e:
			print("ERROR (Likely NAN),:", e, zips)

		if zips.isnumeric():
			zip_counter.setdefault(zips, 1)
			zip_counter[zips] += 1
			pprint(dict(zip_counter))

	for zip_tmp in zip_counter:
		try:
			zip_counter[zip_tmp] = (float(zip_counter[zip_tmp]) / float(get_population_from_zip(zip_tmp))) * 10000.0
		except TypeError:
			print("Type Error:", zip_tmp)
	print("\n ----Sorted by most incidents per zip (top 10)  ---- \n")
	for w in sorted(zip_counter, key=zip_counter.get, reverse=True)[0:10]:
		print(w, " - ", float("{0:.2f}".format(zip_counter[w])))
