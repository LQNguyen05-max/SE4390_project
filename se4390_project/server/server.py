import socket
import threading
import os
import json
import sys

# HOST AND PORT
HOST = "127.0.0.1"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

WEBROOT = "../dist"     

# Send JSON Response
def send_json(conn, data):
    body = json.dumps(data).encode()
    header = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
    conn.sendall(header.encode() + body)

# Query Parameter Parser
def get_query_param(path, key):
    if "?" not in path:
        return None
    query = path.split("?", 1)[1]
    params = query.split("&")
    for p in params:
        k, _, v = p.partition("=")
        if k == key:
            return v
    return None

# API Endpoint Handler
def handle_api(conn, path):

    # /api/search?query=AAPL
    if path.startswith("/api/search"):
        query = get_query_param(path, "query") or ""
        data = {
            "query": query,
            "results": [f"Sample news for {query}", "More sample news"]
        }
        send_json(conn, data)
        return

    # /api/stats/AAPL
    if path.startswith("/api/stats"):
        ticker = path.split("/")[-1]
        data = {
            "ticker": ticker,
            "visits": 12,
            "popularity_rank": 3
        }
        send_json(conn, data)
        return

    # /api/news/AAPL
    if path.startswith("/api/news"):
        ticker = path.split("/")[-1]
        data = {
            "ticker": ticker,
            "news": [
                f"{ticker} hits new high",
                f"{ticker} analysts raise forecast"
            ]
        }
        send_json(conn, data)
        return

    send_404(conn)



# ------------------------------
# Serve static files
# ------------------------------
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


# ------------------------------
# Main Client Handler
# ------------------------------
def handle_client(conn, addr):
    request = conn.recv(4096).decode(errors="ignore")
    # print(f"\n--- Incoming Request from {addr} ---")
    # print(request)

    try:
        path = request.split(" ")[1]
    except:
        conn.close()
        return

    # --------------------------
    # Check API BEFORE files
    # --------------------------
    if path.startswith("/api/"):
        handle_api(conn, path)
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


# ------------------------------
# Start server
# ------------------------------
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(8)

print(f"Serving http://{HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print("Waiting on connection...")
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
