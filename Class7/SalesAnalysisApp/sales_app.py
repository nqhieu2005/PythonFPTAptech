import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numbers as np

def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            global df
            df = pd.read_csv(file_path)
            lbl_status.config(text=f"Da tai: {file_path.split('/')[-1]} | {len(df)} ban ghi ")
            btn_analyze.config(state="normal")
            btn_predict.config(state="normal")
        except Exception as e:
            messagebox.showerror("Loi", f"Khong the tai file: {e}")
def analyze_data():
    if 'df' not in globals():
        messagebox.showwarning("Canh bao", "Vui long tai file CSV truoc")
        return
    analysis_window = tk.Toplevel(root)
    analysis_window.title("Phân tích dữ liệu bán hàng")
    analysis_window.geometry("800x600")
    analysis_window.configure(bg="f0f0f0")
    stats = df.describe().to_string()
    stats_label = tk.Label(analysis_window, text = "Thống kê cơ bản: ", font=("Arial", 12, "bold"))
