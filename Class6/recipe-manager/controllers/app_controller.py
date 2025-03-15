from models.data import categories, recipes, save_feedback, get_feedbacks, get_random_image
from views.welcome_screen import WelcomeScreen
from views.category_screen import CategoryScreen
from views.recipe_list_screen import RecipeListScreen
from views.recipe_detail_screen import RecipeDetailScreen

class AppController:
    def __init__(self, root):
        self.root = root  # Cửa sổ chính
        self.root.title("Recipes")  # Tiêu đề cửa sổ
        self.root.geometry("1000x800")  # Kích thước cửa sổ
        self.root.configure(bg="#fff3e0")  # Màu nền cửa sổ

        # Lưu ID thể loại và món hiện tại
        self.current_category_id = None
        self.current_recipe_id = None

        # Khởi tạo các màn hình
        self.welcome_screen = WelcomeScreen(root, self)
        self.category_screen = CategoryScreen(root, self)
        self.recipe_list_screen = RecipeListScreen(root, self)
        self.recipe_detail_screen = RecipeDetailScreen(root, self)

        # Hiển thị màn hình chào mừng đầu tiên
        self.show_welcome()

    def show_frame(self, frame):
        # Ẩn tất cả các khung
        for f in (self.welcome_screen.frame, self.category_screen.frame, self.recipe_list_screen.frame, self.recipe_detail_screen.frame):
            f.pack_forget()

        # Hiển thị khung được chọn
        frame.pack(fill="both", expand=True)

    def get_categories(self):
        return categories  # Trả về danh sách thể loại

    def get_recipes_by_category(self, category_id):
        return [r for r in recipes if r["categoryId"] == category_id]  # Lọc món theo thể loại

    def get_recipe_by_id(self, recipe_id):
        return next(r for r in recipes if r["id"] == recipe_id)  # Lấy món theo ID

    def get_random_image(self):
        return get_random_image()  # Gọi hàm lấy ảnh ngẫu nhiên từ Model

    def save_feedback(self, recipe_name, feedback_text):
        save_feedback(recipe_name, feedback_text)  # Lưu góp ý vào MongoDB

    def get_feedbacks(self, recipe_name):
        return get_feedbacks(recipe_name)  # Lấy danh sách góp ý

    def show_welcome(self):
        self.show_frame(self.welcome_screen.frame)  # Hiển thị màn hình chào mừng

    def show_categories(self):
        self.show_frame(self.category_screen.frame)  # Hiển thị màn hình danh mục

    def show_recipes(self, category_id):
        self.current_category_id = category_id  # Cập nhật ID thể loại
        recipes_data = self.get_recipes_by_category(category_id)  # Lấy danh sách món
        self.recipe_list_screen.update_recipes(recipes_data)  # Cập nhật giao diện
        self.show_frame(self.recipe_list_screen.frame)  # Hiển thị màn hình danh sách

    def show_recipe_detail(self, recipe_id):
        self.current_recipe_id = recipe_id  # Cập nhật ID món
        recipe = self.get_recipe_by_id(recipe_id)  # Lấy thông tin món
        self.recipe_detail_screen.update_details(recipe)  # Cập nhật giao diện
        self.show_frame(self.recipe_detail_screen.frame)  # Hiển thị màn hình chi tiết