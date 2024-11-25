import os
from telethon import TelegramClient, events
import asyncio
from datetime import datetime

# الحصول على بيانات الحساب من متغيرات البيئة
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SESSION_NAME = os.getenv('SESSION_NAME')

# الحصول على توكن البوت من متغير البيئة
BOT_TOKEN = os.getenv('BOT_TOKEN')

# إنشاء اتصال مع تيليغرام
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# دالة لمعالجة الرسائل الواردة
@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    if event.is_private:
        sender = await event.get_sender()
        sender_name = sender.first_name if sender.first_name else "Unknown"
        sender_id = sender.id
        message_text = event.message.message
        timestamp = datetime.now()

        # حفظ الرسالة في ملف HTML
        file_name = f"Telegram_{sender_id}.html"
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(f"<div style='border:1px solid #ccc; padding:10px; margin:10px;'>\n")
            file.write(f"<p><strong>📩 رسالة جديدة</strong></p>\n")
            file.write(f"<p>👤 <strong>من:</strong> <a href='tg://user?id={sender_id}'>{sender_name}</a> (ID: {sender_id})</p>\n")
            file.write(f"<p>🕒 <strong>التوقيت:</strong> {timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>\n")
            file.write(f"<p>💬 <strong>المحتوى:</strong></p>\n")
            file.write(f"<pre>{message_text}</pre>\n")
            file.write(f"</div>\n")

        # طباعة الرسالة في الكونسول
        print(f"رسالة جديدة من {sender_name} ({sender_id}): {message_text}")

# تشغيل البرنامج
async def main():
    print("تشغيل البوت. بانتظار الرسائل...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
