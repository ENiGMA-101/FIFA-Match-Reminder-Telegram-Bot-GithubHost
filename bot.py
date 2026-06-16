from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from telegram import Bot
from icalendar import Calendar
import pytz

from config import BOT_TOKEN, CHAT_ID

bot = Bot(token=BOT_TOKEN)

scheduler = BlockingScheduler(
    timezone="Asia/Dhaka"
)

def send_reminder(match_name, kickoff):

    message = f"""
⚽ FIFA World Cup 2026

🏆 {match_name}

⏰ Kickoff: {kickoff}

🔔 Starts in 30 minutes
"""

    bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )

with open(
    "FIFA_World_Cup_2026.ics",
    "rb"
) as f:

    calendar = Calendar.from_ical(
        f.read()
    )

for event in calendar.walk("VEVENT"):

    summary = str(
        event.get("SUMMARY")
    )

    kickoff = event.decoded(
        "DTSTART"
    )

    reminder_time = (
        kickoff - timedelta(minutes=30)
    )

    if reminder_time > datetime.now():

        scheduler.add_job(
            send_reminder,
            trigger="date",
            run_date=reminder_time,
            args=[
                summary,
                kickoff.strftime(
                    "%d %b %Y %I:%M %p"
                )
            ]
        )

print("FifaReminderBot started...")
scheduler.start()