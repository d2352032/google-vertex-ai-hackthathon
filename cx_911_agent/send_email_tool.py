# import smtplib
import smtplib
from email.message import EmailMessage

def send_email(to: str, subject: str, body: str):

#     """
#     Sends an email using Mailtrap SMTP.

#     Args:
#         to (str): recipient email address
#         subject (str): email subject
#         body (str): email body text

#     Returns:
#         dict: status and message
#     """


    msg = EmailMessage()
    msg["From"] = "cx-911-agent@onetrust.com"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        # https://mailtrap.io/inboxes/2427512/messages       
        with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
            server.starttls()
            server.login("1a1cc256d310a0", "cf848ad37314b9")
            server.send_message(msg)

        return {
            "status": "success",
            "message": f"Email sent to {to}"
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# # if __name__ == "__main__":
# result = send_email(
#     to="test@example.com",
#     subject="Mailtrap CLI Test2",
#     body="Hello! This email was sent using the Python command."
# )
# print(result)