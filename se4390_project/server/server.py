import socket
import threading
import os
import json
import sys
import yfinance as yf
import time

# HOST AND PORT
HOST = "127.0.0.1"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

WEBROOT = "../dist"     


# Visitor Tracking and Cookies
Visitor_DB = "visitors.json"
visitors = {}
visitor_lock = threading.Lock()

# Request DoS Attack Protection
DOS_protection_limit = 100
ban_ip = set()
request_time = {}

# Load existing visitor data if available
if os.path.exists(Visitor_DB):
    with open(Visitor_DB, "r") as f:
        visitors = json.load(f)

# Update visitor info
def update_visitor(ip, ticker=None):
    now = time.time()
    with visitor_lock:
        if ip not in visitors:
            visitors[ip] = {
                "last_visit": now,
                "tickers": {}
            }
        visitors[ip]["last_visit"] = now
        if ticker:
            visitors[ip]["tickers"][ticker] = visitors[ip]["tickers"].get(ticker, 0) + 1
        
# Save visitor data to file
def save_visitors():
    with visitor_lock:
        with open(Visitor_DB, "w") as f:
            json.dump(visitors, f)

# Send JSON Response
def send_json(conn, data):
    body = json.dumps(data).encode()
    header = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "\r\n"
    )
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
    if path.startswith("/api/search"):
        query = get_query_param(path, "query") or ""
        try:
            print("Query received:", query)
            ticker = yf.Ticker(query)
            info = ticker.info
            print("Ticker info:", info)
            data = {
                "query": query,
                "shortName": info.get("shortName", "N/A"),
                "currentPrice": info.get("currentPrice", "N/A"),
                "marketCap": info.get("marketCap", "N/A"),
                "currency": info.get("currency", "N/A"),
                "exchange": info.get("exchange", "N/A"),
            }
        except Exception as e:
            data = {
                "query": query,
                "error": str(e)
            }
        send_json(conn, data)
        return

    if path.startswith("/api/stats"):
        ticker = path.split("/")[-1]
        try:
            stats_ticker = yf.Ticker(ticker)
            print("Fetching stats for:", ticker)
            stats_info = stats_ticker.info
            data = {
                "ticker": ticker,
                "shortName": stats_info.get("shortName", "N/A"),
                "currentPrice": stats_info.get("currentPrice", "N/A"),
                "marketCap": stats_info.get("marketCap", "N/A"),
                "peRatio": stats_info.get("trailingPE", "N/A"),
                "52WeekHigh": stats_info.get("fiftyTwoWeekHigh", "N/A"),
                "52WeekLow": stats_info.get("fiftyTwoWeekLow", "N/A"),
                "dividendYield": stats_info.get("dividendYield", "N/A"),
                "industry": stats_info.get("industry", "N/A"),
                "sector": stats_info.get("sector", "N/A"),
                "website": stats_info.get("website", "N/A"),
            }
        except Exception as e:
            data = {
                "ticker": ticker,
                "error": str(e)
            }
        send_json(conn, data)
        return

    if path.startswith("/api/news"):
        ticker = path.split("/")[-1]
        try:
            news_ticker = yf.Ticker(ticker)
            news_items = news_ticker.news or []
            if news_items:
                print("First news item keys:", list(news_items[0].keys()))
                print("First news item:", news_items[0])
            filtered_news = []
            for item in news_items:
                if isinstance(item, dict) and "content" in item:
                    content = item["content"]
                    title = content.get("title") or content.get("headline")
                    link = None
                    ctu = content.get("clickThroughUrl")
                    canUrl = content.get("canonicalUrl")
                    if ctu and isinstance(ctu, dict) and "url" in ctu:
                        link = ctu["url"]
                    elif canUrl and isinstance(canUrl, dict) and "url" in canUrl:
                        link = canUrl["url"]
                    elif "url" in content:
                        link = content["url"]
                    if title and link:
                        filtered_news.append({
                            "title": title,
                            "link": link
                        })
            data = {
                "ticker": ticker,
                "news": filtered_news
            }
        except Exception as e:
            data = {
                "ticker": ticker,
                "error": str(e)
            }
        send_json(conn, data)
        return


