import smtplib, ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from decouple import config

# mail server configuration
SERVER = 'smtp.gmail.com'
PORT = 465 # For SSL
SENDER_MAIL = config('sender_email')
SENDER_PASSWD = config('password')
RECEIVER_MAIL = config('receiver_mail')

context = ssl.create_default_context()

with open('email.html', 'r') as htmlContent:
    pass

# mail body, subject, recepient and attachment
mailSubject = 'Reset Your Account Password'
mailContentHtml = 'We’ve received a request to reset the password for the Tutorspedia account associated with hello@SmilesDavis.yeah. No changes have been made to your account yet.<br> You can reset your password by clicking the link below:<br><a style="border: 0; margin: 0; padding: 0; color: #556cd6 !important; text-decoration: none;" href="https://gogole.com">reset password</a><br>If you did not request a new password, please let us know immediately by replying to this email.<br>You can find answers to most questions and get in touch with us at <a style="border: 0; margin: 0; padding: 0; color: #556cd6 !important; text-decoration: none;" href="https://support.stripe.com">support.tutorspedia.com</a>. We’re here to help you at any step along the way.<br><br> — The Tutorspedia team'
recepientMailList = RECEIVER_MAIL
attachmentFilePath = 'bot.png'

def sendMail(SERVER, PORT, SENDER_MAIL, SENDER_PASSWD, mailSubject, mailContentHtml, recepientMailList,attachmentFilePath):
    msg = MIMEMultipart()
    
    msg['Subject'] = mailSubject
    msg['From'] = 'Tutorspedia'
    msg['To'] = recepientMailList
    
    msg.attach(MIMEText(mailContentHtml, 'html'))
    
    # file attachment
    try:
        with open(attachmentFilePath, "rb") as attachment:
            # add file as application/octet-stream
            # email client can usually download this automatically as an attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            
        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)
        
        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename = {attachmentFilePath}",
        )
        
        # Add attachment to message and convert message to string
        msg.attach(part)
    except FileNotFoundError:
        print("File not Found!")
        
    with smtplib.SMTP_SSL(SERVER, PORT, context=context) as server:
        
        try:
            #server.starttls()
            server.login(SENDER_MAIL, SENDER_PASSWD)
            message = msg.as_string()
            server.sendmail(SENDER_MAIL, recepientMailList, message)
            server.quit()
            print('Successfully sent email')
            
        except Exception:
            print('An Error occured while sending mail!')
            
        
        
sendMail(SERVER, PORT, SENDER_MAIL, SENDER_PASSWD, mailSubject, mailContentHtml, recepientMailList,attachmentFilePath)
        
        
    

