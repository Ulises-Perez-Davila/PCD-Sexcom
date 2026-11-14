import numpy as np
import json
import time

RUTA_CSV    = "../../datos/ventas_online-ruido_100000.csv"
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


def estadisticas(columna, arr_np):
    '''
        Pide la columna ya limpia para numpy, regresa las 8 estadisticas
    '''
    n = int(len(arr_np))
    if n <=0:
        return {
            "columna": columna,
            "n_valores_validos": 0,
            "media": None,
            "desviacion_estandar": None,
            "minimo": None,
            "maximo": None,
            "mediana": None,
            "percentil_25": None,
            "percentil_75": None,
        }
    media = float(np.mean(arr_np))
    desv = float(np.std(arr_np))
    maximo = float(np.nanmax(arr_np))
    minimo = float(np.nanmin(arr_np))
    mediana = float(np.median(arr_np))
    per_25=float(np.percentile(arr_np, 25))
    per_75=float(np.percentile(arr_np, 75))

    return {
        "columna": columna,
        "n_valores_validos": n,
        "media": round(media, 2),
        "desviacion_estandar": round(desv, 2),
        "minimo": round(minimo, 2),
        "maximo": round(maximo, 2),
        "mediana": round(mediana, 2),
        "percentil_25": round(per_25, 2),
        "percentil_75": round(per_75, 2),
    }
#paso 6

def outliers(arreglo, n_filas):

    if int(n_filas) <= 0 or len(arreglo) <= 0:
        return {
            "metodo": "desviacion_estandar_3",
            "limite_inferior": None,
            "limite_superior": None,
            "n_outliers": 0,
            "porcentaje": 0.0,
            "outliers_minimo": None,
            "outliers_maximo": None
        }

    media = arreglo.mean()
    std = arreglo.std()
    k=3

    inferior = media - k * std
    superior = media + k * std
    marcados = arreglo[(arreglo < inferior) | (arreglo > superior)]
    n = int(len(marcados))

    if n == 0:
        out_min = None
        out_max = None
        porcentaje = 0.0
    else:
        out_min = round(float(marcados.min()), 2)
        out_max = round(float(marcados.max()), 2)
        porcentaje = round(float(n / n_filas * 100), 2)

    return {
        "metodo": "desviacion_estandar_3",
        "limite_inferior": round(float(inferior), 2),
        "limite_superior": round(float(superior), 2),
        "n_outliers": n,
        "porcentaje": porcentaje,
        "outliers_minimo": out_min,
        "outliers_maximo": out_max
    }

def tiempos(arreglo):
    n = len(arreglo)

    #python puro
    inicio = time.perf_counter()
    total_py = 0.0
    for v in arreglo:
        total_py += v
    media_py = total_py / n

    sumatoria = 0.0
    for x in arreglo:
        sumatoria += (x - media_py) ** 2
    des_py = (sumatoria / n) ** 0.5
    t_py = time.perf_counter() - inicio

    #numpy
    inicio = time.perf_counter()
    media_np = np.mean(arreglo)
    desv_np = np.std(arreglo)
    t_np = time.perf_counter() - inicio

    if not (np.isclose(media_py, media_np) and np.isclose(des_py, desv_np)):
        ''' Si no se parecen los resultados'''
        return "Hubo un error, no se pudo calcular"

    red_tiempos=7
    t_np_red = round(float(t_np), red_tiempos)
    factor = None if t_np_red == 0.0 else round(float(t_py / t_np), 2)

    return {
        "n_filas": int(n),
        "tiempo_bucle_python_seg": round(float(t_py), red_tiempos),
        "tiempo_numpy_seg": t_np_red,
        "factor_velocidad": factor,
        "operacion_medida": "calcular media y desviacion estandar"
    }

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
        return outliers(columna, len(columna))

    def tiempos(self, columna):
        return tiempos(columna);
    
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

  "benchmark": d.tiempos(n1)
}


with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("Archivo escrito.")

json.dumps(resultado, indent=2, ensure_ascii=False)