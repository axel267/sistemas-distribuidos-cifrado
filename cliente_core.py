# Proyecto 1 Sistemas Distribuidos - Parte 1 (lectura de imagen y verificacion)

import hashlib
import os
import sys

# formatos que se pueden usar
EXTENSIONES_VALIDAS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp"}


# ---------- inciso b: leer la imagen ----------

def leer_imagen(ruta):
    # regresa la imagen como bytes

    if not os.path.isfile(ruta):
        raise FileNotFoundError("No existe el archivo: " + ruta)

    extension = os.path.splitext(ruta)[1].lower()
    if extension not in EXTENSIONES_VALIDAS:
        raise ValueError("Formato no soportado: " + extension)

    # "rb" porque es binario, si lo abro como texto se corrompe la imagen
    with open(ruta, "rb") as f:
        datos = f.read()

    if len(datos) == 0:
        raise ValueError("El archivo esta vacio")

    return datos


def guardar_imagen(ruta, datos):
    # guarda los bytes que regresan del servidor
    if not datos:
        raise ValueError("No hay bytes para guardar")

    with open(ruta, "wb") as f:
        f.write(datos)


# ---------- inciso g: comparar las imagenes ----------

def calcular_hash(datos):
    return hashlib.sha256(datos).hexdigest()


def verificar_igualdad(original, recibida):
    # compara con hash y tambien byte por byte, las dos tienen que dar igual
    hash_original = calcular_hash(original)
    hash_recibida = calcular_hash(recibida)

    print("--- Verificacion de imagenes ---")
    print("Tamano original:", len(original), "bytes")
    print("Tamano recibida:", len(recibida), "bytes")
    print("SHA-256 original:", hash_original)
    print("SHA-256 recibida:", hash_recibida)

    hashes_iguales = hash_original == hash_recibida
    bytes_iguales = original == recibida  # compara todo el contenido

    if hashes_iguales and bytes_iguales:
        print("Resultado: las imagenes son IGUALES")
        return True

    print("Resultado: las imagenes son DIFERENTES")
    _buscar_diferencia(original, recibida)
    return False


def _buscar_diferencia(original, recibida):
    # solo sirve para depurar, dice donde falla
    if len(original) != len(recibida):
        print("  Los tamanos no coinciden")

    for i, (a, b) in enumerate(zip(original, recibida)):
        if a != b:
            print("  Primera diferencia en el byte", i, ":", a, "vs", b)
            return


# ---------- extra: abrir las imagenes ----------
# necesita: pip install pillow

def mostrar_imagenes(ruta_original, ruta_recibida):
    try:
        from PIL import Image
    except ImportError:
        print("No esta instalado pillow, no se muestran las imagenes")
        return

    Image.open(ruta_original).show()
    Image.open(ruta_recibida).show()


# ---------- pruebas (para probar sin los demas) ----------
# python cliente_core.py mi_imagen.png

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python cliente_core.py <imagen>")
        sys.exit(1)

    original = leer_imagen(sys.argv[1])
    print("Imagen leida:", len(original), "bytes\n")

    # prueba 1: copia igual, debe dar iguales
    print("Prueba 1: copia exacta")
    guardar_imagen("prueba_recibida.png", original)
    verificar_igualdad(original, leer_imagen("prueba_recibida.png"))

    # prueba 2: cambio un byte, debe dar diferentes
    print("\nPrueba 2: un byte cambiado")
    alterada = bytearray(original)
    alterada[len(alterada) // 2] ^= 0xFF
    verificar_igualdad(original, bytes(alterada))
