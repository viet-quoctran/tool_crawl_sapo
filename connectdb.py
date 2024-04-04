import os
import urllib.parse as up
import psycopg2

def connect_to_database():
    try:
        # Parse thông tin kết nối từ URL
        up.uses_netloc.append("postgres")
        url = up.urlparse("postgres://tofzkkbb:nytl6GEmWB2oKM7CEicSbLjWZqrFcCDC@rain.db.elephantsql.com/tofzkkbb")
        
        # Kết nối đến cơ sở dữ liệu PostgreSQL
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        
        # In ra thông báo nếu kết nối thành công
        print("Kết nối đến cơ sở dữ liệu thành công!")
        
        # Trả về đối tượng kết nối
        return conn
    except Exception as e:
        # Xử lý lỗi nếu có bất kỳ lỗi nào xảy ra khi kết nối
        print("Lỗi khi kết nối đến cơ sở dữ liệu:", e)
        return None

# Gọi hàm connect_to_database() để thực hiện kết nối
conn = connect_to_database()
