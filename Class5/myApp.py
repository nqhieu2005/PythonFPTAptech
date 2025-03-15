from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sys

class MongoDB:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['phoneBook']
        self.collection = self.db['list']

        self.window = tk.Tk()
        self.window.title("Phone Book")
        self.window.geometry("900x550")

        self.image_path = ""

        input_frame = tk.LabelFrame(self.window, text="Thông tin liên hệ", padx=10, pady=10)
        input_frame.pack(padx=10, pady=5, fill='x')

        # Sử dụng grid cho tất cả các widget trong input_frame
        tk.Label(input_frame, text="Họ và tên:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Số điện thoại:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.phone_entry = tk.Entry(input_frame, width=30)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = tk.Entry(input_frame, width=30)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        # Ảnh đại diện (sử dụng grid thay vì pack)
        self.image_label = tk.Label(input_frame, text="Chưa có ảnh", width=15, height=7, relief="solid")
        self.image_label.grid(row=0, column=2, rowspan=3, padx=10, pady=5)

        # Nút chọn ảnh đại diện (sử dụng grid)
        self.select_image_btn = tk.Button(input_frame, text="Chọn ảnh", command=self.select_image)
        self.select_image_btn.grid(row=3, column=2, padx=5, pady=5)

        # Nút thêm & cập nhật danh bạ (sử dụng grid)
        self.add_button = tk.Button(input_frame, text="Thêm", command=self.add_contact)
        self.add_button.grid(row=3, column=1, padx=5, pady=5)

        # Danh sách hiển thị
        self.tree = ttk.Treeview(self.window, columns=("Tên", "Số điện thoại", "Email", "Ảnh"), show="headings")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Số điện thoại", text="Số điện thoại")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Ảnh", text="Ảnh")
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        # Load danh sách liên hệ
        self.load_contacts()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.image_label.config(image='', text='Chưa có ảnh')
        self.image_path = ""

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path = file_path
            image = Image.open(file_path)
            image = image.resize((100, 100))
            image = ImageTk.PhotoImage(image)
            self.image_label.config(image=image, text= '')
            self.image_label.image = image
            
    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if not name or not phone or not email:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return
        contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "image": self.image_path
        }
        result = self.collection.insert_one(contact)

        self.load_contacts()
        self.clear_entries()

        messagebox.showinfo("Thông báo", "Thêm liên hệ thành công")

    def load_contacts(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        contacts = self.collection.find()
        for contact in contacts:
            self.tree.insert("", "end", values=(contact["name"], contact["phone"], contact["email"], contact["image"]))


if __name__ == "__main__":
    app = MongoDB()
    app.window.mainloop()