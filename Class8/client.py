
import socket
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from threading import Thread
from tkinter import ttk
import time
import json
import random

# Tạo danh sách màu cho các người dùng khác nhau
USER_COLORS = [
    "#E91E63", "#9C27B0", "#673AB7", "#3F51B5", "#2196F3", 
    "#009688", "#4CAF50", "#8BC34A", "#CDDC39", "#FFC107", 
    "#FF9800", "#FF5722", "#795548", "#607D8B"
]

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-User Chat Client")
        self.root.geometry("700x550")
        self.root.configure(bg="#f0f0f0")
        
        # Thiết lập thông tin kết nối
        self.host = '127.0.0.1'
        self.port = 12345
        self.client_socket = None
        self.username = None
        self.users_colors = {}  # Lưu trữ màu cho mỗi người dùng
        
        # Tạo style cho các widget
        self.create_styles()
        
        # Tạo giao diện
        self.create_widgets()
        
        # Kết nối và đăng nhập
        self.connect_to_server()

    def create_styles(self):
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", 
                        background="#4CAF50", 
                        foreground="black", 
                        font=("Arial", 10, "bold"),
                        padding=10)
        self.style.map("TButton",
                  background=[("active", "#45a049")])
        
    def create_widgets(self):
        # Tạo frame chính
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tạo header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.header_label = tk.Label(self.header_frame, text="Multi-User Chat", font=("Arial", 16, "bold"), 
                              bg="#2196F3", fg="white", padx=10, pady=10)
        self.header_label.pack(fill=tk.X)
        
        # Frame chính chứa khung chat và danh sách người dùng
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame cho khung chat
        self.chat_frame = ttk.Frame(self.content_frame)
        self.chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame cho danh sách người dùng
        self.users_frame = ttk.Frame(self.content_frame, width=150)
        self.users_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        self.users_frame.pack_propagate(False)  # Giữ kích thước cố định
        
        # Tiêu đề danh sách người dùng
        self.users_label = tk.Label(self.users_frame, text="Người dùng online", 
                            font=("Arial", 12, "bold"), bg="#E0E0E0", 
                            fg="#333333", padx=5, pady=5)
        self.users_label.pack(fill=tk.X)
        
        # Danh sách người dùng
        self.users_listbox = tk.Listbox(self.users_frame, font=("Arial", 10), 
                                bg="white", fg="#333333", height=15)
        self.users_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Khu vực hiển thị tin nhắn
        self.text_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, 
                                          height=20, bg="white", font=("Arial", 10))
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=10)
        self.text_area.config(state=tk.DISABLED)
        
        # Frame cho phần nhập tin nhắn
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=10)
        
        # Entry để nhập tin nhắn
        self.entry = tk.Entry(self.input_frame, font=("Arial", 10), bd=2, relief=tk.GROOVE)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.handle_enter)
        
        # Nút gửi
        self.send_button = ttk.Button(self.input_frame, text="Gửi", command=self.send_message, style="TButton")
        self.send_button.pack(side=tk.RIGHT)
        
        # Thanh trạng thái
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(self.status_frame, text="Đang kết nối...", 
                              font=("Arial", 9), fg="#FFA000", bg="#f0f0f0", anchor="w")
        self.status_label.pack(fill=tk.X)
        
    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            
            # Cập nhật trạng thái
            self.status_label.config(text="Đã kết nối đến server", fg="#4CAF50")
            
            # Yêu cầu người dùng nhập tên
            self.get_username()
            
            # Bật khu vực tin nhắn để thêm thông báo chào mừng
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, f"Chào mừng đến với phòng chat, {self.username}!\n", "system")
            self.text_area.tag_configure("system", foreground="#9E9E9E", font=("Arial", 10, "italic"))
            self.text_area.config(state=tk.DISABLED)
            
            # Khởi động luồng nhận tin nhắn
            self.receive_thread = Thread(target=self.receive_message)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến server: {e}")
            self.root.destroy()
    
    def get_username(self):
        # Hỏi người dùng tên đăng nhập
        self.username = simpledialog.askstring("Đăng nhập", "Nhập tên của bạn:", parent=self.root)
        
        if not self.username:
            self.username = f"User_{random.randint(1000, 9999)}"
            
        # Gửi thông tin đăng nhập đến server
        login_data = {
            "type": "login",
            "username": self.username
        }
        self.client_socket.send(json.dumps(login_data).encode())
        
        # Cập nhật tiêu đề cửa sổ
        self.root.title(f"Chat Client - {self.username}")
        
        # Thêm màu cho người dùng hiện tại
        self.users_colors[self.username] = USER_COLORS[0]  # Người dùng hiện tại luôn có màu đầu tiên
        
        # Cấu hình tag cho tin nhắn
        self.text_area.config(state=tk.NORMAL)
        self.text_area.tag_configure("you_tag", foreground=self.users_colors[self.username], font=("Arial", 10, "bold"))
        self.text_area.tag_configure("you_message", foreground=self.users_colors[self.username], font=("Arial", 10))
        self.text_area.config(state=tk.DISABLED)
    
    def send_message(self):
        message = self.entry.get()
        if message:
            # Tạo gói tin JSON
            message_data = {
                "type": "message",
                "username": self.username,
                "content": message
            }
            
            try:
                # Gửi tin nhắn đến server
                self.client_socket.send(json.dumps(message_data).encode())
                
                # Hiển thị tin nhắn của chính mình
                current_time = time.strftime("%H:%M:%S")
                
                self.text_area.config(state=tk.NORMAL)
                self.text_area.insert(tk.END, f"[{current_time}] ", "time_tag")
                self.text_area.insert(tk.END, f"{self.username}: ", "you_tag")
                self.text_area.insert(tk.END, f"{message}\n", "you_message")
                self.text_area.tag_configure("time_tag", foreground="#9E9E9E", font=("Arial", 9))
                self.text_area.see(tk.END)
                self.text_area.config(state=tk.DISABLED)
                
                # Xóa nội dung đã nhập
                self.entry.delete(0, tk.END)
                
            except Exception as e:
                self.show_error(f"Lỗi khi gửi tin nhắn: {e}")
    
    def receive_message(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                    
                # Phân tích dữ liệu JSON
                try:
                    json_data = json.loads(data)
                    self.process_message(json_data)
                except json.JSONDecodeError:
                    # Nếu không phải JSON, hiển thị như tin nhắn thông thường
                    current_time = time.strftime("%H:%M:%S")
                    
                    self.text_area.config(state=tk.NORMAL)
                    self.text_area.insert(tk.END, f"[{current_time}] Server: {data}\n", "server_message")
                    self.text_area.tag_configure("server_message", foreground="#E53935", font=("Arial", 10))
                    self.text_area.see(tk.END)
                    self.text_area.config(state=tk.DISABLED)
                    
            except Exception as e:
                self.show_error(f"Mất kết nối đến server: {e}")
                break
                
        # Khi vòng lặp kết thúc, đóng kết nối
        self.close_connection("Mất kết nối đến server")
    
    def process_message(self, data):
        msg_type = data.get("type", "")
        
        if msg_type == "message":
            # Xử lý tin nhắn từ người dùng khác
            username = data.get("username", "Unknown")
            content = data.get("content", "")
            current_time = time.strftime("%H:%M:%S")
            
            # Nếu người dùng chưa có màu, gán một màu mới
            if username not in self.users_colors and username != self.username:
                color_index = len(self.users_colors) % len(USER_COLORS)
                self.users_colors[username] = USER_COLORS[color_index]
                
                # Tạo tag cho người dùng này
                self.text_area.config(state=tk.NORMAL)
                self.text_area.tag_configure(f"user_{username}_tag", 
                                    foreground=self.users_colors[username], 
                                    font=("Arial", 10, "bold"))
                self.text_area.tag_configure(f"user_{username}_message", 
                                    foreground=self.users_colors[username], 
                                    font=("Arial", 10))
                self.text_area.config(state=tk.DISABLED)
            
            # Hiển thị tin nhắn nếu không phải từ chính mình
            if username != self.username:
                self.text_area.config(state=tk.NORMAL)
                self.text_area.insert(tk.END, f"[{current_time}] ", "time_tag")
                self.text_area.insert(tk.END, f"{username}: ", f"user_{username}_tag")
                self.text_area.insert(tk.END, f"{content}\n", f"user_{username}_message")
                self.text_area.see(tk.END)
                self.text_area.config(state=tk.DISABLED)
                
        elif msg_type == "system":
            # Xử lý thông báo hệ thống
            content = data.get("content", "")
            
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, f"{content}\n", "system")
            self.text_area.see(tk.END)
            self.text_area.config(state=tk.DISABLED)
            
        elif msg_type == "user_list":
            # Cập nhật danh sách người dùng
            users = data.get("users", [])
            self.update_user_list(users)
            
        elif msg_type == "user_joined":
            # Thông báo người dùng mới tham gia
            username = data.get("username", "")
            
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, f"{username} đã tham gia phòng chat\n", "system")
            self.text_area.see(tk.END)
            self.text_area.config(state=tk.DISABLED)
            
        elif msg_type == "user_left":
            # Thông báo người dùng rời phòng
            username = data.get("username", "")
            
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, f"{username} đã rời phòng chat\n", "system")
            self.text_area.see(tk.END)
            self.text_area.config(state=tk.DISABLED)
    
    def update_user_list(self, users):
        # Xóa danh sách hiện tại
        self.users_listbox.delete(0, tk.END)
        
        # Thêm người dùng hiện tại với dấu sao
        self.users_listbox.insert(tk.END, f"* {self.username}")
        
        # Thêm các người dùng khác
        for user in users:
            if user != self.username:
                self.users_listbox.insert(tk.END, user)
                
                # Nếu chưa có màu, gán màu mới
                if user not in self.users_colors:
                    color_index = len(self.users_colors) % len(USER_COLORS)
                    self.users_colors[user] = USER_COLORS[color_index]
    
    def handle_enter(self, event):
        self.send_message()
        return "break"  # Ngăn không cho Enter tạo dòng mới
    
    def show_error(self, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"LỖI: {message}\n", "error")
        self.text_area.tag_configure("error", foreground="red", font=("Arial", 10, "bold"))
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)
        
        # Cập nhật trạng thái
        self.status_label.config(text=f"Lỗi: {message}", fg="red")
    
    def close_connection(self, reason=None):
        if self.client_socket:
            try:
                # Gửi thông báo đăng xuất trước khi đóng
                logout_data = {
                    "type": "logout",
                    "username": self.username
                }
                self.client_socket.send(json.dumps(logout_data).encode())
                self.client_socket.close()
            except:
                pass
            
        if reason:
            self.show_error(reason)
            
        # Vô hiệu hóa các điều khiển
        self.entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)


    def show_server_code():
        server_window = tk.Toplevel(window)
        server_window.title("Server Code")
        server_window.geometry("800x600")
        
        text = scrolledtext.ScrolledText(server_window, wrap=tk.WORD, font=("Consolas", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert(tk.END, SERVER_CODE)
        text.config(state=tk.DISABLED)
        
        tk.Button(server_window, text="Đóng", 
            command=server_window.destroy, 
            bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

if __name__ == "__main__":
    window = tk.Tk()
 
    app = ChatClient(window)
    window.protocol("WM_DELETE_WINDOW", lambda: app.close_connection("Đóng ứng dụng") or window.destroy())
    window.mainloop()