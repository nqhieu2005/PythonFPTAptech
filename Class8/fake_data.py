from pymongo import MongoClient
from faker import Faker
import base64
import os

# Kết nối đến MongoDB
client = MongoClient("mongodb://localhost:27017/")  
db = client["phoneBook"]
collection = db["list"]

# Tạo dữ liệu giả
fake = Faker()

def generate_fake_image():
    """Tạo chuỗi base64 giả lập thay cho ảnh"""
    return base64.b64encode(os.urandom(100)).decode('utf-8')

# Danh sách lưu trữ các bản ghi giả lập
data_list = []

for _ in range(50):  
    data = {
        "name": fake.name(),
        "phone": fake.phone_number(),
        "email": fake.email(),
        "image_data": generate_fake_image()
    }
    data_list.append(data)

# Chèn vào MongoDB
collection.insert_many(data_list)

print(f"Đã chèn {len(data_list)} bản ghi vào MongoDB!")
