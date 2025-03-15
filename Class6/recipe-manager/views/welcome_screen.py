import tkinter as tk

class WelcomeScreen:
    def __init__(self, root, controller):
        self.frame = tk.Frame(root, bg = '#fff3e0')
        self.controller = controller

        tk.Label(self.frame, text = "Welcome to Recipes", font=("Helvetica", 36, "bold"), bg="#fff3e0", fg="#f39c12").pack(pady=50)

        self.welcome_image = tk.Label(self.frame, bg='#fff3e0', borderwidth=2, relief="solid")
        self.welcome_image.pack(pady=20)
        image = self.controller.get_random_image()
        if image:
            self.welcome_image.image = image
            self.welcome_image.config(image=image)
        tk.Button(self.frame, text="Start Cooking", font=("Helvetica", 16), bg="#f1c40f", fg="white", relief="flat", command=self.controller.show_categories, padx = 30, pady=15, borderwidth=0).pack(pady=30)