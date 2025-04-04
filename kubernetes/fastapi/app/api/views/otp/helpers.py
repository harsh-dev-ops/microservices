from typing import Annotated, List
from fastapi_mail import FastMail, MessageSchema, MessageType
from typing_extensions import Doc

from twilio.rest import Client

from app.conf.settings import settings
from app.conf.mail import mail_conf
from app.api.email.schema import EmailSchema
from app.api.utils.strings import StringUtils

class Otp:
    def __init__(self, ):
        pass
    
    def create(self):
        return StringUtils.random_string(length=6, digits=True, chars=False)
        
    async def send_sms(self, body:str, to:str):
        twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = twilio_client.messages.create(
                        to=to,
                        from_=settings.TWILIO_PHONE_NUMBER,
                        body=body
                    )
        return message.sid
    
    async def send_email(self, data: EmailSchema):
        try:
            message = MessageSchema(
                subject=data.subject,
                recipients=data.email,
                template_body=data.body,
                subtype=MessageType.html,
                )

            fm = FastMail(mail_conf)
            await fm.send_message(message, template_name="otp.html")
            
        except Exception as e:
            print(f"{e}")
    