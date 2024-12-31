import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Conexão encerrada pelo servidor.")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))  # Conecta ao servidor
    username = input("Digite seu nome de usuário: ")
    client_socket.send(username.encode('utf-8'))

    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:

        print("Com quem dejesa falar?")
        user = input()
        client_socket.send(user.encode('utf-8'))

        while True:
            message = input()
            if message == "SAIR":
                client_socket.send(message.encode('utf-8'))
                break
            else:
                client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    main()
