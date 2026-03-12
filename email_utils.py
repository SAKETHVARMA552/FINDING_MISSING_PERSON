import smtplib
from email.mime.text import MIMEText


# Gmail credentials
SENDER_EMAIL = "mangarajujahnavi@gmail.com"
SENDER_PASSWORD = "fdcglxqeeltvuors"   # Gmail App Password


def send_email(receiver_email, subject, message):
    """
    Send email using Gmail SMTP
    """

    try:
        # Create email
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email

        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)

        # Start secure connection
        server.starttls()

        # Login
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send email
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())

        # Close connection
        server.quit()

        print("✅ Email sent successfully")

        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Check email or app password.")
        return False

    except smtplib.SMTPConnectError:
        print("❌ Unable to connect to Gmail SMTP server.")
        return False

    except Exception as e:
        print("❌ Email error:", e)
        return False