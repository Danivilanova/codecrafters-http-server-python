# Uncomment this to pass the first stage
import socket
import threading

def handle_client(conn, addr):
    # get data
    data = conn.recv(1024).decode()

    path = data.split(" ")[1]

    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith("/echo/"):
        content = path.split("/echo/")[1]
        content_length = len(content)
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {content_length}\r\n"
            "\r\n"
            f"{content}"
        )
    elif path == "/user-agent":
        agent = data.split("User-Agent: ")[1].split("\r\n")[0]
        agent_length = len(agent)
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {agent_length}\r\n"
            "\r\n"
            f"{agent}"
        )
    elif path.startswith("/files/"):
        file_name = path.split("/files/")[1]
        try:
            with open(f"files/{file_name}", "rb") as f:
                content = f.read()
                content_length = len(content)
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {content_length}\r\n"
                    "\r\n"
                    f"{content}"
                )
        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    conn.send(response.encode())
    conn.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        conn, addr = server_socket.accept() # wait for client

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

    


if __name__ == "__main__":
    main()
