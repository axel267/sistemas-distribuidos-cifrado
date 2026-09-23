import sys
import os

# Agregamos la ruta principal para poder importar todo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cliente_core import leer_imagen, guardar_imagen, verificar_igualdad
from motor_criptografico import MotorCriptografico
from cliente.cliente_red import enviar_y_recibir_payload

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python prueba_red.py <ruta_imagen> [ip_servidor]")
        print("Ejemplo: python prueba_red.py imagen.png 192.168.1.100")
        sys.exit(1)
        
    ruta_imagen = sys.argv[1]
    # Si pasan una IP como segundo argumento la usamos, si no, usamos localhost
    ip_servidor = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
    
    # Usamos la misma llave que acordó el equipo
    llave_equipo = b'sistemas_dist_26'
    puerto = 65433
    
    print("\n--- INICIANDO CLIENTE COMPLETO ---")
    
    # 1. Persona 1: Lee la imagen
    try:
        bytes_originales = leer_imagen(ruta_imagen)
        print(f"[*] (Persona 1) Imagen leída: {len(bytes_originales)} bytes.")
    except Exception as e:
        print(f"[!] Error leyendo la imagen: {e}")
        sys.exit(1)
        
    # 2. Persona 2: Encripta la imagen
    print(f"[*] (Persona 2) Encriptando con clave: {llave_equipo}...")
    motor = MotorCriptografico(llave_equipo)
    bytes_encriptados = motor.encriptar(bytes_originales)
    print(f"[*] (Persona 2) Datos encriptados, tamaño payload: {len(bytes_encriptados)} bytes.")
    
    # 3. Persona 3: Envía por red (Y aquí responde la Persona 4: el servidor)
    print(f"[*] (Persona 3) Conectando a la red {ip_servidor}:{puerto}...")
    respuesta_red = enviar_y_recibir_payload(ip_servidor, puerto, bytes_encriptados)
    
    if respuesta_red:
        # 4. Persona 1: Guarda la imagen desencriptada recibida y verifica igualdad
        print(f"[*] (Persona 1) Recibidos {len(respuesta_red)} bytes de la red. Guardando...")
        ruta_salida = "imagen_procesada_red.png"
        guardar_imagen(ruta_salida, respuesta_red)
        
        print("[*] (Persona 1) Comprobando si el servidor nos devolvió la imagen exacta:")
        verificar_igualdad(bytes_originales, respuesta_red)
    else:
        print("[!] La comunicación por red falló.")
        
    print("--- FIN DEL CLIENTE ---")
