import socket
import pickle


def start_server():
    HOST = ' 192.168.0.120'  # Listen on all available interfaces
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()

            print(f"Connected by {addr}")

            # Once authenticated, receive data from the client
            data = conn.recv(4096)
            if data:
                result = pickle.loads(data)
                print("Received Result:")
                print(result)


if __name__ == "__main__":
    start_server()
