import psycopg2
import time
import csv
from config import datasets


def main():
    for year, path in datasets.items():
        # load csv files
        with open(path, encoding='cp1251') as dataset:
            start_time = time.time()
            datasets[year] = csv.DictReader(dataset, delimiter=';')
            # just print header (keys of the dictionary)
            print(tuple(next(datasets[year])))
            print("csv.DictReader took %s seconds" % (time.time() - start_time))


if __name__ == '__main__':
    main()
