import pandas as pd
from pathlib import Path
import re

data = {}

folder_from = Path(r'./filtered_reports')
output_file = 'sar_anlysis.xlsx'

#помещаем все данные со всех файлов в один словарь, ключ - суффикс имении файлла, значение - строкии файла
for file in folder_from.glob('*.csv'):
    key = re.search(r'out_(.*).csv',file.name).group(1) # type: ignore
    data[key] = pd.read_csv(file,sep='\t',decimal=",")

#сбор метрик для ЦПУ и очереди
merged = pd.merge(
    data['cpu_util'],
    data['queue'][['times', 'runq-sz']],
    on='times'
    )
merged['cpu_util'] = 100 - merged['%idle']
cpu_data = merged[['times', 'cpu_util', 'runq-sz']].copy()

#сбор метрик для Утил памяти
memory_data = pd.merge(
    data['memory'][['times','%memused']],
    data['swap'][['times','%swpused']],
    on='times'
    )

#сбор метрик Утил сетевого интерфейса
network_all = data['network']#[['times','IFACE','txkB/s','rxkB/s']]
interfaces = network_all['IFACE'].unique()
network_data = {}

for iface in interfaces:
    if iface != 'lo':
        df_iface = network_all[network_all['IFACE']==iface].copy()
        df_iface = df_iface[['times','txkB/s','rxkB/s']]

        df_iface['rx_mbps'] = df_iface['rxkB/s'].astype(float) / 128
        df_iface['tx_mbps'] = df_iface['txkB/s'].astype(float) / 128

        if (sum(df_iface['rx_mbps']) > 0) or (sum(df_iface['tx_mbps']) > 0):
            network_data[iface] = df_iface[['times','rx_mbps','tx_mbps']]


#сбор метрик чтение\запись дисков
disk_all = data['disk']
disk_data = {}
devices = disk_all['DEV'].unique()

for device in devices:
    if device != 'DEV':
        df_dev = disk_all[disk_all['DEV']==device].copy()
        df_dev = df_dev[['times','await','%util']]
        if df_dev['%util'].sum() > 0:
            disk_data[device] = df_dev

with pd.ExcelWriter(output_file) as writer:
    cpu_data.to_excel(writer, sheet_name='CPU', index=False)
    memory_data.to_excel(writer, sheet_name='Memory', index=False)

    for iface,df_iface in network_data.items():
        sheet_name = f'Net_{iface}'[:31]
        df_iface.to_excel(writer, sheet_name=sheet_name,index=False)

    for device, df_dev in disk_data.items():
        sheet_name = f'Disk_{device}'[:31]
        df_dev.to_excel(writer, sheet_name=sheet_name,index=False)

print(f'Файл {output_file} успешно создан!')