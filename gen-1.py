"""
Script para generar el archivo de datos y resolver el problema de
minimización de impacto de averías.
Parte 2.2.1
"""

import sys

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
        distancias = map(float, lineas[2].split())
        if len(distancias) != m:
            raise ValueError(f"Se esperaban {m} distancias, pero se encontraron {len(distancias)}.")

        # Leer pasajeros
        pasajeros = map(int, lineas[3].split())
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
        
        print(f"Archivo de datos generado: {ruta_salida}")
    
    except Exception as e:
        print(f"Error generando el archivo de datos: {e}")
        sys.exit(1)
