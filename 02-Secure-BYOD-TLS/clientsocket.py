import json
import socket
import ssl

HOST = "192.168.1.147"
PORT = 3030

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile="CPAI2.pem")
context.check_hostname=False
context.verify_mode=ssl.CERT_REQUIRED
context.minimum_version= ssl.TLSVersion.TLSv1_3

with socket.create_connection((HOST,PORT)) as sock:
    print("TLS version: ", ssl.OPENSSL_VERSION)

    with context.wrap_socket(sock,server_hostname=HOST) as ssock:
        while True:
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            message = json.dumps({"username":username,"password":password})

            ssock.sendall(message.encode())
            data = ssock.recv(1024)
            print(f"Received from server: {data.decode()}")