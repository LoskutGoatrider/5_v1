import socket
import threading
import time

# Настройки сервера
HOST = '127.0.0.1'  # Локальный адрес
PORT = 12345  # Порт для сервера

clients = []  # Список активных клиентов
history = []  # История сообщений


# Функция для обработки сообщений клиентов
def handle_client(conn, addr):
    name = conn.recv(1024).decode()  # Получаем имя клиента
    print(f"Client {name} connected from {addr}")

    # Приветствуем клиента
    conn.sendall(b'Welcome to the chat!\n')

    # Отправляем историю сообщений
    for message in history:
        conn.sendall(message.encode() + b'\n')

    while True:
        try:
            message = conn.recv(1024).decode()  # Получаем сообщение
            if message == "/exit":  # Если клиент хочет выйти
                print(f"Client {name} has left the chat")
                break

            # Форматируем сообщение
            msg_time = time.strftime('%Y-%m-%d %H:%M:%S')
            full_message = f"{msg_time}: {addr[0]}: {name}: {message}"
            history.append(full_message)  # Добавляем в историю

            # Сохраняем сообщение в файл
            with open("это_история_сообщений.txt", "a") as f:
                f.write(full_message + '\n')

            # Рассылаем сообщение всем кроме отправителя
            broadcast_message(full_message, name)
        except:
            break

    conn.close()  # Закрываем соединение
    clients.remove(conn)  # Удаляем клиента из списка
    print(f"{name} has left the chat.")


# Функция для рассылки сообщений клиентам
def broadcast_message(message, sender):
    for client in clients:
        if client != sender:  # Не отправляем отправителю
            client.sendall(message.encode() + b'\n')


# Основная функция сервера
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Максимум 5 подключений
    print("Server started, waiting for clients...")

    while True:
        conn, addr = server_socket.accept()  # Принимаем новое соединение
        clients.append(conn)  # Добавляем нового клиента
        threading.Thread(target=handle_client, args=(conn, addr)).start()  # Обрабатываем клиента в отдельном потоке


if __name__ == "__main__":
    start_server()  # Запускаем сервер