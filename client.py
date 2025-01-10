import socket
import threading
from crypto import encrypt_message, decrypt_message

def receive_messages(sock, key):
    while True:
        try:
            encrypted_message = sock.recv(1024).decode('utf-8')
            message = decrypt_message(key, encrypted_message)
            print(message)
        except:
            print("Conexão encerrada pelo servidor.")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    action = input("Digite 'LOGIN' para entrar ou 'CADASTRAR' para criar um novo usuário: ").strip().upper()
    client_socket.send(action.encode('utf-8'))

    if action == "CADASTRAR":
        username = input("Escolha um nome de usuário: ")
        password = input("Escolha uma senha: ")
        # Envia o nome de usuário
        client_socket.send(username.encode('utf-8'))  
        response = client_socket.recv(1024).decode('utf-8')  # Espera confirmação ou solicitação para senha

        # Envia a senha
        client_socket.send(password.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        if response == "USUÁRIO CRIADO":
            print("Usuário cadastrado com sucesso! Reinicie o cliente para fazer login.")
        elif response == "USUÁRIO EXISTE":
            print("Usuário já existe. Tente novamente.")
        client_socket.close()
        return


    elif action == "LOGIN":
        username = input("Digite seu nome de usuário: ")
        password = input("Digite sua senha: ")
        client_socket.send(f"{username}:{password}".encode('utf-8'))

        auth_response = client_socket.recv(1024)
        if auth_response == b"FALHA":
            print("Autenticação falhou. Encerrando a conexão.")
            client_socket.close()
            return

        key = auth_response
        print("Autenticação bem-sucedida!")

        threading.Thread(target=receive_messages, args=(client_socket, key)).start()

        current_recipient = None
        while True:
            if not current_recipient:
                current_recipient = input("Com quem deseja falar? ")

            message = input(f"Para {current_recipient} (digite 'MUDAR' para trocar ou 'SAIR' para sair): ")
            if message == "SAIR":
                client_socket.send(encrypt_message(key, message).encode('utf-8'))
                break
            elif message == "MUDAR":
                current_recipient = None
            else:
                data = f"{current_recipient}:{message}"
                client_socket.send(encrypt_message(key, data).encode('utf-8'))


if __name__ == "__main__":
    main()
