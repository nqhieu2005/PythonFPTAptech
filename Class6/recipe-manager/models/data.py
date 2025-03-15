from pymongo import MongoClient
from PIL import Image, ImageTk
import random
import os

client = MongoClient('mongodb://localhost:27017/')
db = client['recipe_manager']
feedback_collection = db['feedback']

categories = [
    {"id": 1, "name": "Main Courses"},
    {"id": 2, "name": "Desserts"},
    {"id": 3, "name": "Appetizers"},
    {"id": 4, "name": "Beverages"}
]

recipes = [
    # Main Courses (10 món)
    {"id": 1, "categoryId": 1, "name": "Spiced Bean Tacos", "ingredients": "Iceberg lettuce, kidney beans, sour cream, jalapeños...", "steps": "Heat oil, add beans, serve in tacos...", "time": "25 min", "serves": "2"},
    {"id": 2, "categoryId": 1, "name": "Grilled Chicken", "ingredients": "Chicken, olive oil, garlic, rosemary...", "steps": "Marinate, grill for 20 min...", "time": "30 min", "serves": "4"},
    {"id": 3, "categoryId": 1, "name": "Beef Stir-Fry", "ingredients": "Beef, bell peppers, soy sauce...", "steps": "Stir-fry beef and veggies...", "time": "20 min", "serves": "3"},
    {"id": 4, "categoryId": 1, "name": "Pasta Primavera", "ingredients": "Pasta, zucchini, tomatoes, cream...", "steps": "Cook pasta, mix with sauce...", "time": "25 min", "serves": "4"},
    {"id": 5, "categoryId": 1, "name": "Salmon with Lemon", "ingredients": "Salmon, lemon, butter, herbs...", "steps": "Bake at 180°C for 15 min...", "time": "20 min", "serves": "2"},
    {"id": 6, "categoryId": 1, "name": "Vegetable Curry", "ingredients": "Potatoes, peas, coconut milk...", "steps": "Simmer for 30 min...", "time": "35 min", "serves": "4"},
    {"id": 7, "categoryId": 1, "name": "Lamb Roast", "ingredients": "Lamb, garlic, rosemary, potatoes...", "steps": "Roast at 200°C for 1 hour...", "time": "70 min", "serves": "6"},
    {"id": 8, "categoryId": 1, "name": "Shrimp Scampi", "ingredients": "Shrimp, garlic, butter, pasta...", "steps": "Sauté shrimp, toss with pasta...", "time": "20 min", "serves": "3"},
    {"id": 9, "categoryId": 1, "name": "Pork Chops", "ingredients": "Pork, apple sauce, thyme...", "steps": "Grill for 15 min...", "time": "20 min", "serves": "2"},
    {"id": 10, "categoryId": 1, "name": "Turkey Casserole", "ingredients": "Turkey, cheese, cream, veggies...", "steps": "Bake at 180°C for 40 min...", "time": "50 min", "serves": "6"},

    # Desserts (10 món)
    {"id": 11, "categoryId": 2, "name": "Chocolate Cake", "ingredients": "Flour, cocoa, sugar, eggs...", "steps": "Bake at 180°C for 35 min...", "time": "50 min", "serves": "8"},
    {"id": 12, "categoryId": 2, "name": "Apple Pie", "ingredients": "Apples, cinnamon, dough...", "steps": "Bake at 200°C for 45 min...", "time": "60 min", "serves": "6"},
    {"id": 13, "categoryId": 2, "name": "Cheesecake", "ingredients": "Cream cheese, sugar, graham...", "steps": "Chill for 4 hours...", "time": "240 min", "serves": "8"},
    {"id": 14, "categoryId": 2, "name": "Lemon Tart", "ingredients": "Lemon, eggs, sugar, crust...", "steps": "Bake at 160°C for 30 min...", "time": "40 min", "serves": "6"},
    {"id": 15, "categoryId": 2, "name": "Brownie", "ingredients": "Chocolate, butter, flour...", "steps": "Bake at 180°C for 25 min...", "time": "35 min", "serves": "8"},
    {"id": 16, "categoryId": 2, "name": "Fruit Sorbet", "ingredients": "Berries, sugar, water...", "steps": "Freeze for 2 hours...", "time": "120 min", "serves": "4"},
    {"id": 17, "categoryId": 2, "name": "Caramel Pudding", "ingredients": "Milk, sugar, eggs...", "steps": "Steam for 20 min...", "time": "30 min", "serves": "4"},
    {"id": 18, "categoryId": 2, "name": "Pecan Pie", "ingredients": "Pecans, syrup, pie crust...", "steps": "Bake at 180°C for 50 min...", "time": "60 min", "serves": "6"},
    {"id": 19, "categoryId": 2, "name": "Tiramisu", "ingredients": "Coffee, mascarpone, ladyfingers...", "steps": "Chill for 6 hours...", "time": "360 min", "serves": "8"},
    {"id": 20, "categoryId": 2, "name": "Ice Cream", "ingredients": "Cream, sugar, vanilla...", "steps": "Churn for 20 min...", "time": "30 min", "serves": "4"},

    # Appetizers (10 món)
    {"id": 21, "categoryId": 3, "name": "Caprese Salad", "ingredients": "Tomato, mozzarella, basil...", "steps": "Layer and drizzle with oil...", "time": "10 min", "serves": "2"},
    {"id": 22, "categoryId": 3, "name": "Bruschetta", "ingredients": "Bread, tomatoes, garlic...", "steps": "Toast and top with mix...", "time": "15 min", "serves": "4"},
    {"id": 23, "categoryId": 3, "name": "Stuffed Mushrooms", "ingredients": "Mushrooms, cheese, breadcrumbs...", "steps": "Bake at 180°C for 20 min...", "time": "25 min", "serves": "6"},
    {"id": 24, "categoryId": 3, "name": "Deviled Eggs", "ingredients": "Eggs, mayonnaise, mustard...", "steps": "Boil, mix, and fill...", "time": "20 min", "serves": "4"},
    {"id": 25, "categoryId": 3, "name": "Spring Rolls", "ingredients": "Veggies, wrappers, sauce...", "steps": "Roll and fry for 5 min...", "time": "15 min", "serves": "6"},
    {"id": 26, "categoryId": 3, "name": "Cheese Platter", "ingredients": "Cheese, grapes, crackers...", "steps": "Arrange on platter...", "time": "10 min", "serves": "4"},
    {"id": 27, "categoryId": 3, "name": "Garlic Bread", "ingredients": "Bread, butter, garlic...", "steps": "Bake at 200°C for 10 min...", "time": "15 min", "serves": "4"},
    {"id": 28, "categoryId": 3, "name": "Chicken Wings", "ingredients": "Wings, sauce, spices...", "steps": "Bake at 200°C for 30 min...", "time": "40 min", "serves": "6"},
    {"id": 29, "categoryId": 3, "name": "Hummus with Pita", "ingredients": "Chickpeas, tahini, pita...", "steps": "Blend and serve...", "time": "15 min", "serves": "4"},
    {"id": 30, "categoryId": 3, "name": "Mini Quiches", "ingredients": "Eggs, cheese, pastry...", "steps": "Bake at 180°C for 20 min...", "time": "30 min", "serves": "6"},

    # Beverages (10 món)
    {"id": 31, "categoryId": 4, "name": "Iced Coffee", "ingredients": "Coffee, ice, milk...", "steps": "Brew and chill...", "time": "5 min", "serves": "1"},
    {"id": 32, "categoryId": 4, "name": "Lemonade", "ingredients": "Lemon, sugar, water...", "steps": "Mix and serve with ice...", "time": "10 min", "serves": "2"},
    {"id": 33, "categoryId": 4, "name": "Green Smoothie", "ingredients": "Spinach, banana, yogurt...", "steps": "Blend for 1 min...", "time": "5 min", "serves": "1"},
    {"id": 34, "categoryId": 4, "name": "Hot Chocolate", "ingredients": "Cocoa, milk, sugar...", "steps": "Heat and stir...", "time": "10 min", "serves": "2"},
    {"id": 35, "categoryId": 4, "name": "Fruit Punch", "ingredients": "Juices, fruits, soda...", "steps": "Mix and chill...", "time": "15 min", "serves": "6"},
    {"id": 36, "categoryId": 4, "name": "Mint Tea", "ingredients": "Mint, water, honey...", "steps": "Steep for 5 min...", "time": "10 min", "serves": "2"},
    {"id": 37, "categoryId": 4, "name": "Mango Lassi", "ingredients": "Mango, yogurt, milk...", "steps": "Blend until smooth...", "time": "5 min", "serves": "2"},
    {"id": 38, "categoryId": 4, "name": "Spiced Chai", "ingredients": "Tea, spices, milk...", "steps": "Boil and strain...", "time": "15 min", "serves": "2"},
    {"id": 39, "categoryId": 4, "name": "Coconut Water", "ingredients": "Coconut, ice...", "steps": "Serve fresh...", "time": "5 min", "serves": "1"},
    {"id": 40, "categoryId": 4, "name": "Berry Infused Water", "ingredients": "Berries, water, mint...", "steps": "Infuse for 1 hour...", "time": "60 min", "serves": "4"},
]

# Hàm lưu góp ý vào MongoDB
def save_feedback(recipe_name, feedback_text):
    feedback_data = {"recipeId": recipe_name, "feedback": feedback_text}
    feedback_collection.insert_one(feedback_data)

# Hàm lấy danh sách góp ý từ MongoDB
def get_feedbacks(recipe_name):
    return list(feedback_collection.find({"recipeId": recipe_name}))

# Hàm lấy ngẫu nhiên ảnh từ thư mục Images
def get_random_image():
    image_files = [f"food{i}.jpeg" for i in range (1, 41)]
    image_file = random.choice(image_files)
    image_path = os.path.join("images", image_file)
    try:
        img = Image.open(image_path).resize((400, 300), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except FileNotFoundError:
        print(f"Error: Image file {image_path} not found")
        return None