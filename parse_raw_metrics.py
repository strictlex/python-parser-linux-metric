import csv
from pathlib import Path
import re

def main():

    folder_from = Path(r'./raw_reports/')
    folder_to = Path(r'./filtered_reports/')
    Path(folder_to).mkdir(parents=True, exist_ok=True)


    csv_files = folder_from.glob('*.csv')
    pattern_spase = r'\s{3,}'

    def split_data(row):
        return re.split(pattern_spase,"".join(row))

    for file_path in csv_files:

        with open(file_path,'r', encoding='utf-8') as file:
            reader = (i.strip('\n') for i in file.readlines())
            next(reader)
            next(reader)
            header = next(reader).split()
            first_time = header[0]
            header[0] = 'times'
            iter_reader = (split_data(r) for r in reader if r[0:2].isdigit())
            out_path_name = f'{folder_to}/{file_path.name}'

            with open(out_path_name,'w', encoding='utf-8') as file:
                writer = csv.writer(file,delimiter="\t")
                writer.writerow(header)
                for row in iter_reader:
                    if row[0]==first_time or row[1] == header[1]:
                        break
                    else:
                        writer.writerow(row)
                    

    print("Обработаные данные выгружены в папку filtered_reports в формате .csv")


if __name__ == "__main__":
    print("Начинаем обработку сырых метрик")
    main()
    
