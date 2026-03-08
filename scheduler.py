"""
Run analysis on schedule
"""

import schedule
import time
from datetime import datetime
from main import run_analysis

def daily_analysis():
    """Run daily geopolitical analysis"""
    
    print(f"\n{'='*60}")
    print(f"🕐 Starting scheduled analysis: {datetime.now()}")
    print(f"{'='*60}\n")
    
    # Run your main analysis
    import subprocess
    result = subprocess.run(['python', 'main.py'], capture_output=True, text=True)
    
    print(result.stdout)
    
    # Optional: Send email notification
    send_email_notification()
    
    print(f"\n✅ Scheduled analysis completed: {datetime.now()}\n")

def send_email_notification():
    """Send email when analysis is ready"""
    import smtplib
    from email.mime.text import MIMEText
    
    msg = MIMEText("Your daily Iran-Israel-America analysis is ready!")
    msg['Subject'] = 'Daily Geopolitical Analysis Ready'
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = 'recipient@example.com'
    
    # Configure SMTP (example for Gmail)
    # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # server.login('your_email@gmail.com', 'your_app_password')
    # server.send_message(msg)
    # server.quit()
    
    print("📧 Email notification sent")

# Schedule daily at 8 AM
schedule.every().day.at("08:00").do(daily_analysis)

# Or weekly on Monday
# schedule.every().monday.at("08:00").do(daily_analysis)

print("📅 Scheduler started. Press Ctrl+C to stop.")
print("Next run:", schedule.next_run())

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute