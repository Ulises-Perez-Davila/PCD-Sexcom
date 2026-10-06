RUTA_CSV    = "../../datos/ventas_online-ruido_100000.csv"
RUTA_SALIDA = "../resultados/resumen.txt"

TEMA       = "ventas online"
PAREJA     = "Cazadores de bandides"
CATEGORICA = "producto"
NUMERICA   = "minutos_en_sitio"

archivo_nombre = RUTA_CSV.split("/")[-1]  

seed = 1

with open(RUTA_CSV, "r", encoding="utf-8") as f:
    lineas = [ln.rstrip("\n") for ln in f if ln.strip() != ""]

cabecera = [c.strip() for c in lineas[0].split("|")]
filas    = [ln.split("|") for ln in lineas[1:]]

n_filas    = len(filas) - 1
n_columnas = len(cabecera)
primeras5  = filas[:5]

#columnas categorica
idx_cat = cabecera.index(CATEGORICA)
conteo  = {}
for fila in filas:
    val = fila[idx_cat].strip() if idx_cat < len(fila) else ""
    if val != "":
        conteo[val] = conteo.get(val, 0) + 1

n_unicos = len(conteo)
if conteo:
    valor_top, conteo_top = max(conteo.items(), key=lambda kv: kv[1])
else:
    valor_top, conteo_top = "", 0

idx_num = cabecera.index(NUMERICA)
valores = []
for fila in filas:
    val = fila[idx_num].strip() if idx_num < len(fila) else ""
    if val == "":
        continue
    try:
        valores.append(float(val))
    except ValueError:
        pass

n_validos = len(valores)
minimo = min(valores) if valores else 0
maximo = max(valores) if valores else 0

vacias_por_col = [0] * n_columnas
total_vacias   = 0
for fila in filas:
    for i in range(n_columnas):
        val = fila[i] if i < len(fila) else ""
        if val.strip() == "":
            vacias_por_col[i] += 1
            total_vacias      += 1

out = []
out.append("=== RESUMEN DEL DATASET ===")
out.append(f"Archivo: {archivo_nombre}")
out.append(f"Pareja: {PAREJA}")
out.append(f"Seed: {seed}")
out.append("")
out.append("--- Dimensiones ---")
out.append(f"Filas: {n_filas}")
out.append(f"Columnas: {n_columnas}")
out.append(f"Nombres de columnas: {', '.join(cabecera)}")
out.append("")
out.append("--- Primeras 5 filas ---")

anchos = []
for i in range(n_columnas):
    max_ancho = len(cabecera[i])
    for fila in primeras5:
        val = fila[i].strip() if i < len(fila) else ""
        max_ancho = max(max_ancho, len(val))
    anchos.append(max_ancho)

out.append(" | ".join(cabecera[i].ljust(anchos[i]) for i in range(n_columnas)))

for fila in primeras5:
    vals = [fila[i].strip() if i < len(fila) else "" for i in range(n_columnas)]
    out.append(" | ".join(vals[i].ljust(anchos[i]) for i in range(n_columnas)))

out.append("")
out.append(f"--- Columna categórica: {CATEGORICA} ---")
out.append(f"Valores únicos: {n_unicos}")
out.append(f"Valor más frecuente: {valor_top} ({conteo_top} apariciones)")
out.append("")
out.append(f"--- Columna numérica: {NUMERICA} ---")
out.append(f"Valores válidos (no vacíos): {n_validos}")
out.append(f"Mínimo: {minimo}")
out.append(f"Máximo: {maximo}")
out.append("")
out.append("--- Calidad de datos ---")
out.append(f"Celdas vacías totales: {total_vacias}")
out.append("Celdas vacías por columna:")
for i, nombre in enumerate(cabecera):
    out.append(f"  {nombre}: {vacias_por_col[i]}")

# poner resultados en el txt
with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")

print(f"Resumen generado")
print(">>> Estoy ejecutando:", __file__)
print(">>> Escribiendo en:", RUTA_SALIDA)
print(">>> Leyendo de:   ", RUTA_CSV)