import sys
# importamos 1
from cliente_core import leer_imagen, guardar_imagen, verificar_igualdad
# Importamos 2
from motor_criptografico import MotorCriptografico

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python prueba_integracion.py <ruta_imagen>")
        sys.exit(1)
    
    ruta_imagen = sys.argv[1]
    llave_equipo = b'sistemas_dist_26' # Llave de 16 bytes (AES-128)
    
    # 1. LECTURA
    bytes_originales = leer_imagen(ruta_imagen)
    print(f"[*] Imagen original leída: {len(bytes_originales)} bytes")

    # 2. CIFRADO
    motor = MotorCriptografico(llave_equipo)
    bytes_cifrados = motor.encriptar(bytes_originales)
    print(f"[*] Imagen cifrada generada: {len(bytes_cifrados)} bytes")

    # --- Aquí entraría la red TCP (Axel y Xotla, borren si quieren esto, solo es prueba) ---
    # Simulamos que el servidor recibe los bytes cifrados y los desencripta
    
    # 3. DESCIFRADO
    bytes_recuperados = motor.desencriptar(bytes_cifrados)
    print(f"[*] Imagen desencriptada recuperada: {len(bytes_recuperados)} bytes")

    # 4. GUARDADO Y VERIFICACIÓN
    ruta_salida = "imagen_procesada.png"
    guardar_imagen(ruta_salida, bytes_recuperados)
    verificar_igualdad(bytes_originales, bytes_recuperados)