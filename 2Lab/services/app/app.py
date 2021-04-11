import csv
from config import output_folder, table_name
from profiler import profile_time
import database


def to_csv(header, rows):
    """
    Save csv file with given header and rows into output folder
    """
    with open(output_folder + 'result.csv', 'w') as result:
        result_writer = csv.writer(result, delimiter=';')
        result_writer.writerow(header)
        result_writer.writerows(rows)


@profile_time
def main():
    try:
        to_csv(*database.get_min_phys_2019_2020(table_name))
    except (database.interface_error, database.operational_error) as e:
        print('Problem with database')
        print(e)
    else:
        print('Queue executed, file saved')


if __name__ == '__main__':
    main()
