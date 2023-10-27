# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client

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
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    conn.send(response.encode())


if __name__ == "__main__":
    main()
