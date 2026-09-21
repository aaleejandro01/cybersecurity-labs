import socket
import time
import secrets
import hmac

def generar_nonce():
    # Genera un nonce de 8 bytes como una cadena hexadecimal
    nonce = secrets.token_hex(8)
    return nonce

clave = "contraseña123"

def calcular_hmac(mensaje, clave):
    algoritmo='sha256'
    # Crea un objeto HMAC con la clave y el algoritmo especificados
    hmac_obj = hmac.new(clave.encode(), mensaje.encode(), algoritmo)

    hmac_hex = hmac_obj.hexdigest()
    return hmac_hex


HOST = "127.0.0.1"
PORT = 3030

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    while True:
        CuentaOrigen = input("Ingrese la cuenta origen: ")
        CuentaDestino = input("Ingrese la cuenta destino: ")
        Cantidad = input("Ingrese la cantidad: ")
        Nonce = generar_nonce()

        message = f"{CuentaOrigen},{CuentaDestino},{Cantidad},{Nonce}"
        concat = message+";"+calcular_hmac(message, clave)
        s.sendall(concat.encode("utf-8"))

        if message.lower() == 'exit':
            break

        data = s.recv(1024)

        # Add a delay if needed
        time.sleep(1)  # Adjust the delay time as per your requirements
