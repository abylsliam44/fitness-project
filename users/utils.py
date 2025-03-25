from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_welcome_email(user):
    print(f"Trying to send the email to {user.email}")

    subject = "Welcome to Fitness Platform!"

    html_message = render_to_string('users/welcome_email.html', {
    'user': user,
    'support_email': settings.DEFAULT_FROM_EMAIL
})
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject,
            plain_message, 
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,  
            fail_silently=False
        )
        print("The email was sent successfully!")
    except Exception as e:
        print(f"Error while trying to sent the email( {e}")
