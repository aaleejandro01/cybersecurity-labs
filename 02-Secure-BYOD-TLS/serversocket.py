import json
import socket
import ssl

PORT = 3030

def handle_client(conn,addr):
    print(f"Connected by {addr}")
    with conn:
        while True:
            data= conn.recv(1024)
            if not data:
                break
            message = json.loads(data.decode())
            username = message.get("username")
            password = message.get("password")

            print(f"Received from {addr}: Username: {username}, Password: {password}")

            response = "Credentials received"
            conn.sendall(response.encode())
    print(f"Connection with {addr} closed")

def main():
    HOST = "192.168.1.147"
    PORT = 3030

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='CPAI2.pem',keyfile='key.pem')
    context.minimum_version = ssl.TLSVersion.TLSv1_3

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) as sock:
        sock.bind((HOST,PORT))
        sock.listen()
        with context.wrap_socket(sock,server_side=True) as ssock:
            print(f"Listening on {HOST}:{PORT}")
            print("TLS version: ", ssl.OPENSSL_VERSION)

            while True:
                conn,addr = ssock.accept()
                handle_client(conn,addr)

if __name__ == "__main__":
    main()
