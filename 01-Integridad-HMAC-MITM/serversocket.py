import socket
import hmac
import os
clave = "contraseña123"

def calcular_hmac(mensaje, clave):
    algoritmo='sha256'
    # Crea un objeto HMAC con la clave y el algoritmo especificados
    hmac_obj = hmac.new(clave.encode(), mensaje.encode(), algoritmo)

    hmac_hex = hmac_obj.hexdigest()
    return hmac_hex

def guardar_nonce_en_archivo(archivo, nonce):
        with open(archivo, 'a') as file:
            file.write(f"{nonce}\n")


HOST = "127.0.0.1"
PORT = 3030
Listarecibos = []
archivo_nonce = "nonces.txt"
nonce = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        print(f"Connected by {addr}")

        with conn:
            while True:
                data = conn.recv(1024)
                s = data.decode("utf-8").split(";")
                m = s[0]
                c = s[1]
                l= m.split(",")[3]
                hashData = calcular_hmac(m, clave)
                if not data:
                    break
                if not os.path.exists(archivo_nonce):
                    with open(archivo_nonce, 'w') as file:
                        file.write("NONCES REGISTRADOS\n")
                with open(archivo_nonce, 'r') as file:
                    nonces_registrados = file.read().splitlines()
                    for n in nonces_registrados:
                        if (l == n):
                            nonce =+1
                            break
                    if(nonce == 0):
                        guardar_nonce_en_archivo(archivo_nonce, l)

                print(f"Received from client: {data.decode('utf-8')}")
                if (hashData == c and nonce == 0):
                    print("Se ha conservado la integridad")

                elif (hashData == c and nonce != 0):
                    print("Fallo de integridad por Replay Attack")
                else:
                    print("Fallo de Integridad")
                # Here you can process the received data and prepare a response if needed
                response = "Todo recibido"
                # conn.sendall(response.encode('utf-8'))
                conn.sendall(response.encode('utf-8'))
