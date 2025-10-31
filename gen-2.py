"""
Script para generar el archivo de datos y resolver el problema de
maximización de la satisfacción de los pasajeros.
Parte 2.2.2
"""

import sys
import os
import subprocess

def leer_archivo_entrada(ruta_entrada):
    """Lee el archivo de entrada y devuelve los datos."""
    try:
        with open(ruta_entrada, 'r') as f:
            lineas = f.readlines() # Devuelve una lista de strings
        
        # Eliminamos espacios al inicio y final de cada linea
        lineas = [linea.strip() for linea in lineas]

        # Leemos la primera línea para obtener n, m y u
        n, m, u = map(int, lineas[0].split())

        if len(lineas) != 1 + m + n:    # número de líneas que debe deben tener los datos de entrada
            raise ValueError("El archivo de entrada no tiene el formato correcto")

        # Con el valor de m, leemos las siguientes m líneas que se corresponden con la matriz de pasajeros
        c = []
        for i in range(1, m + 1):
            fila = list(map(int, lineas[i].split()))
            if len(fila) != m:
                raise ValueError(f"La fila {i} de la matriz de pasajeros no tiene {m} elementos. Tiene {len(fila)}")      # número de columnas no válido
            c.append(fila)

        # Con el valor de u, leemos las siguientes u líneas que se corresponden con la matriz de disponibilidad
        o = []
        for i in range(m + 1, m + 1 + n):
            fila = list(map(int, lineas[i].split()))
            if len(fila) != u:
                raise ValueError(f"La fila {i} de la matriz de disponibilidad no tiene {u} elementos. Tiene {len(fila)}")  # número de columnas no válido
            o.append(fila)
        
        return n, m, u, c, o
    
    except Exception as e:
        print(f"Error leyendo el archivo de entrada: {e}")
        sys.exit(1)

def verificar_factibilidad(n, m, u, o):
    """Verifica si el problema es factible"""
    total_franjas_disponibles = sum(o[i][j] for i in range(n) for j in range(u))    # numero de espacios disponibles
    
    print(f"Franjas disponibles: {total_franjas_disponibles}")
    print(f"Autobuses a asignar: {m}")
    
    if total_franjas_disponibles < m:
        print("ERROR: El problema es INFACTIBLE")
        print(f"Se necesitan al menos {m} franjas disponibles, pero solo hay {total_franjas_disponibles}")
        return False
    return True

def es_simetrica(matriz):
    n_filas = len(matriz)

    if n_filas == 0:
        return True
    
    # debe ser cuadrada (filas = columnas)
    n_columnas = len(matriz[0])

    if n_filas != n_columnas:
        return False
        
    for i in range(n_filas):
        for j in range(i + 1, n_columnas):
            
            if matriz[i][j] != matriz[j][i]:
                return False
                
    return True

def diagonal_es_cero(matriz):
    n = len(matriz)
    
    # Iteraramos sobre la diagonal principal (A[i][i])
    for i in range(n):
        if matriz[i][i] != 0:
            return False
            
    return True

def generar_archivo_datos(n, m, u, c, o, ruta_salida):
    """Genera el archivo .dat"""
    try:
        with open(ruta_salida, 'w') as f:
            # Escribir conjuntos
            # Talleres
            f.write(f"set TALLERES :=")
            for i in range(u):
                f.write(f" t{i+1}")
            f.write(";\n")
            # Autobuses
            f.write(f"set AUTOBUSES :=")
            for i in range(m):
                f.write(f" a{i+1}")
            f.write(";\n")
            # Franjas
            f.write(f"set FRANJAS :=")
            for i in range(n):
                f.write(f" s{i+1}")
            f.write(";\n\n")

            # Escribir parámetros
            # Matriz c
            f.write("param c :")
            # Escribir cabeceras de columnas (AUTOBUSES)
            for j in range(m):
                f.write(f" a{j+1}")
            f.write(" :=\n")
            
            for i in range(m):
                f.write(f"\ta{i+1}") # Cabecera de fila
                for j in range(m):
                    f.write(f" {c[i][j]}")
                if i < m - 1:
                    f.write("\n")
                else:
                    f.write(";\n\n")
            
            # Matriz o
            f.write("param o :")
            # Escribir cabeceras de columnas (TALLERES)
            for j in range(u):
                f.write(f" t{j+1}")
            f.write(" :=\n")
            
            # Las filas son FRANJAS (s1, s2, ...)
            for i in range(n):
                f.write(f"\ts{i+1}")
                for j in range(u):
                    f.write(f" {o[i][j]}")
                if i < n - 1:
                    f.write("\n")
                else:
                    f.write(";\n\n")
            
            f.write("end;\n")
            
            print(f"\nArchivo de datos generado: {ruta_salida}")
    
    except Exception as e:
        print(f"Error generando el archivo de datos: {e}")
        sys.exit(1)

