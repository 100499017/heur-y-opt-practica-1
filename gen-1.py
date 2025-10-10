"""
Script para generar el archivo de datos y resolver el problema de
minimización de impacto de averías.
Parte 2.2.1
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

        if len(lineas) != 4:
            raise ValueError("El archivo de entrada no tiene el formato correcto")
        
        # Leer n y m
        n, m = map(int, lineas[0].split())

        # Leer kd y kp
        kd, kp = map(float, lineas[1].split())

        # Leer distancias
        distancias = list(map(float, lineas[2].split()))
        if len(distancias) != m:
            raise ValueError(f"Se esperaban {m} distancias, pero se encontraron {len(distancias)}.")

        # Leer pasajeros
        pasajeros = list(map(int, lineas[3].split()))
        if len(pasajeros) != m:
            raise ValueError(f"Se esperaban {m} valores de pasajeros, pero se encontraron {len(pasajeros)}.")
        
        return n, m, kd, kp, distancias, pasajeros
    
    except Exception as e:
        print(f"Error leyendo el archivo de entrada: {e}")
        sys.exit(1)

def generar_archivo_datos(n, m, kd, kp, distancias, pasajeros, ruta_salida):
    """Genera el archivo .dat"""
    try:
        with open(ruta_salida, 'w') as f:
            # Escribir conjuntos
            f.write(f"set AUTOBUSES :=")
            for i in range(m):
                f.write(f" a{i+1}")
            f.write(";\n")

            f.write(f"set FRANJAS :=")
            for i in range(n):
                f.write(f" f{i+1}")
            f.write(";\n\n")

            # Escribir parámetros
            f.write(f"param kd := {kd};\n")
            f.write(f"param kp := {kp};\n\n")

            # Escribir distancias
            f.write("param d :=\n")
            for i in range(m):
                f.write(f"\ta{i+1} {distancias[i]}")
                if i < m - 1:
                    f.write("\n")
                else:
                    f.write(";\n")
            f.write("\n")

            # Escribir pasajeros
            f.write("param p :=\n")
            for i in range(m):
                f.write(f"\ta{i+1} {pasajeros[i]}")
                if i < m - 1:
                    f.write("\n")
                else:
                    f.write(";\n")
        
        print(f"\nArchivo de datos generado: {ruta_salida}")
    
    except Exception as e:
        print(f"Error generando el archivo de datos: {e}")
        sys.exit(1)

def resolver_glpk(modelo, datos, salida_glpk="solucion-1.txt"):
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

def procesar_solucion(solucion_glpk, n, m):
    """Procesa la solución de GLPK y la muestra en el formato requerido"""
    try:
        lineas = solucion_glpk.split('\n')

        # Buscar información de la solución
        valor_objetivo = None
        variables = 0
        restricciones = 0

        asignaciones = {}
        autobuses_no_asignados = []

        for linea in lineas:
            if "Objective:" in linea:
                partes = linea.split()
                if len(partes) >= 4:
                    valor_objetivo = float(partes[3])
                continue
            
            # Buscar variables de asignación x
            if "x[" in linea and " 1" in linea:
                partes = linea.split()
                if len(partes) >= 4:
                    if partes[3] == '1':
                        var_name = partes[1]
                        # Extraer autobús y franja
                        contenido = var_name.split('[')[1].split(']')[0]
                        autobus, franja = contenido.split(',')
                        asignaciones[autobus] = franja
                continue
            
            # Buscar variables de no asignación y
            if "y[" in linea and "1" in linea:
                partes = linea.split()
                if len(partes) >= 4:
                    if partes[3] == '1':
                        var_name = partes[1]
                        if "y[" in var_name:
                            autobus = var_name.split('[')[1].split(']')[0]
                            autobuses_no_asignados.append(autobus)
        
        # Contar variables y restricciones (estimación basada en el modelo)
        variables = m * n + m  # x[i,j] + y[i]
        restricciones = n + m  # restricciones de franjas + autobuses
        
        # Mostrar resultados en el formato requerido
        print(f"{valor_objetivo} {variables} {restricciones}")
        
        # Mostrar asignaciones
        for autobus in sorted(asignaciones.keys()):
            print(f"Autobús {autobus} asignado a franja {asignaciones[autobus]}")
        
        for autobus in sorted(autobuses_no_asignados):
            print(f"Autobús {autobus} no asignado")
            
        return valor_objetivo, variables, restricciones
    
    except Exception as e:
        print(f"Error procesando la solución: {e}")
        return None

def main():
    if len(sys.argv) != 3:
        print("Uso: ./gen-1.py fichero-entrada fichero-salida")
        sys.exit(1)
    
    ruta_entrada = sys.argv[1]
    ruta_salida = sys.argv[2]

    # Verificar que existe el archivo de entrada
    if not os.path.exists(ruta_entrada):
        print(f"Error: El archivo de entrada '{ruta_entrada}' no existe")
        sys.exit(1)
    
    # Leer datos de entrada
    print(f"Leyendo archivo de entrada: {ruta_entrada}")
    n, m, kd, kp, distancias, pasajeros = leer_archivo_entrada(ruta_entrada)

    print(f"Parámetros leídos:")
    print(f"  Franjas (n): {n}")
    print(f"  Autobuses (m): {m}")
    print(f"  kd: {kd}")
    print(f"  kp: {kp}")
    print(f"  Distancias: {distancias}")
    print(f"  Pasajeros: {pasajeros}")

    # Generar archivo de datos
    generar_archivo_datos(n, m, kd, kp, distancias, pasajeros, ruta_salida)

    # Resolver con GLPK
    modelo = "parte-2-1.mod"
    if not os.path.exists(modelo):
        print(f"Error: El archivo de modelo '{modelo}' no existe.")
        sys.exit(1)
    
    solucion_glpk = resolver_glpk(modelo, ruta_salida)

    if solucion_glpk:
        print("\n--- SOLUCIÓN ÓPTIMA ---")
        valor_objetivo, variables, restricciones = procesar_solucion(solucion_glpk, n, m)

        if valor_objetivo is not None:
            print("\nResumen:")
            print(f"\tCoste total mínimo: {valor_objetivo:.2f} €")
            print(f"\tVariables: {variables}")
            print(f"\tRestricciones: {restricciones}")
    else:
        print("No se pudo obtener una solución óptima.")

if __name__ == "__main__":
    main()
