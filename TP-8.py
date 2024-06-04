import csv

def leer_fixture(archivo_csv):
    partidos = []
    with open(archivo_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            partidos.append(row)
    return partidos

def inicializar_equipos(partidos):
    equipos = {}
    for partido in partidos:
        if partido['Home Team'] not in equipos:
            equipos[partido['Home Team']] = {
                'Puntos': 0, 'Partidos Jugados': 0, 'Victorias': 0, 'Empates': 0,
                'Derrotas': 0, 'Goles a Favor': 0, 'Goles en Contra': 0, 'Diferencia de Goles': 0
            }
        if partido['Away Team'] not in equipos:
            equipos[partido['Away Team']] = {
                'Puntos': 0, 'Partidos Jugados': 0, 'Victorias': 0, 'Empates': 0,
                'Derrotas': 0, 'Goles a Favor': 0, 'Goles en Contra': 0, 'Diferencia de Goles': 0
            }
    return equipos

def actualizar_resultados(archivo_csv_resultados, equipos, partidos):
    with open(archivo_csv_resultados, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            actualizar_partido(row, equipos, partidos)

def actualizar_partido(resultado, equipos, partidos):
    match_number = int(resultado['Match Number'])
    home_goals = int(resultado['Home Team Goals'])
    away_goals = int(resultado['Away Team Goals'])
    
    for partido in partidos:
        if int(partido['Match Number']) == match_number:
            partido['Result'] = f"{home_goals}-{away_goals}"
            actualizar_estadisticas(partido, home_goals, away_goals, equipos)
            break

def actualizar_estadisticas(partido, home_goals, away_goals, equipos):
    home_team = partido['Home Team']
    away_team = partido['Away Team']
    
    equipos[home_team]['Partidos Jugados'] += 1
    equipos[away_team]['Partidos Jugados'] += 1
    equipos[home_team]['Goles a Favor'] += home_goals
    equipos[away_team]['Goles a Favor'] += away_goals
    equipos[home_team]['Goles en Contra'] += away_goals
    equipos[away_team]['Goles en Contra'] += home_goals
    equipos[home_team]['Diferencia de Goles'] += (home_goals - away_goals)
    equipos[away_team]['Diferencia de Goles'] += (away_goals - home_goals)
    
    if home_goals > away_goals:
        equipos[home_team]['Victorias'] += 1
        equipos[home_team]['Puntos'] += 3
        equipos[away_team]['Derrotas'] += 1
    elif home_goals < away_goals:
        equipos[away_team]['Victorias'] += 1
        equipos[away_team]['Puntos'] += 3
        equipos[home_team]['Derrotas'] += 1
    else:
        equipos[home_team]['Empates'] += 1
        equipos[away_team]['Empates'] += 1
        equipos[home_team]['Puntos'] += 1
        equipos[away_team]['Puntos'] += 1

def calcular_posiciones(equipos):
    posiciones = sorted(equipos.items(), key=lambda item: (
        item[1]['Puntos'], item[1]['Diferencia de Goles'], item[1]['Goles a Favor']), reverse=True)
    return posiciones

def generar_informe_final(posiciones, archivo_salida):
    with open(archivo_salida, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Grupo', 'Equipo', 'Puntos', 'Partidos Jugados', 'Victorias', 'Empates', 'Derrotas', 'Goles a Favor', 'Goles en Contra', 'Diferencia de Goles'])
        for equipo, stats in posiciones:
            writer.writerow(['Grupo X', equipo, stats['Puntos'], stats['Partidos Jugados'], stats['Victorias'], stats['Empates'], stats['Derrotas'], stats['Goles a Favor'], stats['Goles en Contra'], stats['Diferencia de Goles']])

def mostrar_menu():
    print("Menú de Opciones:")
    print("1. Leer Fixture")
    print("2. Actualizar Resultados")
    print("3. Calcular Posiciones")
    print("4. Generar Informe Final")
    print("5. Salir")

def main():
    archivo_fixture = 'copa-america-2024-UTC.csv'
    archivo_resultados = 'resultados.csv'
    archivo_salida = 'posiciones_finales.csv'
    
    partidos = []
    equipos = {}
    
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")
        
        if opcion == '1':
            partidos = leer_fixture(archivo_fixture)
            equipos = inicializar_equipos(partidos)
            for partido in partidos[:5]:  # Mostrar los primeros 5 partidos como ejemplo
                print(partido)
                
        elif opcion == '2':
            if not partidos:
                print("Primero debes cargar el fixture.")
            else:
                actualizar_resultados(archivo_resultados, equipos, partidos)
                print("Resultados actualizados.")
                
        elif opcion == '3':
            if not equipos:
                print("Primero debes cargar el fixture y actualizar los resultados.")
            else:
                posiciones = calcular_posiciones(equipos)
                for equipo, stats in posiciones:
                    print(equipo, stats)
                    
        elif opcion == '4':
            if not equipos:
                print("Primero debes cargar el fixture y actualizar los resultados.")
            else:
                posiciones = calcular_posiciones(equipos)
                generar_informe_final(posiciones, archivo_salida)
                print(f"Informe final generado en {archivo_salida}.")
                
        elif opcion == '5':
            print("Saliendo...")
            break
            
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == '__main__':
    main()