def resolver_glpk(modelo, datos, salida_glpk="solucion-2.txt"):
    """Ejecuta GLPK para resolver el problema"""
    try:
        # Comando para ejecutar GLPK
        comando = ["glpsol", "--math", modelo, "--data", datos, "-o", salida_glpk]

        print("Ejecutando GLPK...")
        resultado = subprocess.run(comando, capture_output=True, text=True)

        if resultado.returncode != 0:
            print(f"Error al ejecutar GLPK: {resultado.stderr}")
            return None
        
        # Leer la solución de GLPK
        with open(salida_glpk, 'r') as f:
            solucion = f.read()
        
        return solucion

    except Exception as e:
        print(f"Error al ejecutar GLPK: {e}")
        return None

def procesar_solucion(solucion_glpk, n, m, u):
    """Procesa la solución de GLPK y la muestra en el formato pedido"""
    try:
        lineas = solucion_glpk.split('\n')
        valor_objetivo = None
        variables = 0
        restricciones = 0
        asignaciones = []

        # Buscar información en la salida de GLPK
        for linea in lineas:
            if "Objective:" in linea:
                partes = linea.split()
                if len(partes) >= 4:
                    valor_objetivo = float(partes[3])
            if "Rows:" in linea:
                partes = linea.split()
                if len(partes) >= 2:
                    restricciones = int(partes[1])
            if "Columns:" in linea:
                partes = linea.split()
                if len(partes) >= 2:
                    variables = int(partes[1])
            # Buscar variables x[i,t,f] que son 1
            if "x[" in linea and " 1" in linea:
                partes = linea.split()
                if len(partes) >= 4 and partes[3] == '1':
                    var_name = partes[1]
                    # Extraer autobús, taller y franja: x[i,t,f]
                    contenido = var_name.split('[')[1].split(']')[0]
                    autobus, taller, franja = contenido.split(',')
                    asignaciones.append((autobus, taller, franja))

        # Mostrar resultados en el formato pedido
        print(f"{valor_objetivo} {variables} {restricciones}")
        for autobus, taller, franja in sorted(asignaciones):
            print(f"Autobús {autobus} asignado a taller {taller} en franja {franja}")
        
        return valor_objetivo, variables, restricciones
    except Exception as e:
        print(f"Error procesando la solución: {e}")
        return None

def main():
    if len(sys.argv) != 3:
        print("Uso: ./gen-2.py <fichero-entrada> <fichero-salida>. Por ejemplo: ./gen-2.py ejemplo-2.in ejemplo-2.dat")
        sys.exit(1)
    
    ruta_entrada = sys.argv[1]
    ruta_salida = sys.argv[2]

    # Verificar que existe el archivo de entrada
    if not os.path.exists(ruta_entrada):
        print(f"Error: El archivo de entrada '{ruta_entrada}' no existe")
        sys.exit(1)
    
    # Leer datos de entrada
    print(f"Leyendo archivo de entrada: {ruta_entrada}")
    n, m, u, c, o = leer_archivo_entrada(ruta_entrada)

    print(f"Parámetros leídos:")
    print(f"  Franjas (n): {n}")
    print(f"  Autobuses (m): {m}")
    print(f"  Talleres (u): {u}")
    print(f"  Matriz pasajeros: {c}")
    print(f"  Matriz disponibilidad: {o}")

    # Verificar factibilidad
    if not verificar_factibilidad(n, m, u, o):
        sys.exit(1)

    # Verificar que la matriz sea simétrica
    if not es_simetrica(c):
        print("La matriz de autobuses tiene que ser simétrica.")
        sys.exit(1)

    if not diagonal_es_cero:
        print("La diagopan principal debe ser todo ceros.")
        sys.exit(1)

    print("El problema es FACTIBLE. Procediendo a generar el archivo de datos y resolverlo...")
    # Generar archivo de datos
    generar_archivo_datos(n, m, u, c, o, ruta_salida)

    # Resolver con GLPK
    modelo = "parte-2-2.mod"
    if not os.path.exists(modelo):
        print(f"Error: El archivo de modelo '{modelo}' no existe.")
        sys.exit(1)
    
    solucion_glpk = resolver_glpk(modelo, ruta_salida)

    if solucion_glpk:
        print("\n--- SOLUCIÓN ÓPTIMA ---")
        valor_objetivo, variables, restricciones = procesar_solucion(solucion_glpk, n, m, u)

        if valor_objetivo is not None:
            print("\nResumen:")
            print(f"\tCoste total mínimo: {valor_objetivo:.2f} €")
            print(f"\tVariables: {variables}")
            print(f"\tRestricciones: {restricciones - 1}")
    else:
        print("No se pudo obtener una solución óptima.")

if __name__ == "__main__":
    main()
