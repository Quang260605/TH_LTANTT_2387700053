import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_email(receiver_email, subject, body, smtp_user, smtp_pass):
    if not smtp_user or not smtp_pass:
        print("[-] Email failed: SMTP_USER or SMTP_PASS not set in .env")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = receiver_email
    msg.set_content(body)

    smtp_pass_clean = smtp_pass.replace(" ", "")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(smtp_user, smtp_pass_clean)
            smtp.send_message(msg)
        print(f"[+] Email sent to {receiver_email}")
    except Exception as e1:
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(smtp_user, smtp_pass_clean)
                smtp.send_message(msg)
            print(f"[+] Email sent to {receiver_email}")
        except Exception as e2:
            print(f"[-] Email failed: {e1} / {e2}")
