import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

RUTIFICADOR_URL = "https://rutificador.net/rut/"
def bloquear_anuncios(route):
    if any(domain in route.request.url for domain in ["googletagmanager.com", "googlesyndication.com", "ads", "advertising"]): route.abort()
    else: route.continue_()

def buscar_rut(page, rut_a_buscar, datos_ruts, ruts_no_encontrados):
    try:
        fecha_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"{fecha_hora}\tBuscando RUT: {rut_a_buscar}")
        page.goto(RUTIFICADOR_URL, timeout=60000)
        page.wait_for_selector('input[name="rut"]', timeout=10000)
        page.fill('input[name="rut"]', rut_a_buscar)
        page.click('button#btn-buscar')
        page.wait_for_selector('table#tabla-resultados', timeout=10000)
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        tabla_resultados = soup.find('table', {'id': 'tabla-resultados'})

        if tabla_resultados:
            filas = tabla_resultados.find('tbody').find_all('tr')
            for fila in filas:
                columnas = fila.find_all('td')
                rut = columnas[0].get_text().strip()
                nombre = columnas[1].get_text().strip()
                edad = columnas[2].get_text().strip()
                sexo = columnas[3].get_text().strip()
                domicilio = columnas[4].get_text().strip()
                ciudad = columnas[5].get_text().strip()
                datos_ruts[rut] = (nombre, edad, sexo, domicilio, ciudad)

        else:
            print(f"No se encontraron resultados para el RUT: {rut_a_buscar}")
            ruts_no_encontrados.append(rut_a_buscar)

    except Exception as e:
        print(f"Error durante la búsqueda del RUT {rut_a_buscar}: {e}")
        ruts_no_encontrados.append(rut_a_buscar)

def ingresar_multiples_ruts(page, datos_ruts, ruts_no_encontrados):
    tiempo_inicio = time.time()
    ruts_encontrados = 0
    while True:
        try:
            cantidad_ruts = int(input("¿Cuántos RUTs deseas ingresar? (de 1 a 50): "))
            if 1 <= cantidad_ruts <= 50: break
            else: print("Por favor, ingresa un número entre 1 y 50.")
        except ValueError: print("Entrada no válida. Por favor, ingresa un número válido.")

    ruts = []
    for i in range(cantidad_ruts):
        rut = input(f"Ingresa el RUT {i+1}: ")
        ruts.append(rut)

    for rut in ruts:
        buscar_rut(page, rut, datos_ruts, ruts_no_encontrados)
        if rut in datos_ruts: ruts_encontrados += 1

    tiempo_final = time.time()
    tiempo_total = tiempo_final - tiempo_inicio
    print(f"Se encontraron datos para {ruts_encontrados} de {cantidad_ruts} RUTs ingresados.")
    print(f"El tiempo total de búsqueda fue de {tiempo_total:.2f} segundos.")

def mostrar_datos(datos_ruts, ruts_no_encontrados):
    if datos_ruts:
        print("\nDatos de todos los RUTs encontrados:")
        print(f"{'RUT':<15} {'Nombre':<30} {'Edad Aprox.':<10} {'Sexo':<10} {'Domicilio':<30} {'Ciudad':<20}")
        print("-" * 125)
        for rut, datos in datos_ruts.items():
            nombre, edad, sexo, domicilio, ciudad = datos
            print(f"{rut:<15} {nombre:<30} {edad:<10} {sexo:<10} {domicilio:<30} {ciudad:<20}")
        print(f"\nTotal de RUTs almacenados: {len(datos_ruts)}")

    if ruts_no_encontrados:
        print(f"\nNo se encontraron datos para {len(ruts_no_encontrados)} RUTs:")
        for rut in ruts_no_encontrados: print(f"{rut}")
    else: print("Todos los RUTs ingresados tuvieron resultados.")

def exportar_a_excel(datos_ruts):
    try:
        df = pd.DataFrame([(rut, datos[0], datos[1], datos[2], datos[3], datos[4]) for rut, datos in datos_ruts.items()],columns=["RUT", "Nombre", "Edad Aprox.", "Sexo", "Domicilio", "Ciudad"])
        nombre_archivo = input("Ingresa el nombre del archivo: ")
        if not nombre_archivo.endswith(".xlsx"): nombre_archivo += ".xlsx"

        df.to_excel(nombre_archivo, index=False)
        ruta_completa = os.path.abspath(nombre_archivo)
        print(f"Datos exportados exitosamente a '{ruta_completa}'.")
    except Exception as e: print(f"Error al exportar los datos a Excel: {e}")

def menu():
    datos_ruts = {}
    ruts_no_encontrados = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', headless=True)
        page = browser.new_page()
        page.route("**/*", bloquear_anuncios)
        while True:
            print("\nMenú:\n1. Ingresar entre 1 y 50 RUTs y medir el tiempo\n2. Mostrar todos los datos\n3. Exportar los datos a Excel\n4. Salir")
            opcion = input("Selecciona una opción: ")
            if opcion == '1': ingresar_multiples_ruts(page, datos_ruts, ruts_no_encontrados)
            elif opcion == '2': mostrar_datos(datos_ruts, ruts_no_encontrados)
            elif opcion == '3': exportar_a_excel(datos_ruts)
            elif opcion == '4':
                print("Saliendo del programa...")
                break
            else: print("Opción no válida, por favor intenta de nuevo.")
        browser.close()
        
if __name__ == "__main__": menu()