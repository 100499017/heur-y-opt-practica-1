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
s.t. asignacion_autobus {i in AUTOBUSES}:
    sum{t in TALLERES, f in FRANJAS} x[i,t,f] = 1;          

s.t. capacidad_franja {t in TALLERES, f in FRANJAS}:
    sum{i in AUTOBUSES} x[i,t,f] <= o[f,t];
 
s.t. y_autobus_i_franja {i in AUTOBUSES, j in AUTOBUSES, f in FRANJAS: i < j}:
    y[i,j,f] <= sum{t in TALLERES} x[i,t,f];

s.t. y_autobus_j_franja {i in AUTOBUSES, j in AUTOBUSES, f in FRANJAS: i < j}:
    y[i,j,f] <= sum{t in TALLERES} x[j,t,f];

s.t. y_comparten_franja {i in AUTOBUSES, j in AUTOBUSES, f in FRANJAS: i < j}:
    y[i,j,f] >= sum{t in TALLERES} x[i,t,f] + sum{t in TALLERES} x[j,t,f] - 1;

end;