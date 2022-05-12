from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            "email",
            "name",
            "content",
        )
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email", },
            ),
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Full Name"},
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Message"},
            ),
        }

        labels = {
            'email': 'Email',
            'name': 'Full Name',
            'content': 'Message',
        }
