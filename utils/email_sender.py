from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, HtmlContent


def send_email(to_email, subject, html_content):
    sender_email = settings.SENDGRID_SENDER
    api_key = settings.SENDGRID_API_KEY

    # create a Mail object
    mail = Mail(
        from_email=sender_email,
        to_emails=to_email,
        subject=subject,
        html_content=HtmlContent(html_content),
    )

    try:
        print('here in email sender .........')
        print(sender_email)
        print(api_key)
        # send the email using SendGrid API
        sg = SendGridAPIClient(api_key)
        response = sg.send(mail)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return response
    except Exception as e:
        print(str(e))
