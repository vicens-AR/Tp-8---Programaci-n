import csv

with open('copa-america-2024-UTC.csv', mode='r', newline='', encoding='utf-8') as archivo:
    lector = csv.reader(archivo)
    encabezados = next(lector) 
for fila in lector:
    print(fila)