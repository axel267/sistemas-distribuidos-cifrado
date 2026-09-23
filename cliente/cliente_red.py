import socket

def enviar_y_recibir_payload(ip_servidor, puerto, bytes_encriptados):
    # 1. Creación del Socket
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Configuración de seguridad (Timeout)
    cliente.settimeout(15.0)
    
    try:
        # 3. Establecer la conexión
        print(f"[*] Conectando a {ip_servidor}:{puerto}...")
        cliente.connect((ip_servidor, puerto))
        
        # 4. Enviar los datos
        print(f"[*] Enviando paquete de {len(bytes_encriptados)} bytes...")
        cliente.sendall(bytes_encriptados)
        
        # 5. Preparar la recepción de la respuesta
        print("[*] Esperando la imagen de respuesta del servidor...")
        bytes_recibidos = bytearray()
        
        # 6. Recibir en fragmentos (Chunks)
        while True:
            pedazo = cliente.recv(4096)
            if not pedazo:
                break
            bytes_recibidos.extend(pedazo)
            
        print(f"[*] Recepción exitosa: {len(bytes_recibidos)} bytes.")
        return bytes(bytes_recibidos)
        
    except socket.timeout:
        print("[!] Error: El servidor se tardó demasiado (Timeout).")
        return None
    except Exception as e:
        print(f"[!] Error de conexión: {e}")
        return None
    finally:
        # 7. Cerrar la conexión
        cliente.close()