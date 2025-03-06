class ProductManager:
    def __init__(self):
        self.products = set()

    def add_product(self, product_name):
        if product_name in self.products:
            print(f"Product '{product_name}' already exists.")
        else:
            self.products.add(product_name)
            print(f"Product '{product_name}' added.")

    def remove_product(self, product_name):
        if product_name in self.products:
            self.products.remove(product_name)
            print(f"Product '{product_name}' removed.")
        else:
            print(f"Product '{product_name}' does not exist.")

    def list_products(self):
        if self.products:
            print("Products in store:")
            for product in self.products:
                print(f"- {product}")
        else:
            print("No products in store.")

if __name__ == "__main__":
    manager = ProductManager()
    while True:
        print("\n1. Add product")
        print("2. Remove product")
        print("3. List products")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            product_name = input("Enter product name to add: ")
            manager.add_product(product_name)
        elif choice == '2':
            product_name = input("Enter product name to remove: ")
            manager.remove_product(product_name)
        elif choice == '3':
            manager.list_products()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")