# ------------------------------
# Serve GET requests for static files
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

# ------------------------------
# Serve HEAD requests for static files
# ------------------------------
def send_head(conn, file_path):
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
    if not os.path.exists(file_path):
        send_404(conn)
        return
    size = os.path.getsize(file_path)
    header = f"HTTP/1.1 200 OK\r\nContent-Type: {mime}\r\nContent-Length: {size}\r\n\r\n"
    conn.sendall(header.encode())

def send_404(conn):
    body = b"<h1>404 Not Found</h1>"
    header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
    conn.sendall(header.encode() + body)

def send_429(conn):
    body = b"<h1>429 Too Many Requests</h1>"
    header = "HTTP/1.1 429 Too Many Requests\r\nContent-Type: text/html\r\n\r\n"
    conn.sendall(header.encode() + body)

# ------------------------------
# Main Client Handler
# ------------------------------
def handle_client(conn, addr):
    request = conn.recv(4096).decode(errors="ignore")

    ip = addr[0]
    now = time.time()

    with visitor_lock:
        if ip in ban_ip:
            send_429(conn)
            conn.close()
            return
        
        # track request times for DoS protection
        times = request_time.get(ip, [])
        times = [t for t in times if now - t < 60]
        times.append(now)
        request_time[ip] = times
        
        if len(times) >= DOS_protection_limit:
            ban_ip.add(ip)
            print(f"Banning IP {ip} for excessive requests")
            send_429(conn)
            conn.close()
            return
        
    print("Connection from", addr)


    try:
        request_line, rest = request.split("\r\n", 1)
        method, path, version = request_line.split(" ", 2)
    except Exception:
        conn.close()
        return
    
    # Default to index.html
    if path == "/":
        path = "/index.html"

    # update visitor info only for /api/news
    if path.startswith("/api/news"): 
        ticker = path.split("/")[-1]
        update_visitor(ip, ticker)
        save_visitors()

    file_path = os.path.join(WEBROOT, path.lstrip("/"))

    headers = {}
    lines = rest.split("\r\n")
    i=0
    while i < len(lines):
        line = lines[i]
        if line == "":
            i += 1
            break
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()
        i += 1
    body = b""
    if method in ("POST", "PUT"):
        content_length = int(headers.get("content-length", 0))
        body = b"\r\n".join(line.encode() for line in lines[i:])
        while len(body) < content_length:
            body += conn.recv(4096)
    
    if method == "HEAD":
        if os.path.exists(file_path):
            send_head(conn,file_path)
        else:
            send_404(conn)
        conn.close()
        return
    
    if method == "POST" and path.startswith("/Upload"):
        filename = path.split("/")[-1]
        upload_dir = os.path.join(WEBROOT, "Upload")
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)

        with open(file_path, "wb") as f:
            f.write(body.encode() if isinstance(body, str) else body)

            header = "HTTP/1.1 201 Created\r\n\r\n"
            conn.sendall(header.encode())
            conn.close()
            return
    
    if method == "PUT" and path.startswith("/Upload"):
        filename = path.split("/")[-1]
        upload_dir = os.path.join(WEBROOT, "Upload")
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(body)
        header = "HTTP/1.1 200 OK\r\n\r\n"
        conn.sendall(header.encode())
        conn.close()
        return

    if path.startswith("/api/"):
        handle_api(conn, path)
        conn.close()
        return

    if not os.path.exists(file_path):
    # Serve index.html for client-side routes (SPA fallback)
        index_path = os.path.join(WEBROOT, "index.html")
        if os.path.exists(index_path):
            send_file(conn, index_path)
        else:
            send_404(conn)
            conn.close()
        conn.close()
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
    try:
        conn, addr = server.accept()
        # print("Connection from", addr)
        # Multithreading to handle multiple clients
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Shutting down server...")
        # Save visitor data periodically
        save_visitors()
        server.close()

