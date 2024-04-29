import os
import pandas as pd
import psycopg2
from connectdb import connect_to_database

# Define the path to the folder containing the data
folder_path = 'C:\\Users\\\Administrator\\Desktop\\tool_crawl_sapo\\data'

# List and sort all files by modification time in descending order
all_files = sorted(os.listdir(folder_path), key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)

# Find the most recent Excel file
excel_file = next((file for file in all_files if file.endswith('.xlsx')), None)
conn = connect_to_database()
if excel_file:
    excel_file_path = os.path.join(folder_path, excel_file)
    print(f"Most recent Excel file: {excel_file}")
    print(f"Path to the Excel file: {excel_file_path}")
    print(f"Path exists: {os.path.exists(excel_file_path)}")

    try:
        df = pd.read_excel(excel_file_path, header=30)
        df.dropna(how='all', inplace=True)
        df['Ngày chứng từ'] = pd.to_datetime(df['Ngày chứng từ'], format='%d/%m/%Y %H:%M:%S')
        df['Giờ'] = df['Ngày chứng từ'].dt.hour

        # Corrected grouping for daily and hourly revenue
        daily_revenue = df.groupby(df['Ngày chứng từ'].dt.date)['Số tiền thanh toán'].sum().reset_index(name='total_sales')
        hourly_revenue = df.groupby([df['Ngày chứng từ'].dt.date, 'Giờ'])['Số tiền thanh toán'].sum().reset_index(name='total_sales')

        if conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_sales_report (
                    date DATE,
                    total_sales FLOAT
                );
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hourly_sales_report (
                    date DATE,
                    hour INT,
                    total_sales FLOAT
                );
            ''')
            conn.commit()

            # Inserting daily revenue
            for _, row in daily_revenue.iterrows():
                cursor.execute('INSERT INTO daily_sales_report (date, total_sales) VALUES (%s, %s)', (row['Ngày chứng từ'], row['total_sales']))

            # Inserting hourly revenue
            for _, row in hourly_revenue.iterrows():
                cursor.execute('INSERT INTO hourly_sales_report (date, hour, total_sales) VALUES (%s, %s, %s)', (row['Ngày chứng từ'], row['Giờ'], row['total_sales']))
            conn.commit()
            cursor.close()
        conn.close()
        print("Data has been successfully inserted into the database.")
    except Exception as e:
        print("Error reading the Excel file or inserting data into the database:", e)
else:
    print("No Excel file found in the directory.")
