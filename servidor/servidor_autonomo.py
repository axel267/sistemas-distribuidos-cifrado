import socket
import sys
import os

# Aseguramos que se pueda importar motor_criptografico desde el directorio padre
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motor_criptografico import MotorCriptografico

def iniciar_servidor(host='0.0.0.0', puerto=65432, clave_secreta=b'llave_secreta_16'):
    """
    Levanta un servicio para operar autónomamente en un ciclo de escucha infinito.
    Recibe paquetes, los desencripta y los devuelve al cliente.
    """
    # 1. Inicializar el motor criptográfico de la Persona 2
    # La llave DEBE ser la misma que usa el cliente (16, 24 o 32 bytes)
    motor = MotorCriptografico(clave_secreta)
    
    # 2. Configuración de la infraestructura del servidor (Sockets)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Para evitar errores de puerto ocupado
    
    # 3. Escuchar en el puerto especificado
    servidor.bind((host, puerto))
    servidor.listen(5)
    
    # TRUCO PARA WINDOWS: Le damos un timeout de 1 segundo al servidor general.
    # Si no hacemos esto, Windows bloquea el programa eternamente y bloquea el Ctrl+C.
    servidor.settimeout(1.0)
    print(f"[*] Servidor autónomo escuchando en {host}:{puerto}...", flush=True)

    # 4. Ciclo de escucha infinito (Listen loop)
    try:
        while True:
            try:
                cliente_socket, direccion = servidor.accept()
            except socket.timeout:
                # No se conectó nadie en este segundo. Damos otra vuelta.
                # Esto le da la oportunidad a Windows de detectar si presionaste Ctrl+C.
                continue
            print(f"\n[*] Nueva conexión entrante desde {direccion[0]}:{direccion[1]}", flush=True)
            
            try:
                # Recibimos el payload
                bytes_recibidos = bytearray()
                
                # Como el cliente (Persona 3) no cierra la conexión después de enviar, 
                # implementamos un pequeño timeout temporal para saber cuándo dejó de enviar datos
                cliente_socket.settimeout(1.0)
                
                while True:
                    try:
                        pedazo = cliente_socket.recv(4096)
                        if not pedazo:
                            break # El cliente cerró la conexión
                        bytes_recibidos.extend(pedazo)
                    except socket.timeout:
                        break # Ya no hay más datos por recibir en este momento

                if len(bytes_recibidos) > 0:
                    print(f"[*] Recibido payload encriptado de {len(bytes_recibidos)} bytes.", flush=True)
                    
                    # 5. Invocar la función de desencriptar (Persona 2)
                    try:
                        print("[*] Desencriptando el payload...", flush=True)
                        bytes_resultantes = motor.desencriptar(bytes(bytes_recibidos))
                        
                        # 6. Enrutar de regreso por la misma conexión
                        print(f"[*] Enviando imagen desencriptada de vuelta ({len(bytes_resultantes)} bytes)...", flush=True)
                        cliente_socket.sendall(bytes_resultantes)
                        print("[*] Envío completado.", flush=True)
                    except ValueError as ve:
                        print(f"[!] Error de desencriptación (¿Llave incorrecta o datos corruptos?): {ve}", flush=True)
                    
            except Exception as e:
                print(f"[!] Error procesando la petición del cliente: {e}", flush=True)
            finally:
                # Cerramos la conexión con este cliente en particular
                cliente_socket.close()
                print(f"[*] Conexión cerrada con {direccion[0]}:{direccion[1]}", flush=True)
                
    except KeyboardInterrupt:
        print("\n[*] Apagando el servidor autónomo por orden del usuario (Ctrl+C).", flush=True)
    finally:
        servidor.close()

if __name__ == "__main__":
    # Estos valores deben ser acordados con la Persona 3 y Persona 2
    IP_ESCUCHA = '0.0.0.0' # Escucha en todas las interfaces de red
    PUERTO = 65433
    LLAVE_SIMETRICA = b'sistemas_dist_26' 
    
    iniciar_servidor(IP_ESCUCHA, PUERTO, LLAVE_SIMETRICA)
