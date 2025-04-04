import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.script import Translation
from pyrogram import enums
import math

# متغير لتخزين آخر وقت تحديث (خارج الدالة للحفاظ على القيمة بين الاستدعاءات)
last_update_time_global = 0  # تهيئة افتراضية

async def progress_for_pyrogram(current, total, ud_type, message, start, bar_width=20, status=""):
    global last_update_time_global  # الوصول إلى المتغير العام

    now = time.time()
    diff = now - start
    percentage = current * 100 / total
    speed = current / diff
    elapsed_time = round(diff) * 1000
    time_to_completion = round((total - current) / speed) * 1000
    estimated_total_time = elapsed_time + time_to_completion

    elapsed_time = TimeFormatter(milliseconds=elapsed_time)
    estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

    progress = "[{0}{1}] \n".format(
        ''.join(["█" for _ in range(math.floor(percentage / (100 / bar_width)))]),
        ''.join(["░" for _ in range(bar_width - math.floor(percentage / (100 / bar_width)))])
    )

    tmp = progress + Translation.PROGRESS.format(
        round(percentage, 2),
        humanbytes(current),
        humanbytes(total),
        humanbytes(speed),
        estimated_total_time if estimated_total_time != '' else "0 s"
    )

    status_message = f"**{ud_type}**\n\n{status}\n\n{tmp}"

    # إضافة شرط التأخير الزمني
    if (now - last_update_time_global) >= 3 or current == total: # 3 ثواني تأخير (يمكن تغييرها إلى 4)
        try:
            await message.edit(
                text=status_message,
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('⛔️ Cancel', callback_data='close')
                        ]
                    ]
                )
            )
            last_update_time_global = now  # تحديث آخر وقت تحديث
        except Exception as e:
            print(f"Error updating progress: {e}")
    else:
        # لا تقم بالتحديث إذا لم يمر 3 ثواني
        pass


def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
          ((str(hours) + "h, ") if hours else "") + \
          ((str(minutes) + "m, ") if minutes else "") + \
          ((str(seconds) + "s, ") if seconds else "") + \
          ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]
