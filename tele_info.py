import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
import pytz

# الإعدادات للسجلات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# الحصول على التوكن من متغير البيئة
TOKEN = os.getenv('TOKEN')

# استعلام عن معلومات المستخدم
def get_info(update: Update, context: CallbackContext) -> None:
    try:
        user_id = int(context.args[0])
        user = context.bot.get_chat(user_id)

        # طباعة كافة معلومات المستخدم للمساعدة في التحقق
        logger.debug(f"معلومات المستخدم: {user}")

        # استجابة تحتوي على الاسم والمعرف واسم المستخدم
        response = (
            f"اسم العرض: {user.first_name}\n"
            f"اسم المستخدم: @{user.username if user.username else 'لا يوجد'}\n"
            f"المعرف: {user.id}\n"
        )

        # الحصول على النبذة التعريفية (Bio) إن كانت متاحة
        if hasattr(user, 'bio') and user.bio:
            response += f"النبذة التعريفية: {user.bio}\n"
        else:
            response += "النبذة التعريفية: لا توجد\n"

        # الحصول على الصور الشخصية للمستخدم
        photos = context.bot.get_user_profile_photos(user_id)
        if photos.total_count > 0:
            # إرسال عدد الصور الشخصية
            response += f"عدد الصور الشخصية: {photos.total_count}\n"
            
            # إرسال الصورة الشخصية الأحدث
            photo_file_id = photos.photos[0][-1].file_id
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_file_id)
        else:
            response += "لا توجد صور شخصية للمستخدم.\n"
            logger.debug("لا توجد صور شخصية للمستخدم.")

        # إرسال الرد النهائي
        update.message.reply_text(response)
    except ValueError:
        update.message.reply_text("يرجى إدخال رقم معرف صالح.")
    except Exception as e:
        logger.error(f"خطأ أثناء استعلام المعلومات: {e}")
        update.message.reply_text("حدث خطأ أثناء استعلام المعلومات. يرجى المحاولة لاحقاً.")

if __name__ == '__main__':
    # إعداد Updater والبوت
    updater = Updater(TOKEN, use_context=True)

    # الحصول على Dispatcher لإضافة المعالجات
    dp = updater.dispatcher

    # إضافة معالج لأمر /info لاستعلام المعلومات
    dp.add_handler(CommandHandler("info", get_info))

    # بدء البوت
    updater.start_polling()
    updater.idle()
