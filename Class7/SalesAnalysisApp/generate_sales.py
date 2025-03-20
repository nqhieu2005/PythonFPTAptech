import pandas  as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sales_data(num_records=1000):
    start_date = datetime(2022, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(num_records)]
    base_sales = 1000
    sales = [base_sales + i * 5 + random.uniform(-200, 200) for i in range(num_records)]
    df = pd.DataFrame({'Date': dates, 'Sales': sales})
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    df.to_csv('sales_data.csv',index=False)
    print(f"Da tao file 'sales_data.csv' voi {num_records} ban ghi")

generate_sales_data(1000)