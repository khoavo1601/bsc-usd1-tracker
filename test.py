import requests

TOKEN = "8086894988:AAFueaG7-pInd_oUF0r7WffBQRfiu_8qr08"
CHAT_ID = "990309170"

message = "✅ Test thành công: Bot Telegram đã hoạt động!"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
response = requests.post(url, data={"chat_id": CHAT_ID, "text": message})

print("Gửi thành công" if response.status_code == 200 else "Lỗi gửi:", response.text)
