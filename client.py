import socket
import threading

# Настройки клиента
HOST = '127.0.0.1'  # Адрес сервера
PORT = 12345        # Порт сервера

# Функция для получения сообщений
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()  # Получаем сообщение
            if message:
                print(message)  # Печатаем сообщение
        except:
            print("Connection closed.")
            break

# Функция для отправки сообщений
def send_messages(sock):
    while True:
        message = input()  # Получаем ввод от пользователя
        sock.sendall(message.encode())  # Отправляем сообщение

        if message == "/exit":  # Если пользователь хочет выйти
            break

if __name__ == "__main__":
    name = input("Enter your name: ")  # Запрашиваем имя у пользователя
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))  # Подключаемся к серверу

    client_socket.sendall(name.encode())  # Отправляем имя на сервер
    print("Connected to the server.")

    # Создаем поток для получения сообщений
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    send_messages(client_socket)  # Отправляем сообщения

    client_socket.close()  # Закрываем соединение