# Modelo para minimización del impacto de averías
# Parte 2.2.1

/* Conjuntos */
set AUTOBUSES; # Conjunto de autobuses
set FRANJAS;   # Conjunto de franjas

/* Parámetros */
param kd;           # Coste por kilómetro
param kp;           # Penalización por pasajero
param d{AUTOBUSES}; # Distancia (km) de cada autobús al taller
param p{AUTOBUSES}; # Número de pasajeros de cada autobús

/* Variables de decisión */
var x{AUTOBUSES, FRANJAS} binary;
# x[i,j] = 1 si el autobús i se asigna a la franja j, 0 en caso contrario

var y{AUTOBUSES} binary;
# y[i] = 1 si el autobús i no se asigna a ninguna franja, 0 en caso contrario

/* Función objetivo */
minimize coste_total:
    sum{i in AUTOBUSES, j in FRANJAS} kd * d[i] * x[i,j] +
    sum{i in AUTOBUSES} kp * p[i] * y[i];

/* Restricciones */

# Cada franja puede tener como máximo un autobús
subject to una_franja_maximo {j in FRANJAS}:
    sum{i in AUTOBUSES} x[i,j] <= 1;

# Cada autobús debe estar asignado a una franja o no asignado
subject to asignacion_autobus {i in AUTOBUSES}:
    sum{j in FRANJAS} x[i,j] + y[i] = 1;
