import socket
import threading
import os

HOST = "127.0.0.1"
PORT = 8080

WEBROOT = "../dist"     

def handle_client(conn, addr):
    request = conn.recv(4096).decode(errors="ignore")
    print(f"\n--- Incoming Request from {addr} ---")
    print(request)

    try:
        path = request.split(" ")[1]
    except:
        conn.close()
        return

    # Default to index.html
    if path == "/":
        path = "/index.html"

    file_path = os.path.join(WEBROOT, path.lstrip("/"))

    if not os.path.exists(file_path):
        send_404(conn)
        return

    send_file(conn, file_path)
    conn.close()


def send_file(conn, file_path):
    ext = file_path.split(".")[-1]

    mime = {
        "html": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "jsx": "application/javascript",
        "png": "image/png",
        "jpg": "image/jpg",
        "jpeg": "image/jpeg"
    }.get(ext, "text/plain")

    with open(file_path, "rb") as f:
        body = f.read()

    header = f"HTTP/1.1 200 OK\r\nContent-Type: {mime}\r\n\r\n"
    conn.sendall(header.encode() + body)


def send_404(conn):
    body = b"<h1>404 Not Found</h1>"
    header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
    conn.sendall(header.encode() + body)


# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(8)

print(f"Serving http://{HOST}:{PORT}")
while True:
    conn, addr = server.accept()
    print("Waiting on connection...")
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
