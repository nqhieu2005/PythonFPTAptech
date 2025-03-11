from pymongo import MongoClient
from pprint import pprint
import sys



class MongoCRUD:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['python']
        self.collection = self.db['users']
    

    def create(self):
        print("\n=== Thêm người dùng ===")
        name = input("Nhập tên: ")
        age = int(input("Nhập tuổi: "))
        email = input("Nhập email: ")

        user = {
            "name": name,
            "age": age,
            "email": email
        }
        
        result = self.collection.insert_one(user)
        print(f"Thêm người dùng thành công. ID: {result.inserted_id}")
    def read(self):
        print("\n=== Danh sách người dùng ===")
        users = self.collection.find()
        for user in users:
            pprint(user)
    def update(self):
        print("\n=== Cập nhật người dùng ===")
        email = input("Nhập email người dùng cần cập nhật: ")
        print("Nhập thông tin mới(để trống nếu không muốn thay đổi):")
        new_name = input("Nhập tên: ")
        new_age = input("Nhập tuổi: ")

        update_data = {}
        if new_name :
            update_data["name"] = new_name
        if new_age:
            update_data["age"] = new_age
        if update_data:
            result = self.collection.update_one(
                {"email": email},
                {"$set": update_data}
            )
            if result.modified_count > 0:
                print("Cập nhật người dùng thành công")
            else:
                print("Không tìm thấy người dùng cần cập nhật hoặc không có thay đổi")
    def delete(self):
        print("\n=== Xóa người dùng ===")
        email = input("Nhập email người dùng cần xóa: ")
        result = self.collection.delete_one({"email": email})
        if result.deleted_count > 0:
            print("Xóa người dùng thành công")
        else:
            print("Không tìm thấy người dùng cần xóa")
    def menu(self):
        while True:
            print("\n=== MENU ===")
            print("1. Thêm người dùng")
            print("2. Danh sách người dùng")
            print("3. Cập nhật người dùng")
            print("4. Xóa người dùng")
            print("5. Thoát")

            choice = input("Chọn chức năng: ")
            if choice == '1':
                self.create()
            elif choice == '2':
                self.read()
            elif choice == '3':
                self.update()
            elif choice == '4':
                self.delete()
            elif choice == '5':
                print("Tạm biệt!")
                self.client.close()
                sys.exit(0) 
            else:
                print("Chức năng không hợp lệ")
def main():
    try:
        crud = MongoCRUD()
        crud.menu()
    except Exception as e:
        print(f"Lỗi: {e}")
if __name__ == "__main__":
    main()

