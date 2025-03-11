import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient
from pprint import pprint
import sys

class MongoCRUD:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['python_2']
        self.collection = self.db['users']

        self.window = tk.Tk()
        self.window.title("MongoDB CRUD - Quản Lý Người Dùng")
        self.window.geometry("700x400")

        #Khung(Frame) để chứa trường nhập liệu
        input_frame = tk.LabelFrame(self.window, text="Thông tin người dùng", padx=10, pady=10)
        input_frame.pack(padx=10, pady=5, fill='x')

        #Các trường nhập liệu
        tk.Label(input_frame, text="Tên:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Tuổi:").grid(row=1, column=0, padx=5, pady=5)
        self.age_entry = tk.Entry(input_frame)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(input_frame)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        #Frame cho các nút chức năng
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)
        
        #Các nút chức năng
        tk.Button(button_frame, text="Thêm", command=self.create).pack(side = tk.LEFT, padx=5)
        tk.Button(button_frame, text="Danh sách", command=self.read).pack(side = tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cập nhật", command=self.update).pack(side = tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xóa", command=self.delete).pack(side = tk.LEFT, padx=5)
        tk.Button(button_frame, text="Thoát", command=self.window.quit).pack(side = tk.LEFT, padx=5)

        #Treeview để hiển thị dữ liệu dạng bảng
        self.tree = ttk.Treeview(self.window, columns=("ID", "Tên", "Tuổi", "Email"), show="headings")
        self.tree.heading("ID", text="ID")   
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Tuổi", text="Tuổi")
        self.tree.heading("Email", text="Email")

        self.tree.column("ID", width=180)
        self.tree.column("Tên", width=150)
        self.tree.column("Tuổi", width=50, anchor="center")
        self.tree.column("Email", width=200)

        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

    def clear_entries(self):
            self.name_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

    def create(self):
            try:          
                name = self.name_entry.get()
                age = self.age_entry.get()
                email = self.email_entry.get()
                
                if not all([name, age, email]):
                    messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin!")
                    return
                user = {"name": name, "age": int(age), "email": email}
                result = self.collection.insert_one(user)

                self.clear_entries()
                self.read()
                messagebox.showinfo("Thành công", f"Đã thêm người dùng mới với ID: {result.inserted_id}")
            except ValueError:
                messagebox.showerror("Error", "Tuổi phải là số nguyên!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")
            
    def read(self):
            self.tree.delete(*self.tree.get_children())
            users = self.collection.find()
            for user in users:
                self.tree.insert("", "end", values=(str(user["_id"]), user["name"], user["age"], user["email"]))
    def update(self):
            try:
                email = self.email_entry.get()
                if not email:
                    messagebox.showerror("Error", "Vui lòng nhập Email!")
                    return
                update_data = {}
                if self.name_entry.get():
                    update_data["name"] = self.name_entry.get()
                if self.age_entry.get():
                    update_data["age"] = int(self.age_entry.get())
                
                if update_data:
                    result = self.collection.update_one({"email": email}, {"$set": update_data})
                    self.clear_entries()
                    self.read()
                    if result.modified_count > 0:
                        messagebox.showinfo("Thành công", f"Đã cập nhật thông tin người dùng có Email: {email}")
                    else:
                        messagebox.showerror("Error", f"Không tìm thấy người dùng có Email: {email}")
                else:
                    messagebox.showerror("Error", "Vui lòng nhập ít nhất một trường cần cập nhật!")
            except ValueError:
                messagebox.showerror("Error", "Tuổi phải là số nguyên!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

    def delete(self):
            try:
                email = self.email_entry.get()
                if not email:
                    messagebox.showerror("Error", "Vui lòng nhập Email!")
                    return
                result = self.collection.delete_one({"email":email})
                self.clear_entries()
                self.read()
                if result.deleted_count > 0:
                    messagebox.showinfo("Thành công", f"Đã xóa người dùng có Email: {email}")
                else:
                    messagebox.showerror("Error", f"Không tìm thấy người dùng có Email: {email}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")
        
    def quit(self):
            self.client.close()
            self.window.quit()
            sys.exit(0)
        
    def run(self):
            self.window.mainloop()
    
if __name__ == "__main__":
    app = MongoCRUD()
    app.run()



