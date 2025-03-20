import socket
import threading
import json
import time

class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}  # {client_socket: username}
        self.lock = threading.Lock()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"Client connected from {address}")
                
                # Tạo thread mới để xử lý client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket, address):
        username = None
        
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                
                try:
                    json_data = json.loads(data)
                    msg_type = json_data.get("type", "")
                    
                    if msg_type == "login":
                        username = json_data.get("username", f"User_{address[1]}")
                        self.add_client(client_socket, username)
                        
                    elif msg_type == "message":
                        if username:
                            content = json_data.get("content", "")
                            self.broadcast_message(json_data, client_socket)
                            print(f"{username}: {content}")
                            
                    elif msg_type == "logout":
                        break
                        
                except json.JSONDecodeError:
                    # Xử lý dữ liệu không phải JSON
                    print(f"Không phải JSON: {data}")
                    
        except Exception as e:
            print(f"Lỗi: {e}")
        finally:
            self.remove_client(client_socket, username)
            client_socket.close()
            print(f"Client {username} từ {address} đã ngắt kết nối")

    def add_client(self, client_socket, username):
        with self.lock:
            # Kiểm tra nếu tên đã tồn tại, thêm số ngẫu nhiên
            base_username = username
            i = 1
            while username in self.clients.values():
                username = f"{base_username}_{i}"
                i += 1
                
            self.clients[client_socket] = username
            
            # Gửi thông báo chào mừng cho client mới
            welcome_msg = {
                "type": "system",
                "content": f"Chào mừng đến với phòng chat, {username}! Hiện có {len(self.clients)} người đang online."
            }
            client_socket.send(json.dumps(welcome_msg)).encode()
            
            # Gửi danh sách người dùng hiện tại
            user_list = {
                "type": "user_list",
                "users": list(self.clients.values())
            }
            client_socket.send(json.dumps(user_list).encode())
            
            # Thông báo cho tất cả client khác
            join_notification = {
                "type": "user_joined",
                "username": username
            }
            self.broadcast_message(join_notification, exclude=client_socket)
            
            # Cập nhật danh sách người dùng cho tất cả
            self.broadcast_user_list()
            
            print(f"Client {username} đã tham gia. Tổng số: {len(self.clients)}")

    def remove_client(self, client_socket, username):
        with self.lock:
            if client_socket in self.clients:
                username = self.clients.pop(client_socket)
                
                # Thông báo đến các client khác
                leave_notification = {
                    "type": "user_left",
                    "username": username
                }
                self.broadcast_message(leave_notification)
                
                # Cập nhật danh sách người dùng
                self.broadcast_user_list()
                
                print(f"Client {username} đã rời đi. Còn lại: {len(self.clients)}")

    def broadcast_message(self, message, exclude=None):
        with self.lock:
            for client in list(self.clients.keys()):
                if client != exclude:
                    try:
                        client.send(json.dumps(message).encode())
                    except:
                        # Nếu gửi lỗi, xóa client
                        self.remove_client(client, self.clients.get(client))

    def broadcast_user_list(self):
        user_list = {
            "type": "user_list",
            "users": list(self.clients.values())
        }
        self.broadcast_message(user_list)

if __name__ == "__main__":
    server = ChatServer()
    server.start()