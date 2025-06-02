from collections import Counter
import os
import platform
import argparse
from datetime import datetime
import json
import smtplib
from email.mime.text import MIMEText

def parse_args():
    parser = argparse.ArgumentParser(description="Simple Log Analyzer CLI Tool")
    
    # Add file parameter
    parser.add_argument(
        '-f', '--file',
        type=str,
        required=True,
        help="Path to the log file to analyze"
    )
    
    # Add keywords
    parser.add_argument(
        '-k', '--keywords',
        type=str,
        nargs='+', # Add more than one args
        default=["warn","critical","error","fail"],
        help="List of keywords to search for (space separated)"
    )
    
    # Add argument for adding result into summary.json
    parser.add_argument(
        "--save-summary",
        action='store_true',
        help="save the log analysis summary to summary.json"
    )
    
    # Add Argument for only getting beep when flag is passed
    parser.add_argument(
        '--get-beep',
        action="store_true",
        help="Play a beep sound if any alert keyword is found"
    )
    
    # Adding Argument for fetching email
    parser.add_argument(
        '--get-email',
        action='store_true',
        help='Send log summary via email if critical alerts are found'
    )
    
    return parser.parse_args()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Function to send Email
def send_email(subject, body):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("❌ Email credentials not found in environment variables.")
        return
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("📧 Email sent successfully!")
    except Exception as e:
        print("Failed to send email", e)


args = parse_args()
log_file = args.file

with open(log_file, "r") as f:
    lines = f.readlines() # This loads all lines of the file into memory.
    
keywords = args.keywords
# keywords = ["error", "warn", "fail", "critical", "exception", "invalid"]

counts = Counter()

for line in lines:
    for keyword in keywords:
        if keyword.lower() in line.lower():
            counts[keyword] += 1
            
total = sum(counts.values())
            
log_summary = {
    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    "log_file": log_file,
    "summary": {}
}

print("🔍 Log Summary:")
for keyword in keywords:
    count = counts[keyword]
    if total > 0:
        percent = ((count/total) * 100 ) 
    else:
        percent = 0
    print(percent)
    bar_length = int(percent)
    bar = ("#" * (bar_length // 4))
    print(f"{keyword.capitalize():<10}: {count} | {bar} ({percent:.1f}%)")
    log_summary["summary"][keyword] = {
        "count": count,
        "percentage": f"{percent}% {bar}"
    }
    
# Ensure summary.json exists and is a valid JSON array

if args.save_summary:
    json_filepath = "summary.json"
    if not os.path.exists(json_filepath):
        with open(json_filepath, "w") as f:
            json.dump([], f, indent=4)

    # Load existing data from summary.json, or initialize as empty list if invalid
    with open(json_filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

    # Append Summary into Data
    data.append(log_summary)

    # write into summary.json
    with open("summary.json", "w") as f:
        json.dump(data, f, indent=4)
    
# Adding Beep Message
def beep():
    if platform.system() == 'Windows':
        import winsound
        winsound.Beep(1000, 500)
    else:
        print('\a')
        print('Beep Beep Beep')
        
alert_keywords = ["warn", "fail", "critical","error"]

if args.get_email:
    alert_summary = "\n".join([f"{k.capitalize()}: {counts[k]}" for k in alert_keywords if counts[k] > 0])
    if alert_summary:
        send_email("🚨 Log Alert Report", f"Alert keywords found in log:\n\n{alert_summary}")

if args.get_beep:
    if any(counts[k]>0 for k in alert_keywords):
        print("\n⚠️ ALERT TRIGGERED! ⚠️")
        beep()
        print("One or more critical log entries were found:")
        for k in alert_keywords:
            if counts[k]>0:
                print(f" - {k.capitalize()}: {counts[k]}")
