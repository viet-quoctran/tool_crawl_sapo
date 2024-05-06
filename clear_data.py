import os
import pandas as pd
import psycopg2
from connectdb import connect_to_database
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
folder_path = 'C:\\Users\\Administrator\\Desktop\\tool_crawl_sapo\\data'
all_files = sorted(os.listdir(folder_path), key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
excel_file = next((file for file in all_files if file.endswith('.xlsx')), None)

conn = connect_to_database()
if conn is not None and excel_file:
    excel_file_path = os.path.join(folder_path, excel_file)
    print(f"Most recent Excel file: {excel_file}")
    print(f"Path to the Excel file: {excel_file_path}")
    print(f"Path exists: {os.path.exists(excel_file_path)}")

    try:
        df = pd.read_excel(excel_file_path, header=30)
        df.dropna(how='all', inplace=True)
        df['Ngày chứng từ'] = pd.to_datetime(df['Ngày chứng từ'], format='%d/%m/%Y %H:%M:%S')
        df['Month-Year'] = df['Ngày chứng từ'].dt.to_period('M').astype(str)
        df['Hour'] = df['Ngày chứng từ'].dt.hour
        monthly_revenue = df.groupby('Month-Year')['Số tiền thanh toán'].sum().reset_index(name='total_sales')
        hourly_revenue = df.groupby(['Month-Year', 'Hour'])['Số tiền thanh toán'].sum().reset_index(name='total_sales')
        
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_sales_report (
                month_year TEXT PRIMARY KEY,
                total_sales FLOAT
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hourly_sales_report (
                month_year TEXT,
                hour INT,
                total_sales FLOAT,
                PRIMARY KEY (month_year, hour)
            );
        ''')
        conn.commit()

        for _, row in monthly_revenue.iterrows():
            cursor.execute('''
                INSERT INTO monthly_sales_report (month_year, total_sales)
                VALUES (%s, %s)
                ON CONFLICT (month_year) DO UPDATE SET
                total_sales = monthly_sales_report.total_sales + EXCLUDED.total_sales;
            ''', (row['Month-Year'], row['total_sales']))

        for _, row in hourly_revenue.iterrows():
            cursor.execute('''
                INSERT INTO hourly_sales_report (month_year, hour, total_sales)
                VALUES (%s, %s, %s)
                ON CONFLICT (month_year, hour) DO UPDATE SET
                total_sales = hourly_sales_report.total_sales + EXCLUDED.total_sales;
            ''', (row['Month-Year'], row['Hour'], row['total_sales']))
        conn.commit()

        cursor.close()
        conn.close()
        print("Monthly and hourly revenue data have been successfully updated in the database.")
    except Exception as e:
        print("Error reading the Excel file or inserting data into the database:", e)
        if conn:
            conn.close()
else:
    print("Failed to establish a database connection or no Excel file found.")
    if conn:
        conn.close()
