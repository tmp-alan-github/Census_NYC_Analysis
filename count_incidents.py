from pprint import pprint
import pandas as pd


def count_borough_incidents( in_f='data/311.csv', size=1 ):
    population_dict = {"bronx": 1471160, "brooklyn": 2648771, "manhattan": 1664727, 'queens': 23585832,
                       'staten island': 479558}

    counting_dict = {"bronx": 0, "brooklyn": 0, "manhattan": 0, 'queens': 0, 'staten island': 0}
    reader = pd.read_table(in_f, sep=',', skip_blank_lines=True, memory_map=True, chunksize=size)

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
    print("Complaints per 10,000 people")
    for key in population_dict.keys():
        result = int(counting_dict[key] * (100000 / (population_dict[key])))
        print(key, " - ", result)


def count_zip_incidents( in_f='data/311.csv', size=1 ):
    reader = pd.read_table(in_f, sep=',', skip_blank_lines=True, chunksize=size)
    zip_counter = {}
    for chunk in reader:
        zip = str(chunk['Incident Zip'].values[0]).split(",")[0].strip()
        if ("nan" != zip):
            zip_counter.setdefault(zip, 1)
            zip_counter[zip] += 1
            pprint(dict(zip_counter))
