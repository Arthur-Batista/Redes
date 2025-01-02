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

    # Etapa de autenticação
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")
    client_socket.send(f"{username}:{password}".encode('utf-8'))

    # Verificar se a autenticação foi bem-sucedida
    auth_response = client_socket.recv(1024).decode('utf-8')
    if auth_response != "SUCESSO":
        print("Autenticação falhou. Encerrando a conexão.")
        client_socket.close()
        return

    print("Autenticação bem-sucedida!")

    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        print("Com quem deseja falar?")
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
