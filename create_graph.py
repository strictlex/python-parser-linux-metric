import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

folder_reports = Path(r'./filtered_reports')
output_dir = Path(r'./graphs')
output_dir.mkdir(exist_ok=True)
files = folder_reports.glob(r'*.csv')
label_dict = {
        'CPU': 'Загрузка CPU, %',
        'kbmemfree': 'Использование памяти (KB)"',
        'DEV':'Дисковый ввод-вывод', 
        'tps':'Дисковый ввод-вывод', 
        'IFACE':'Сетевой трафик',
        'pgpgin/s': 'Подкачка страниц',
        'runq-sz': 'Длина очереди / % занятости',
        'kbswpfree' : 'Использование swap (KB / %)' }

for file in files:
    df = pd.read_csv(file,sep='\t', decimal=',')
    times = df['times']
    times = pd.to_datetime(times)
    label_metrics = label_dict.get(df.columns[1],'Значение')
    print(file.name)
    df.set_index('times', inplace=True)
    df.select_dtypes(include='number')
    df.plot(figsize=(10,6),fontsize=12)
    plt.grid(True)
    plt.title(file.name)
    plt.ylabel(ylabel=label_metrics)
    plt.savefig(output_dir / f'{file.stem}.png')
    plt.show()