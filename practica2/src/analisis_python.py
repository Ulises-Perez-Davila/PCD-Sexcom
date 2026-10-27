import json

RUTA_CSV    = "../../datos/ventas_online-ruido_100000.csv"
RUTA_SALIDA = "../resultados/analisis_python.json"

TEMA       = "ventas online"
PAREJA     = "Cazadores de bandides"
CATEGORICA = "producto"
NUMERICA   = "monto_venta"

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


datos = leer_csv(RUTA_CSV)


#paso 2
def a_float(texto):
    """Intenta convertir a float. Devuelve None si no se puede."""
    try:
        return float(texto)
    except (ValueError, TypeError):
        return None



def columna_numerica(datos, columna):
    """Extrae una columna como lista de floats, descartando lo no convertible."""
    crudos = map(lambda fila: fila.get(columna, ""), datos)
    convertidos = map(a_float, crudos)
    return list(filter(lambda x: x is not None, convertidos))


montos = columna_numerica(datos, "monto_venta")


#paso 3
def valores_unicos(datos, columna):
    """Set de valores distintos de una columna, sin contar vacios."""
    valores = map(lambda fila: fila.get(columna, "").strip(), datos)
    return set(filter(lambda v: v != "", valores))


def conteo_por_categoria(datos, columna):
    """Diccionario {valor: cuantas veces aparece}, sin contar vacios."""
    conteo = {}
    for fila in datos:
        valor = fila.get(columna, "").strip()
        if valor == "":
            continue
        conteo[valor] = conteo.get(valor, 0) + 1
    return conteo



def estadisticas(datos, columna):
    crudos = map(lambda fila: fila.get(columna, "").strip(), datos)

    validos = filter(lambda x: x != "" and a_float(x) is not None, crudos)
    numeros = list(map(float, validos))

    if not numeros:
        return {
            "columna": columna,
            "n_valores_validos": 0,
            "minimo": None,
            "maximo": None,
            "promedio": None,
            "mediana": None
        }

    ordenados = sorted(numeros)
    n = len(ordenados)
    mitad = n // 2

    if n % 2 == 1:
        mediana = ordenados[mitad]
    else:
        mediana = (ordenados[mitad - 1] + ordenados[mitad]) / 2

    return {
        "columna": columna,
        "n_valores_validos": n,
        "minimo": min(numeros),
        "maximo": max(numeros),
        "promedio": round(sum(numeros) / n, 2),
        "mediana": round(mediana, 2)
    }


def percentil(numeros, p):
    """Percentil aproximado por posicion, como lo pide la Practica 2."""
    if not numeros:
        return None
    ordenados = sorted(numeros)
    pos = int(p * len(ordenados))
    pos = min(pos, len(ordenados) - 1)    # no pasarse del final
    return ordenados[pos]


# Paso 4
montos = columna_numerica(datos, NUMERICA)

umbral = percentil(montos, 0.9)

if umbral is not None:
    caros = list(filter(
        lambda fila: a_float(fila.get(NUMERICA, "")) is not None
        and a_float(fila.get(NUMERICA, "")) > umbral,
        datos
    ))
else:
    caros = []

if montos:
    porcentaje = round(100 * len(caros) / len(montos), 2)
else:
    porcentaje = 0.0

#paso 5
class Dataset:
    """Un dataset del curso, leido desde un CSV separado por '|'."""

    def __init__(self, ruta, separador="|"):
        self.ruta = ruta
        self.filas = leer_csv(ruta, separador)
        self.columnas = list(self.filas[0].keys()) if self.filas else []

    # --- acceso a columnas ---

    def columna(self, nombre):
        """La columna como lista de strings, tal cual viene del archivo."""
        return [fila.get(nombre, "") for fila in self.filas]

    def numerica(self, nombre):
        """La columna como lista de floats, descartando lo no convertible."""
        return columna_numerica(self.filas, nombre)

    # --- analisis ---

    def valores_unicos(self, columna):
        return valores_unicos(self.filas, columna)

    def conteo(self, columna):
        return conteo_por_categoria(self.filas, columna)

    def mas_frecuente(self, columna):
        c = self.conteo(columna)
        if not c:
            return None, 0
        valor = max(c, key=c.get)
        return valor, c[valor]

    def top_3(self, columna):
        #primero ordenar alfabeticamente
        dicci = dict(sorted(self.conteo(columna).items(), key=lambda x: x[0]))
        #ahora ordenar por aparicion
        dicci = dict(sorted(dicci.items(), key=lambda x: x[1], reverse=True))
        
        final = []
        for key, valor in dicci.items():
            final.append({"valor": key, "conteo": valor})

            # Tomar solo los primeros 3
            if len(final) == 3:
                break
        return final

    def estadisticas(self, columna):
        return estadisticas(self.filas, columna)

    def contar_vacias(self):
        """Celdas vacias por columna."""
        return {col: sum(1 for fila in self.filas
                         if fila.get(col, "").strip() == "")
                for col in self.columnas}
   
    def filtrar(self, condicion):
        """Filas que cumplen una condicion. 'condicion' es una funcion
        que recibe una fila (dict) y devuelve True o False."""
        return list(filter(condicion, self.filas))

    # --- metodos especiales ---

    def __len__(self):
        return len(self.filas)

    def __str__(self):
        return f"Dataset({self.ruta}: {len(self.filas)} filas, {len(self.columnas)} columnas)"


d = Dataset(RUTA_CSV)

#paso 6

mas_frecuente, veces = d.mas_frecuente("producto")
montos = d.numerica("monto_venta")

resultado = {
    "archivo": "ventas_online-ruido_100000.csv",
    "pareja": PAREJA,
    "seed": seed,
    "valores_unicos_categorica": {
        "columna": "producto",
        "n_valores_unicos": len(d.valores_unicos("producto")),
        "valores": sorted(d.valores_unicos("producto")),
    },
    "conteo_por_categoria": d.conteo("producto"),
    "categoria_mas_frecuente": {"valor": mas_frecuente, "conteo": veces},
    "top_3_categorias": d.top_3("producto"),
    "estadisticas_numerica_1": d.estadisticas("monto_venta"),
    "estadisticas_numerica_2": d.estadisticas("minutos_en_sitio"),
    "promedio_por_categoria": {},
    "filtrado": {
        "condicion": "monto_venta > " + str(umbral),
        "umbral_usado": umbral,
        "n_registros_que_cumplen": len(caros),
        "porcentaje": round(100 * len(caros) / len(montos), 2),
    },
}

with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("Archivo escrito.")

json.dumps(resultado, indent=2, ensure_ascii=False)