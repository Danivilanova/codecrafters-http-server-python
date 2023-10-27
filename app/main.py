import socket
import threading
import argparse
import os
from typing import Optional

# HTTP response codes
HTTP_OK = "HTTP/1.1 200 OK\r\n"
HTTP_CREATED = "HTTP/1.1 201 OK\r\n"
HTTP_NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"
HTTP_INTERNAL_ERROR = "HTTP/1.1 500 Internal Server Error\r\n"

def send_response(conn, http: str, headers: Optional[dict] = {}, body: Optional[str] = ''):
    """
    Send an HTTP response.
    
    Parameters:
    - conn: socket connection
    - http: HTTP status code string
    - headers: dict of HTTP headers
    - body: content to send as the body
    """
    response = http
    if headers:
        for key, value in headers.items():
            response += f"{key}: {value}\r\n"
    response += "\r\n" + body
    conn.send(response.encode())

def read_file(file_path: str) -> Optional[str]:
    """
    Read a file and return its content.
    
    Parameters:
    - file_path: path to the file
    
    Returns:
    - content of the file or None if file not found
    """
    try:
        with open(file_path, "rb") as f:
            return f.read().decode()
    except FileNotFoundError:
        return None

def write_file(file_path: str, content: str):
    """
    Write content to a file.
    
    Parameters:
    - file_path: path to the file
    - content: content to write
    """
    with open(file_path, "wb") as f:
        f.write(content.encode())

def handle_client(conn, addr, args):
    """
    Handle individual client connections.
    
    Parameters:
    - conn: socket connection
    - addr: address of the client
    - args: command line arguments
    """
    try:
        data = conn.recv(1024).decode()
        header = data.split("\r\n")[0]
        request_type, path, protocol = header.split(" ")

        # Main route
        if path == "/":
            send_response(conn=conn, http=HTTP_OK)
        
        # Echo route
        elif path.startswith("/echo/"):
            content = path.split("/echo/")[1]
            headers = {"Content-Type": "text/plain", "Content-Length": len(content)}
            send_response(conn=conn, http=HTTP_OK, headers=headers, body=content)
        
        # User-Agent route
        elif path == "/user-agent":
            agent = data.split("User-Agent: ")[1].split("\r\n")[0]
            headers = {"Content-Type": "text/plain", "Content-Length": len(agent)}
            send_response(conn=conn, http=HTTP_OK, headers=headers, body=agent)
        
        # File route
        elif path.startswith("/files/"):
            file_name = path.split("/files/")[1]
            file_path = os.path.join(args.directory, file_name)
            if request_type == "GET":
                content = read_file(file_path)
                if content:
                    headers = {"Content-Type": "application/octet-stream", "Content-Length": len(content)}
                    send_response(conn=conn, http=HTTP_OK, headers=headers, body=content)
                else:
                    send_response(conn=conn, http=HTTP_NOT_FOUND)
            elif request_type == "POST":
                content = data.split("\r\n\r\n")[1]
                write_file(file_path, content)
                send_response(conn=conn, http=HTTP_CREATED)
        
        # Route not found
        else:
            send_response(conn=conn, http=HTTP_NOT_FOUND)
    except Exception as e:
        print(e)
        send_response(conn=conn, http=HTTP_INTERNAL_ERROR)
    finally:
        conn.close()

def main(args):
    """
    Entry point for the application.
    """
    # Create server socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        conn, addr = server_socket.accept()  # wait for client

        # Start a new thread for each client
        thread = threading.Thread(target=handle_client, args=(conn, addr, args))
        thread.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", default="")
    args = parser.parse_args()
    main(args)
