RUTA_CSV    = "../../datos/ventas_online-ruido_100000.csv"
RUTA_SALIDA = "../src/resumen.txt"

TEMA       = "ventas online"
PAREJA     = "Los cazadores de bandides"
CATEGORICA = "producto"
NUMERICA   = "id"

archivo_nombre = RUTA_CSV.split("/")[-1] 

# ---------- Obtener la seed desde el nombre del archivo ----------
# "ventas_online-ruido_100.csv"  ->  seed = "100"
seed = "desconocida"
for parte in archivo_nombre.replace(".csv", "").split("_"):
    if parte.isdigit():
        seed = parte
        break

#leer archivo
with open(RUTA_CSV, "r", encoding="utf-8") as f:
    lineas = [ln.rstrip("\n") for ln in f if ln.strip() != ""]

cabecera = [c.strip() for c in lineas[0].split("|")]
filas    = [ln.split("|") for ln in lineas[1:]]

n_filas    = len(filas)
n_columnas = len(cabecera)
primeras5  = filas[:5]

# celdas vacias
vacias_por_col = [0] * n_columnas
total_vacias   = 0
for fila in filas:
    for i in range(n_columnas):
        val = fila[i] if i < len(fila) else ""
        if val.strip() == "":
            vacias_por_col[i] += 1
            total_vacias      += 1

# texto de la salida
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
out.append(" | ".join(cabecera))
for fila in primeras5:
    vals = [fila[i].strip() if i < len(fila) else "" for i in range(n_columnas)]
    out.append(" | ".join(vals))
out.append("")
out.append(f"--- Columna categórica: {CATEGORICA} ---")
out.append("")
out.append(f"--- Columna numérica: {NUMERICA} ---")
out.append("")
out.append("--- Calidad de datos ---")
out.append(f"Celdas vacías totales: {total_vacias}")
out.append("Celdas vacías por columna:")
for i, nombre in enumerate(cabecera):
    out.append(f"  {nombre}: {vacias_por_col[i]}")

# escribir resultados
with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")

print(f"Resumen generado")