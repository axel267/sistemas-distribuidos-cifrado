import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class MotorCriptografico:
    def __init__(self, clave_secreta: bytes):
        """
        Inicializa el motor con una llave simétrica.
        La llave DEBE ser de 16, 24 o 32 bytes.
        """
        self.key = clave_secreta
        self.block_size = AES.block_size # AES (bloques fijos de 16 bytes)

    def encriptar(self, datos_originales: bytes) -> bytes:
        """
        Toma los bytes de la imagen y devuelve un payload cifrado con su IV.
        """
        # 1. Generar un Vector de Inicialización (IV) único por transmisión
        iv = os.urandom(self.block_size)
        # 2. Iniciar el cifrador en modo CBC
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # 3. Aplicar padding para que los bytes sean múltiplos exactos de 16
        padded_data = pad(datos_originales, self.block_size)
        # 4. Cifrar la información
        ciphertext = cipher.encrypt(padded_data)
        # 5. Retornar el IV concatenado con la imagen cifrada
        return iv + ciphertext

    def desencriptar(self, payload_recibido: bytes) -> bytes:
        """
        Toma el payload cifrado, extrae el IV y recupera los bytes de la imagen.
        """
        # 1. Extraer el IV (los primeros 16 bytes)
        iv = payload_recibido[:self.block_size]
        # 2. Separar los datos encriptados
        ciphertext = payload_recibido[self.block_size:]
        # 3. Iniciar el descifrador
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # 4. Descifrar los datos
        padded_data = cipher.decrypt(ciphertext)
        # 5. Remover el padding para obtener los bytes originales exactos
        datos_originales = unpad(padded_data, self.block_size)
        
        return datos_originales