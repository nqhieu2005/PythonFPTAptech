import tkinter as tk

class RecipeListScreen:
    def __init__(self, root, controller):
        self.frame = tk.Frame(root, bg="#fff3e0")  # Khung với màu nền vàng nhạt
        self.controller = controller

        # Tiêu đề lớn, màu cam
        tk.Label(self.frame, text="Recipes", font=("Helvetica", 36, "bold"), bg="#fff3e0", fg="#f39c12").pack(pady=50)

        # Khung chứa danh sách món
        self.recipe_list = tk.Frame(self.frame, bg="#fff3e0")
        self.recipe_list.pack(pady=20)

        # Nút Back
        tk.Button(self.frame, text="Back", font=("Helvetica", 14), bg="#e74c3c", fg="white", relief="flat",
                  command=self.controller.show_categories, padx=20, pady=10).pack(pady=20)

    def update_recipes(self, recipes):
        # Xóa các widget cũ
        for widget in self.recipe_list.winfo_children():
            widget.destroy()

        # Hiển thị danh sách món mới
        for recipe in recipes:
            frame = tk.Frame(self.recipe_list, bg="#ffffff", borderwidth=1, relief="solid")  # Khung món
            frame.pack(fill="x", pady=10, padx=50)

            # Hiển thị hình ảnh ngẫu nhiên
            image = self.controller.get_random_image()
            if image:
                img_label = tk.Label(frame, image=image, bg="#ffffff")
                img_label.image = image  # Giữ tham chiếu ảnh
                img_label.pack(side="left", padx=10)

            # Tên món
            tk.Label(frame, text=recipe["name"], font=("Helvetica", 16, "bold"), fg="#2c3e50", bg="#ffffff",
                     wraplength=500).pack(side="left", padx=10, pady=5)

            # Nút View
            tk.Button(frame, text="View", font=("Helvetica", 12), bg="#f1c40f", fg="white", relief="flat",
                      command=lambda rid=recipe["id"]: self.controller.show_recipe_detail(rid), padx=15, pady=5).pack(side="right", padx=10)