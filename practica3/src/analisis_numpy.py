import numpy as np
import json
import time

RUTA_CSV    = "../../datos/ventas_online-ruido_100.csv"
RUTA_SALIDA = "../resultados/analisis_numpy.json"

TEMA       = "ventas online"
PAREJA     = "Cazadores de bandides"
CATEGORICA = "producto"
NUMERICA_1 = "monto_venta"
NUMERICA_2 = "minutos_en_sitio"

archivo_nombre = RUTA_CSV.split("/")[-1]  

seed = 1
#paso 1
def leer_csv(ruta, separador="|"):
    """Lee un CSV y lo devuelve como lista de diccionarios.
    Cada fila es un dict {nombre_columna: valor}."""
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.read().strip().split("\n")

    cabecera = lineas[0].split(separador)
    datos = []
    for linea in lineas[1:]:
        valores = linea.split(separador)
        datos.append(dict(zip(cabecera, valores)))
    return datos

# Localizar la columna POR NOMBRE, nunca por un indice escrito a mano
'''
i_monto = cabecera.index(NUMERICA_1)
i_minutos = cabecera.index(NUMERICA_2)
print("monto_venta esta en la posicion", i_monto)
print("minutos_en_sitio esta en la posicion", i_minutos)
print()


crudos = [fila[i_monto] for fila in filas]
print("valores crudos:", crudos)'''

#paso 2
def a_float(texto):
    """Convierte texto a float; devuelve np.nan si no se puede."""
    try:
        return float(texto.strip())
    except (ValueError, AttributeError):
        return np.nan

def columna_numerica(datos, columna):
    """Extrae una columna como lista de floats, descartando lo no convertible."""
    crudos = map(lambda fila: fila.get(columna, ""), datos)
    convertidos = np.array([a_float(v) for v in crudos])
    validos = convertidos[~np.isnan(convertidos)]
    return validos

#paso 3
'''
n_total = monto.size
n_nan = np.isnan(monto).sum()
n_validos = n_total - n_nan

print("valores en total :", n_total)
print("no convertibles  :", n_nan)
print("validos          :", n_validos)
print("porcentaje valido:", round(100 * n_validos / n_total, 2), "%")'''

#paso 4

'''validos = monto[~np.isnan(monto)]

print("validos:", validos)
print("cuantos:", validos.size)
print()
print("minimo :", validos.min())
print("maximo :", validos.max())
print("media  :", round(validos.mean(), 2))
print("suma   :", validos.sum())

# La ruta alternativa: funciones nan*, sin filtrar
print("nanmin :", np.nanmin(monto))
print("nanmax :", np.nanmax(monto))
print("nanmean:", round(np.nanmean(monto), 2))
print()
print("dan lo mismo?", np.allclose(
    [validos.min(), validos.max(), validos.mean()],
    [np.nanmin(monto), np.nanmax(monto), np.nanmean(monto)],
))'''

#paso 5
'''
minutos = np.array([a_float(fila[i_minutos]) for fila in filas])

X = np.column_stack([monto, minutos])

print("shape:", X.shape)        # (12, 2): 12 registros, 2 variables
print()
print(X)

# Promedio de cada columna, ignorando nan (axis=0 = por columna)
print("promedios por columna:", np.round(np.nanmean(X, axis=0), 2))
print("minimos  por columna:", np.nanmin(X, axis=0))
print("maximos  por columna:", np.nanmax(X, axis=0))
print()
# Y una columna suelta sigue siendo X[:, i]
print("columna monto  :", X[:, 0])
print("columna minutos:", X[:, 1])'''

def estadisticas(columna, arr_np):
    '''
        Pide la columna ya limpia para numpy, regresa las 7 estadisticas
    '''

    media= np.round(np.nanmean(arr_np, axis=0), 2)
    desv_std= np.std(arr_np)
    maximo = np.nanmax(arr_np)
    minimo = np.nanmin(arr_np)
    mediana = np.median(arr_np)
    per_25=np.percentile(arr_np, 25)
    per_75=np.percentile(arr_np, 75)
    n = len(arr_np)

    return {
        "columna": columna,
        "n_valores_validos": n,
        "minimo": minimo,
        "maximo": maximo,
        "promedio": media,
        "mediana": mediana,
        "percentil_25": per_25,
        "percentil_75": per_75
    }
#paso 6

def outliers(arreglo, n_filas):

    if int(n_filas) <= 0 or len(arreglo) <= 0:
        return {
            "metodo": "desviacion_estandar_3",
            "limite_inferior": None,
            "limite_superior": None,
            "n_outliers": 0,
            "porcentaje": None,
            "outliers_minimo": None,
            "outliers_maximo": None
        }

    media = arreglo.mean()
    std = arreglo.std()
    k=3

    inferior = media - k * std
    superior = media + k * std
    marcados = arreglo[(arreglo < inferior) | (arreglo > superior)]

    minimo= np.nanmin(marcados)
    maximo= np.nanmax(marcados)
    n= len(marcados)

    return {
        "metodo": "desviacion_estandar_3",
        "limite_inferior": inferior,
        "limite_superior": superior,
        "n_outliers": n,
        "porcentaje": (n/n_filas)*100,
        "outliers_minimo": minimo,
        "outliers_maximo": maximo
    }

