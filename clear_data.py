import os
import pandas as pd
import connectdb
from io import StringIO
# Thư mục chứa các file Excel
folder_path = 'C:\\Users\\Admin\\Desktop\\Selenium\\data'

# Lấy danh sách tất cả các file trong thư mục và sắp xếp theo thời gian tạo (mới nhất đầu tiên)
all_files = sorted(os.listdir(folder_path), key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)

# Lọc ra file Excel đầu tiên trong danh sách (file mới nhất)
excel_file = next((file for file in all_files if file.endswith('.xlsx')), None)

if excel_file:
    # Đường dẫn đến file Excel mới nhất
    excel_file_path = os.path.join(folder_path, excel_file)
    
    # In ra tên của file Excel mới nhất
    print("File Excel gần nhất:", excel_file)
    
    # Kiểm tra đường dẫn của file Excel
    print("Đường dẫn đến file Excel:", excel_file_path)
    print("Đường dẫn tồn tại:", os.path.exists(excel_file_path))
    
    # Sử dụng pandas để đọc file Excel
    try:
        df = pd.read_excel(excel_file_path, header=2, usecols='A:AO')
        df['Số lượng'] = pd.to_numeric(df['Số lượng'], errors='coerce').fillna(0).astype(int)
        df['Ngày hoàn thành'] = pd.to_datetime(df['Ngày hoàn thành'], format='%d/%m/%Y %H:%M:%S')
        df_clear = df.loc[:, ['Mã ĐH', 'Ngày hoàn thành', 'Mã sản phẩm', 'Tên sản phẩm', 'Số lượng', 'Đơn vị tính', 'Đơn giá', 'CK tổng đơn hàng']]
        df_new = df_clear.rename(columns={
            'Mã ĐH': 'ma_dh',
            'Ngày hoàn thành': 'ngay_hoan_thanh',
            'Mã sản phẩm': 'ma_san_pham',
            'Tên sản phẩm': 'ten_san_pham',
            'Số lượng': 'so_luong',
            'Đơn vị tính': 'don_vi_tinh',
            'Đơn giá': 'don_gia',
            'CK tổng đơn hàng': 'ck_tong_don_hang'
        }).iloc[1:]
        print(df_new.info)
        df_dress = df_new[df_new['ten_san_pham'].str.contains('Đầm', na=False)]

        # In ra DataFrame chứa các dòng có 'ten_san_pham' chứa chuỗi "Đầm"
        print(df_dress)
        # Kết nối đến cơ sở dữ liệu PostgreSQL
        # conn = connectdb.connect_to_database()
        
        # if conn is not None:
        #     # Tạo một chuỗi kết nối I/O để ghi dữ liệu DataFrame vào database
        #     output = StringIO()
        #     df_new.to_csv(output, sep='\t', header=False, index=False)
        #     output.seek(0)
            
        #     # Tạo một cursor để thực hiện các câu lệnh SQL
        #     cursor = conn.cursor()
            
        #     # Copy dữ liệu từ chuỗi kết nối I/O vào table "oders" trong cơ sở dữ liệu
        #     cursor.copy_from(output, 'orders', null='', columns=df_new.columns)
            
        #     # Commit các thay đổi vào cơ sở dữ liệu
        #     conn.commit()
            
        #     # Đóng cursor và kết nối
        #     cursor.close()
        #     conn.close()
            
        #     print("Dữ liệu đã được lưu vào cơ sở dữ liệu thành công!")
        # else:
        #     print("Không thể kết nối đến cơ sở dữ liệu.")
    except Exception as e:
        print("Lỗi khi đọc file Excel:", e)
else:
    print("Không tìm thấy file Excel trong thư mục.")



