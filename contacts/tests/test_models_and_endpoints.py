from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.template.loader import get_template
from django.conf import settings
from unittest.mock import patch, Mock
from ..models import Contact
from conf.utils import send_email

CONTACT_FORM_URL = reverse('contacts:send-email')


class TestContactApp(TestCase):
    def setUp(self) -> None:
        self.email = "test@test.com"
        self.name = "test"
        self.content = "Hello Every one this new message from django app"
        self.email_payload = {
            'data': {
                'email': self.email,
                'name': self.name,
                'content': self.content
            }
        }

    def test_create_contact_object_with_correct_values(self):
        contact_object = Contact.objects.create(
            email=self.email,
            name=self.name,
            content=self.content
        )

        self.assertEqual(Contact.objects.all().count(), 1)
        self.assertEqual(contact_object.email, contact_object.email)
        self.assertEqual(contact_object.name, contact_object.name)
        self.assertEqual(contact_object.content, contact_object.content)

    def test_send_email_with_correct_data(self):
        send_email(self.email_payload).join()

        email_content = get_template('email_templates/contact_email_template.html').render(
            self.email_payload.get('data'))
        email = mail.outbox[0]

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(email.subject, 'New Message')
        self.assertEqual(email.from_email, settings.EMAIL_HOST_USER)
        self.assertEqual(email.to, [settings.EMAIL_TO])
        self.assertHTMLEqual(email.body, email_content)

    @patch('contacts.views.send_email')
    def test_post_request_to_contactus_url_with_correct_email_data(self, mocked_send_email: Mock):
        response = self.client.post(CONTACT_FORM_URL, self.email_payload.get('data'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.all().count(), 1)

        contact_obj = Contact.objects.all().first()

        self.assertEqual(contact_obj.email, self.email)
        self.assertEqual(contact_obj.name, self.name)
        self.assertEqual(contact_obj.content, self.content)

        mocked_send_email.assert_called_once_with(self.email_payload)