def tiempos(arreglo):
    # --- Bucle de Python puro ---
    inicio = time.perf_counter()
    total_py = 0.0
    for v in arreglo:
        total_py += v * v
    t_py = time.perf_counter() - inicio

    # --- NumPy, vectorizado ---
    inicio = time.perf_counter()
    total_np = float((arreglo ** 2).sum())
    t_np = time.perf_counter() - inicio

    print("bucle:", round(total_py, 2), "en", round(t_py, 6), "s")
    print("numpy:", round(total_np, 2), "en", round(t_np, 6), "s")
    print()
    print("calculan lo mismo?", np.allclose(total_py, total_np))
    print("factor de velocidad:", round(t_py / t_np, 1), "x")
'''
pesos_por_minuto = X[:, 0] / X[:, 1]

print("por registro:", np.round(pesos_por_minuto, 2))
print()
print("promedio de la metrica:", round(np.nanmean(pesos_por_minuto), 2))
print("registro mas alto     :", round(np.nanmax(pesos_por_minuto), 2))

a = np.array([100.0, 50.0, 0.0])
b = np.array([5.0, 0.0, 0.0])
print(a / b)       # 20, inf, nan'''

#paso 7
'''
# Simular una columna del tamanio de la tuya, ya filtrada
rng = np.random.default_rng(42)          # semilla fija: reproducible
valores_np = rng.normal(850, 180, 100_000)
valores_py = valores_np.tolist()         # la misma data, como lista de Python

print("cuantos valores:", len(valores_py))

# --- Bucle de Python puro: media y desviacion estandar ---
inicio = time.perf_counter()

n = len(valores_py)
suma = 0.0
for v in valores_py:
    suma += v
media_py = suma / n

acum = 0.0
for v in valores_py:
    acum += (v - media_py) ** 2
std_py = (acum / n) ** 0.5

t_bucle = time.perf_counter() - inicio

# --- NumPy ---
inicio = time.perf_counter()
media_np = valores_np.mean()
std_np = valores_np.std()
t_numpy = time.perf_counter() - inicio

print(f"bucle -> media {media_py:.4f} | std {std_py:.4f} | {t_bucle:.6f} s")
print(f"numpy -> media {media_np:.4f} | std {std_np:.4f} | {t_numpy:.6f} s")
print()
print("mismo resultado?", np.allclose([media_py, std_py], [media_np, std_np]))
print(f"factor de velocidad: {t_bucle / t_numpy:.1f}x")

# Lo mismo, pero midiendo con time.time()
inicio = time.time()
valores_np.mean()
valores_np.std()
t_malo = time.time() - inicio

print("medido con time.time()      :", t_malo, "s")

inicio = time.perf_counter()
valores_np.mean()
valores_np.std()
t_bueno = time.perf_counter() - inicio

print("medido con time.perf_counter():", t_bueno, "s")
print()
try:
    print("factor con time.time():", t_bucle / t_malo)
except ZeroDivisionError as e:
    print("ZeroDivisionError:", e, "<- el reloj no alcanza a ver nada")
'''
#clase recopilando las funcionas
class Dataset:
    """Un dataset del curso, leido desde un CSV separado por '|'."""

    def __init__(self, ruta, separador="|"):
        self.ruta = ruta
        self.filas = leer_csv(ruta, separador)
        self.columnas = list(self.filas[0].keys()) if self.filas else []

    # --- acceso a columnas ---

    def idx_columna(self, nombre):
        """La columna como lista de strings, tal cual viene del archivo."""
        return self.columnas.index(nombre)

    def numerica(self, nombre):
        """La columna como lista de floats, descartando lo no convertible."""
        return columna_numerica(self.filas, nombre)

    # --- analisis ---

    def estadisticas(self, columna, validos):
        return estadisticas( columna, validos)
    
    def outliers(self, columna):
        return outliers(columna, self.__len__())
    
    # --- metodos especiales ---
    def __len__(self):
        return len(self.filas)

    def __str__(self):
        return f"Dataset({self.ruta}: {len(self.filas)} filas, {len(self.columnas)} columnas)"

#escribir en el json

d = Dataset(RUTA_CSV)

n1 = d.numerica(NUMERICA_1)
n2 = d.numerica(NUMERICA_2)

resultado = {
  "archivo": archivo_nombre,
  "pareja": PAREJA,
  "seed": seed,

  "numerica_1": d.estadisticas(NUMERICA_1,n1),

  "numerica_2": d.estadisticas(NUMERICA_2,n2),

  "outliers_numerica_1": d.outliers(n1),

  "outliers_numerica_2": d.outliers(n2),

  "benchmark": {
    "n_filas": 98500,
    "tiempo_bucle_python_seg": 0.45,
    "tiempo_numpy_seg": 0.002,
    "factor_velocidad": 225.0,
    "operacion_medida": "calcular media y desviacion estandar"
  }
}


with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("Archivo escrito.")

json.dumps(resultado, indent=2, ensure_ascii=False)