import json
import socket
import ssl
from concurrent.futures import ThreadPoolExecutor

HOST = "192.168.1.147"
PORT = 3030

def client_thread(i):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="CPAI2.pem")
    context.check_hostname = False
    context.verify_mode = ssl.CERT_REQUIRED
    context.minimum_version = ssl.TLSVersion.TLSv1_3

    with socket.create_connection((HOST, PORT)) as sock:
        print("TSL version ", ssl.OPENSSL_VERSION)

        with context.wrap_socket(sock, server_hostname=HOST) as ssock:
            username = "test_user_" + str(i+1)
            password = "test_password_" + str(i+1)

            message = json.dumps({"username": username, "password": password})

            ssock.sendall(message.encode())
            data = ssock.recv(1024)
            print(f"Received from server: {data.decode()}")

# Crea un conjunto de hilos para 300 conexiones simultáneas
num_clients = 300

with ThreadPoolExecutor(max_workers=num_clients) as executor:
    futures = [executor.submit(client_thread, i) for i in range(num_clients)]

# Espera a que todas las conexiones se completen
for future in futures:
    future.result()