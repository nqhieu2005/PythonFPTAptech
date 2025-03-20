from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import base64
import io
import sys
from datetime import datetime
import math


class MongoDB:
    def __init__(self):
        try:
            self.client = MongoClient('mongodb://localhost:27017/')
            self.db = self.client['phoneBook']
            self.collection = self.db['list']
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến MongoDB: {str(e)}")
            sys.exit(1)

        self.window = tk.Tk()
        self.window.title("Danh bạ điện thoại")
        self.window.geometry("1000x650")
        self.window.configure(bg="#f0f0f0")
        
        # Biến để lưu ID của liên hệ đang được chỉnh sửa
        self.current_id = None
        # Biến để lưu ảnh hiện tại dưới dạng base64
        self.current_image_data = None
        # Biến để theo dõi trạng thái chỉnh sửa
        self.is_editing = False

        self.current_page = 1
        self.contacts_per_page = 10
        self.total_pages = 1
        self.total_contacts = 0
        self.current_search = ""

        # Tạo frame chính
        main_frame = tk.Frame(self.window, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame cho thông tin liên hệ
        input_frame = tk.LabelFrame(main_frame, text="Thông tin liên hệ", padx=10, pady=10, bg="#f0f0f0", font=("Arial", 12, "bold"))
        input_frame.pack(padx=10, pady=10, fill='x')

        # Frame bên trái cho các trường nhập liệu
        left_frame = tk.Frame(input_frame, bg="#f0f0f0")
        left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)

        # Frame bên phải cho ảnh
        right_frame = tk.Frame(input_frame, bg="#f0f0f0")
        right_frame.pack(side=tk.RIGHT, fill="both", padx=5, pady=5)

        # Tạo và đặt các widget nhập liệu bên trái
        tk.Label(left_frame, text="Họ và tên:", bg="#f0f0f0", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.name_entry = tk.Entry(left_frame, width=30, font=("Arial", 11))
        self.name_entry.grid(row=0, column=1, padx=5, pady=10)

        tk.Label(left_frame, text="Số điện thoại:", bg="#f0f0f0", font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.phone_entry = tk.Entry(left_frame, width=30, font=("Arial", 11))
        self.phone_entry.grid(row=1, column=1, padx=5, pady=10)

        tk.Label(left_frame, text="Email:", bg="#f0f0f0", font=("Arial", 11)).grid(row=2, column=0, padx=5, pady=10, sticky="w")
        self.email_entry = tk.Entry(left_frame, width=30, font=("Arial", 11))
        self.email_entry.grid(row=2, column=1, padx=5, pady=10)

        # Ảnh đại diện bên phải
        self.image_frame = tk.Frame(right_frame, width=200, height=200, bg="white", relief="solid", borderwidth=1)
        self.image_frame.pack(padx=20, pady=10)
        self.image_frame.pack_propagate(False)  # Giữ kích thước cố định
        
        self.image_label = tk.Label(self.image_frame, text="Chưa có ảnh", bg="white")
        self.image_label.pack(fill="both", expand=True)

        # Nút chọn ảnh
        self.select_image_btn = tk.Button(right_frame, text="Chọn ảnh", command=self.select_image, 
                                       bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.select_image_btn.pack(padx=5, pady=10)

        # Frame cho các nút chức năng
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill="x", padx=10, pady=5)

        # Tạo các nút chức năng
        self.add_button = tk.Button(button_frame, text="Thêm", command=self.add_contact,
                                  bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = tk.Button(button_frame, text="Cập nhật", command=self.update_contact,
                                     bg="#FF9800", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5)
        self.update_button.pack(side=tk.LEFT, padx=5)
        self.update_button.config(state=tk.DISABLED)  # Ban đầu nút cập nhật bị vô hiệu hóa

        self.delete_button = tk.Button(button_frame, text="Xóa", command=self.delete_contact,
                                     bg="#F44336", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        self.delete_button.config(state=tk.DISABLED)  # Ban đầu nút xóa bị vô hiệu hóa

        self.clear_button = tk.Button(button_frame, text="Làm mới", command=self.clear_entries,
                                    bg="#607D8B", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.chat_button = tk.Button(button_frame, text="Chat", command=self.open_chat,
                           bg="#9C27B0", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5)
        self.chat_button.pack(side=tk.LEFT, padx=5)
        self.chat_button.config(state=tk.DISABLED) 

        # Frame tìm kiếm
        search_frame = tk.Frame(main_frame, bg="#f0f0f0")
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Tìm kiếm:", bg="#f0f0f0", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=40, font=("Arial", 11))
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.search_contacts)

        # Frame cho danh sách liên hệ
        list_frame = tk.LabelFrame(main_frame, text="Danh sách liên hệ", padx=10, pady=10, bg="#f0f0f0", font=("Arial", 12, "bold"))
        list_frame.pack(padx=10, pady=5, fill='both', expand=True)
        # Create pagination frame
        pagination_frame = tk.Frame(main_frame, bg="#f0f0f0")
        pagination_frame.pack(fill="x", padx=10, pady=5)

        # Previous page button
        self.prev_button = tk.Button(pagination_frame, text="<<", command=self.prev_page,
                                bg="#607D8B", fg="white", font=("Arial", 10, "bold"), padx=10, pady=3)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        # Page info label
        self.page_info = tk.Label(pagination_frame, text="Trang 1 / 1", bg="#f0f0f0", font=("Arial", 11))
        self.page_info.pack(side=tk.LEFT, padx=10)

        # Next page button
        self.next_button = tk.Button(pagination_frame, text=">>", command=self.next_page,
                                bg="#607D8B", fg="white", font=("Arial", 10, "bold"), padx=10, pady=3)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Items per page dropdown
        tk.Label(pagination_frame, text="Số liên hệ/trang:", bg="#f0f0f0", font=("Arial", 11)).pack(side=tk.LEFT, padx=10)
        self.page_size_var = tk.StringVar(value="10")
        page_size_options = ttk.Combobox(pagination_frame, textvariable=self.page_size_var, 
                                        values=["5", "10", "20", "50"], width=5)
        page_size_options.pack(side=tk.LEFT, padx=5)
        page_size_options.bind("<<ComboboxSelected>>", self.change_page_size)

        # Tạo thanh cuộn
        scrollbar_y = tk.Scrollbar(list_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Danh sách hiển thị
        self.tree = ttk.Treeview(list_frame, columns=("ID", "Tên", "Số điện thoại", "Email", "Ảnh"), 
                               show="headings", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Định nghĩa các cột
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Số điện thoại", text="Số điện thoại")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Ảnh", text="Ảnh")
        
        # Định nghĩa chiều rộng của các cột
        self.tree.column("ID", width=0, stretch=tk.NO)  # Ẩn cột ID
        self.tree.column("Tên", width=200)
        self.tree.column("Số điện thoại", width=150)
        self.tree.column("Email", width=250)
        self.tree.column("Ảnh", width=300)
        
        self.tree.pack(fill='both', expand=True)
        
        # Cấu hình thanh cuộn
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Sự kiện khi click vào một liên hệ
        self.tree.bind("<ButtonRelease-1>", self.select_contact)
        
        # Style cho Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        # Load danh sách liên hệ
        self.load_contacts()

    def clear_entries(self):
        """Xóa tất cả các trường nhập liệu và đặt lại trạng thái"""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.image_label.config(image=None, text="Chưa có ảnh")
        self.current_image_data = None
        self.current_id = None
        self.is_editing = False
        
        # Cập nhật trạng thái các nút
        self.add_button.config(state=tk.NORMAL)
        self.update_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.chat_button.config(state=tk.DISABLED)

    def select_image(self):
        """Chọn ảnh từ máy tính và hiển thị trên giao diện"""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            try:
                # Mở và hiển thị ảnh với kích thước phù hợp
                image = Image.open(file_path)
                image = image.resize((180, 180), Image.LANCZOS)  # Sử dụng LANCZOS để chất lượng ảnh tốt hơn
                
                # Lưu dữ liệu ảnh dưới dạng base64
                with open(file_path, "rb") as image_file:
                    self.current_image_data = base64.b64encode(image_file.read()).decode("utf-8")
                
                # Hiển thị ảnh lên giao diện
                photo_image = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo_image, text="")
                self.image_label.image = photo_image  # Giữ tham chiếu để tránh bị thu gom bởi garbage collector
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mở ảnh: {str(e)}")
                
    def add_contact(self):
        """Thêm liên hệ mới vào CSDL"""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if not name or not phone or not email:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return
            
        contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "image_data": self.current_image_data  # Lưu ảnh dưới dạng base64
        }
        
        try:
            result = self.collection.insert_one(contact)
            self.load_contacts()
            self.clear_entries()
            messagebox.showinfo("Thông báo", "Thêm liên hệ thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm liên hệ: {str(e)}")

    def update_contact(self):
        """Cập nhật thông tin liên hệ"""
        if not self.current_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn một liên hệ để cập nhật")
            return
            
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if not name or not phone or not email:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return
            
        contact = {
            "name": name,
            "phone": phone,
            "email": email,
        }
        
        # Chỉ cập nhật ảnh nếu đã chọn ảnh mới
        if self.current_image_data:
            contact["image_data"] = self.current_image_data
            
        try:
            from bson.objectid import ObjectId
            self.collection.update_one({"_id": ObjectId(self.current_id)}, {"$set": contact})
            self.load_contacts()
            self.clear_entries()
            messagebox.showinfo("Thông báo", "Cập nhật liên hệ thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật liên hệ: {str(e)}")

    def delete_contact(self):
        """Xóa liên hệ khỏi CSDL"""
        if not self.current_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn một liên hệ để xóa")
            return
            
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa liên hệ này?")
        if not confirm:
            return
            
        try:
            from bson.objectid import ObjectId
            self.collection.delete_one({"_id": ObjectId(self.current_id)})
            self.load_contacts()
            self.clear_entries()
            messagebox.showinfo("Thông báo", "Xóa liên hệ thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa liên hệ: {str(e)}")

    def select_contact(self, event):
        """Chọn một liên hệ từ danh sách để xem/chỉnh sửa"""
        selected_item = self.tree.selection()
        self.chat_button.config(state=tk.NORMAL)
        if not selected_item:
            return
            
        item = self.tree.item(selected_item[0])
        values = item["values"]
        
        # Lấy ID từ cột ẩn
        self.current_id = values[0]
        
        # Hiển thị thông tin của liên hệ đã chọn lên form
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])
        
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, values[2])
        
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[3])
        
        # Tải thông tin liên hệ từ CSDL để lấy dữ liệu ảnh
        try:
            from bson.objectid import ObjectId
            contact = self.collection.find_one({"_id": ObjectId(self.current_id)})
            if contact and "image_data" in contact and contact["image_data"]:
                self.current_image_data = contact["image_data"]
                # Chuyển đổi dữ liệu base64 thành ảnh
                image_data = base64.b64decode(contact["image_data"])
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((180, 180), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo, text="")
                self.image_label.image = photo
            else:
                self.image_label.config(image=None, text="Chưa có ảnh")
                self.current_image_data = None
        except Exception as e:
            print(f"Lỗi khi tải ảnh: {str(e)}")
            self.image_label.config(image=None, text="Lỗi tải ảnh")
            self.current_image_data = None
        
        # Cập nhật trạng thái các nút
        self.is_editing = True
        self.add_button.config(state=tk.DISABLED)
        self.update_button.config(state=tk.NORMAL)
        self.delete_button.config(state=tk.NORMAL)

    def load_contacts(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            # Count total contacts for pagination
            if self.current_search:
                query = {
                    "$or": [
                        {"name": {"$regex": self.current_search, "$options": "i"}},
                        {"phone": {"$regex": self.current_search, "$options": "i"}},
                        {"email": {"$regex": self.current_search, "$options": "i"}}
                    ]
                }
                self.total_contacts = self.collection.count_documents(query)
            else:
                self.total_contacts = self.collection.count_documents({})
            
            # Calculate total pages
            self.total_pages = math.ceil(self.total_contacts / self.contacts_per_page)
            if self.total_pages == 0:
                self.total_pages = 1
            
            # Ensure current page is valid
            if self.current_page > self.total_pages:
                self.current_page = self.total_pages
            
            # Update pagination display
            self.page_info.config(text=f"Trang {self.current_page} / {self.total_pages}")
            
            # Enable/disable navigation buttons
            self.prev_button.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
            self.next_button.config(state=tk.NORMAL if self.current_page < self.total_pages else tk.DISABLED)
            
            # Calculate skip value for pagination
            skip = (self.current_page - 1) * self.contacts_per_page
            
            # Query with pagination
            if self.current_search:
                contacts = self.collection.find(query).skip(skip).limit(self.contacts_per_page)
            else:
                contacts = self.collection.find().skip(skip).limit(self.contacts_per_page)
            
            for contact in contacts:
                # Hiển thị phần đầu của ID để tiện theo dõi
                contact_id = str(contact["_id"])
                
                # Kiểm tra xem liên hệ có ảnh không
                has_image = "Có" if contact.get("image_data") else "Không"
                
                self.tree.insert("", "end", values=(contact_id, contact["name"], contact["phone"], contact["email"], has_image))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách liên hệ: {str(e)}")

    def search_contacts(self, event=None):
        """Tìm kiếm liên hệ theo tên, số điện thoại hoặc email"""
        search_text = self.search_entry.get().strip().lower()
        self.current_search = search_text
        self.current_page = 1  # Reset to first page
        self.load_contacts()
        
        # Xóa tất cả các mục hiện tại
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        if not search_text:
            # Nếu không có văn bản tìm kiếm, tải lại tất cả liên hệ
            self.load_contacts()
            return
            
        try:
            # Tìm kiếm trong MongoDB
            query = {
                "$or": [
                    {"name": {"$regex": search_text, "$options": "i"}},
                    {"phone": {"$regex": search_text, "$options": "i"}},
                    {"email": {"$regex": search_text, "$options": "i"}}
                ]
            }
            results = self.collection.find(query)
            
            for contact in results:
                contact_id = str(contact["_id"])
                has_image = "Có" if contact.get("image_data") else "Không"
                self.tree.insert("", "end", values=(contact_id, contact["name"], contact["phone"], contact["email"], has_image))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {str(e)}")
    

    def open_chat(self):
        """Open chat window with selected contact"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn một liên hệ để chat")
            return
            
        item = self.tree.item(selected_item[0])
        values = item["values"]
        contact_id = values[0]
        contact_name = values[1]
        
        # Create chat window
        self.chat_window = tk.Toplevel(self.window)
        self.chat_window.title(f"Chat với {contact_name}")
        self.chat_window.geometry("500x600")
        self.chat_window.configure(bg="#f0f0f0")
        
        # Chat history frame
        chat_frame = tk.Frame(self.chat_window, bg="#f0f0f0")
        chat_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Chat history display with scrollbar
        chat_history_frame = tk.Frame(chat_frame, bg="#f0f0f0")
        chat_history_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        chat_scrollbar = tk.Scrollbar(chat_history_frame)
        chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat_history = tk.Text(chat_history_frame, wrap=tk.WORD, state=tk.DISABLED, 
                                yscrollcommand=chat_scrollbar.set, bg="white", font=("Arial", 11))
        self.chat_history.pack(fill="both", expand=True)
        chat_scrollbar.config(command=self.chat_history.yview)
        
        # Input frame
        input_frame = tk.Frame(chat_frame, bg="#f0f0f0")
        input_frame.pack(fill="x", padx=5, pady=5)
        
        self.message_entry = tk.Text(input_frame, height=2, width=40, font=("Arial", 11))
        self.message_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        self.message_entry.bind("<Return>", lambda event: self.send_message(contact_id, contact_name))
        
        send_button = tk.Button(input_frame, text="Gửi", command=lambda: self.send_message(contact_id, contact_name),
                            bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5)
        send_button.pack(side=tk.RIGHT, padx=5)
        
        # Button frame
        button_frame = tk.Frame(chat_frame, bg="#f0f0f0")
        button_frame.pack(fill="x", padx=5, pady=5)
        
        clear_chat_button = tk.Button(button_frame, text="Xóa lịch sử chat", 
                                    command=lambda: self.clear_chat_history(contact_id),
                                    bg="#F44336", fg="white", font=("Arial", 10), padx=10, pady=3)
        clear_chat_button.pack(side=tk.LEFT, padx=5)
        
        # Load chat history for this contact
        self.load_chat_history(contact_id, contact_name)
        
        # Set focus to message entry
        self.message_entry.focus_set()
        
    def send_message(self, contact_id, contact_name):
        """Send a message to the contact"""
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            return "break"
            
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Save message to database
        chat_message = {
            "contact_id": contact_id,
            "sender": "me",
            "message": message,
            "timestamp": timestamp
        }
        
        try:
            # Store messages in a new collection 'chat_messages'
            if 'chat_messages' not in self.db.list_collection_names():
                self.db.create_collection('chat_messages')
                
            self.db['chat_messages'].insert_one(chat_message)
            
            # Display message in chat window
            self.chat_history.config(state=tk.NORMAL)
            self.chat_history.insert(tk.END, f"Bạn ({timestamp}):\n", "sender")
            self.chat_history.insert(tk.END, f"{message}\n\n", "message")
            self.chat_history.see(tk.END)
            self.chat_history.config(state=tk.DISABLED)
            
            # Configure tags
            self.chat_history.tag_configure("sender", foreground="#007BFF", font=("Arial", 10, "bold"))
            self.chat_history.tag_configure("message", font=("Arial", 11))
            self.chat_history.tag_configure("receiver", foreground="#28A745", font=("Arial", 10, "bold"))
            
            # Clear message entry
            self.message_entry.delete("1.0", tk.END)
            
            # Simulate a response after a short delay (for demonstration)
            self.chat_window.after(1000, lambda: self.simulate_response(contact_id, contact_name))
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể gửi tin nhắn: {str(e)}")
        
        return "break"  # Prevent default Return behavior in Text widget
        
    def simulate_response(self, contact_id, contact_name):
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        responses = [
            f"Xin chào! Đây là tin nhắn tự động từ {contact_name}: Cảm ơn đã liên hệ, tôi sẽ trả lời ngay sau khi online.",
            # "Tôi sẽ liên hệ lại với bạn sau.",
            # "Cảm ơn vì đã nhắn tin. Tôi đang bận, sẽ trả lời sau.",
            # "Rất vui khi nhận được tin nhắn của bạn!",
            # "Ok, tôi đã nhận được thông tin."
        ]
        
        import random
        message = random.choice(responses)
        
        # Save message to database
        chat_message = {
            "contact_id": contact_id,
            "sender": "contact",
            "message": message,
            "timestamp": timestamp
        }
        
        try:
            self.db['chat_messages'].insert_one(chat_message)
            
            # Display message in chat window
            self.chat_history.config(state=tk.NORMAL)
            self.chat_history.insert(tk.END, f"{contact_name} ({timestamp}):\n", "receiver")
            self.chat_history.insert(tk.END, f"{message}\n\n", "message")
            self.chat_history.see(tk.END)
            self.chat_history.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Lỗi khi mô phỏng phản hồi: {str(e)}")
        
    def load_chat_history(self, contact_id, contact_name):
        """Load chat history for a specific contact"""
        try:
            messages = self.db['chat_messages'].find({"contact_id": contact_id}).sort("timestamp", 1)
            
            self.chat_history.config(state=tk.NORMAL)
            self.chat_history.delete("1.0", tk.END)
            
            # Configure tags
            self.chat_history.tag_configure("sender", foreground="#007BFF", font=("Arial", 10, "bold"))
            self.chat_history.tag_configure("message", font=("Arial", 11))
            self.chat_history.tag_configure("receiver", foreground="#28A745", font=("Arial", 10, "bold"))
            
            for msg in messages:
                if msg["sender"] == "me":
                    self.chat_history.insert(tk.END, f"Bạn ({msg['timestamp']}):\n", "sender")
                else:
                    self.chat_history.insert(tk.END, f"{contact_name} ({msg['timestamp']}):\n", "receiver")
                
                self.chat_history.insert(tk.END, f"{msg['message']}\n\n", "message")
            
            self.chat_history.see(tk.END)
            self.chat_history.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải lịch sử chat: {str(e)}")
        
    def clear_chat_history(self, contact_id):
        """Clear chat history for a specific contact"""
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa tất cả tin nhắn với liên hệ này?")
        if not confirm:
            return
            
        try:
            self.db['chat_messages'].delete_many({"contact_id": contact_id})
            
            # Clear display
            self.chat_history.config(state=tk.NORMAL)
            self.chat_history.delete("1.0", tk.END)
            self.chat_history.config(state=tk.DISABLED)
            
            messagebox.showinfo("Thông báo", "Đã xóa lịch sử chat thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa lịch sử chat: {str(e)}")
    def prev_page(self):
  
        if self.current_page > 1:
            self.current_page -= 1
            self.load_contacts()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_contacts()

    def change_page_size(self, event=None):
        """Change number of contacts per page"""
        try:
            self.contacts_per_page = int(self.page_size_var.get())
            self.current_page = 1  # Reset to first page
            self.load_contacts()
        except ValueError:
            pass

if __name__ == "__main__":
    app = MongoDB()
    app.window.mainloop()