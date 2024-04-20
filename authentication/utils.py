from django.core.mail import EmailMessage
import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
class Util:
    
    @staticmethod
    def send_email(data):
        
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], from_email="support@agritech.com", to=[data['to_email']])
        
        email.send()

    @staticmethod
    def validate_phone_number(value):
        pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not pattern.match(value):
            raise ValidationError('Invalid phone number')
        
    @staticmethod
    def validate_email(value):
        validator = EmailValidator()
        try:
            validator(value)
        except ValidationError:
            return False
        return True