

from fastapi_mail import FastMail, MessageSchema, MessageType
from jinja2 import FileSystemLoader, Environment
from pydantic import NameEmail


from app.config import MAIL_CONFIGURATION, RESEND_TEMPLATE_PATH


class EmailInfrastructure:
    def __init__(self):
        self.__fm = FastMail(MAIL_CONFIGURATION)
        self.template_env = Environment(loader=FileSystemLoader(RESEND_TEMPLATE_PATH))


    async def send_email_verification_code(self, recipient: NameEmail | str,
                                           verification_code: int,
                                           subject="Verification Code", ) -> None:
        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            template_body={"activation_code": verification_code},
            subtype=MessageType.html, )

        await self.__fm.send_message(message, template_name="code-verification.html")

    async def send_message_via_clicking(self, recipient: NameEmail | str, activation_link: str,
                                        subject="Account Verification",
                                        email_template="link-verification.html", error_response=None):
        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            template_body={"activation_link": activation_link, "username": recipient},
            subtype=MessageType.html,
        )
        await self.__fm.send_message(message, template_name=email_template)

