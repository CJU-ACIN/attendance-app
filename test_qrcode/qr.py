import qrcode

# SQL 쿼리문
query = "INSERT INTO my_table (column1, column2) VALUES ('value1', 'value2')"

# QR 코드 생성
qr = qrcode.QRCode()
qr.add_data(query)
qr.make()
img = qr.make_image(fill_color="black", back_color="white")
img.save("qr_code.png")
