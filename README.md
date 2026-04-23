metrics_and_collect_raw_repots.txt - команды для запуска сбора метрик
file_sh_for_linux.txt -  скрипт bash sh для линукс
грузим в папку "raw_reports" - файлы csv с сырыми метриками линукс  
parse_raw_metrics.py - обрабатывает сырые(sar csv - просто текстовик) sar метрики в рабочий csv
create_graph.py - строит графики по каждому обработанному csv
all_in_one_csv_for_excel.py - выгружает нужны метрики в один xlsx файл для импорта в excel\google sheets