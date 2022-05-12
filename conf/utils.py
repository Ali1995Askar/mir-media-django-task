import threading
from django.conf import settings

from django.urls import reverse
from django.utils.html import format_html
from django.template.loader import get_template
from django.core.mail import EmailMessage


def relational_fields(field_name):
    def _nested_fields(obj):
        relational_obj = getattr(obj, field_name)
        if relational_obj is None:
            return 'None'

        app_name = relational_obj._meta.app_label
        model_name = relational_obj._meta.model_name
        view_name = f'admin:{app_name}_{model_name}_change'
        link_url = reverse(view_name, args=[relational_obj.pk])
        return format_html(f'<a href="{link_url}">{relational_obj}</a>')

    _nested_fields.short_description = field_name

    return _nested_fields


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send()


def send_email(payload):
    email_content = get_template('email_templates/contact_email_template.html').render(payload['data'])
    email = EmailMessage(subject='New Message',
                         body=email_content,
                         from_email=settings.EMAIL_HOST_USER,
                         to=[settings.EMAIL_TO],
                         reply_to=[payload['data']['email']])
    email.content_subtype = 'html'
    thread = EmailThread(email=email)
    thread.start()
    return thread
