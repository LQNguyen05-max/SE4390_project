# HTTP Parsing in Client
import sys
import socket
import os

# Function to send HTTP requests
def send_request(host, port, filename, command, options=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    if command == "GET":
        req = f"GET /{filename} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        s.sendall(req.encode())
        response = s.recv(8192).decode()
        print(response)

        if "200 OK" in response:
            body = response.split("\r\n\r\n", 1)[1]
            os.makedirs("Download", exist_ok=True)
            with open(f"Download/{filename}", "w") as f:
                f.write(body)
            print("File downloaded -> Download/", filename)

    elif command == "HEAD":
        req = f"HEAD /{filename} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        s.sendall(req.encode())
        response = s.recv(2048).decode()
        headers = response.split("\r\n\r\n")[0]
        print(headers)

    elif command == "POST":
        filepath = f"Download/{filename}"
        if not os.path.exists(filepath):
            print("File not found in Download/")
            return
        with open(filepath, "rb") as f:
            data = f.read()

        req = (
            f"POST /Upload/{filename} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"Content-Length: {len(data)}\r\n\r\n"
        )
        s.sendall(req.encode() + data)
        print(s.recv(2048).decode())

    elif command == "PUT":
        filepath = f"Download/{filename}"
        if not os.path.exists(filepath):
            print("File not found for PUT update")
            return
        with open(filepath, "rb") as f:
            data = f.read()

        req = (
            f"PUT /Upload/{filename} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"Content-Length: {len(data)}\r\n\r\n"
        )
        s.sendall(req.encode() + data)
        print(s.recv(2048).decode())

    s.close()

# DOS Attack Function
def dos_attack(host, port, filename, command, count):
    for i in range(count):
        print(f"Sending request #{i+1}")
        send_request(host, port, filename, command)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: client.py <host> <port> <filename> <GET|HEAD|POST|PUT> [-d count]")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]
    command = sys.argv[4]

    dos_count = None
    if "-d" in sys.argv:
        d_index = sys.argv.index("-d")
        if d_index + 1 < len(sys.argv):
            dos_count = int(sys.argv[d_index + 1])
        
    if dos_count:
        dos_attack(host, port, filename, command, dos_count)
    else:
        send_request(host, port, filename, command)
