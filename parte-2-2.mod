# Modelo para maximización de la satisfacción de los pasajeros
# Parte 2.2.2

/* Conjuntos */
set AUTOBUSES;
set TALLERES;
set FRANJAS;

/* Parámetros */
param c{AUTOBUSES, AUTOBUSES};
param o{FRANJAS, TALLERES} binary;

/* Variables de decisión */
var x{AUTOBUSES, TALLERES, FRANJAS} binary;

/* Variables auxiliares */
var y{i in AUTOBUSES, j in AUTOBUSES, f in FRANJAS: i < j} binary;

/* Función objetivo */
minimize pasajeros_totales:
    sum{f in FRANJAS} sum{i in AUTOBUSES, j in AUTOBUSES: i < j} c[i,j] * y[i,j,f];

/* Restricciones */
# Todos los autobuses asignados a una franja
s.t. asignacion_autobus {i in AUTOBUSES}:
    sum{t in TALLERES, f in FRANJAS} x[i,t,f] = 1;          

# Los autobuses solo pueden ser asignados en una franja y taller si lo permite la matriz de disponibilidad
s.t. capacidad_franja {t in TALLERES, f in FRANJAS}:
    sum{i in AUTOBUSES} x[i,t,f] <= o[f,t];

# comprueba si el autobús i está en la franja f de algún taller     todos los autobuses tienen que estar asignados -> comprobar
s.t. z_upper1 {i in AUTOBUSES, j in AUTOBUSES, f in FRANJAS: i < j}:
    y[i,j,f] <= sum{t in TALLERES} x[i,t,f];

# comprueba si el autobús j está en la franja f de algún taller
s.t. z_upper2 {i in AUTOBUSES, j in AUTOBUSES, f in FRANJAS: i < j}:
    y[i,j,f] <= sum{t in TALLERES} x[j,t,f];

# si ambos autobuses están en la misma franja f en algún taller (y = 1 en las dos restricciones anteriores), entonces y será 1
s.t. z_lower {i in AUTOBUSES, j in AUTOBUSES, f in FRANJAS: i < j}:
    y[i,j,f] >= sum{t in TALLERES} x[i,t,f] + sum{t in TALLERES} x[j,t,f] - 1;      # si ambos coinciden, 1 + 1 - 1 = 1; si no, al menos uno es 0, y da 0 o negativo

end;