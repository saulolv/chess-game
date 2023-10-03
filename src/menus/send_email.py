from sendgrid import SendGridAPIClient
import os
from sendgrid.helpers.mail import Mail

import random



def send_email(email_destiny, code):
    api_key = api
    # from_email = 'srs@ic.ufal.br'
    
    body = f"Seu código de verificação é {code}"
    message = Mail(
        from_email=from_email,
        to_emails=email_destiny,
        subject='Recuperação de senha',
        plain_text_content=body,
        html_content=body)
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
    
    return code
