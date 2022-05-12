from django.views.generic.edit import FormView
from django.contrib import messages
from conf.utils import send_email
from . import forms


# Create your views here.

class ContactCreateView(FormView):
    form_class = forms.ContactForm

    template_name = "basics/contact_us.html"
    success_url = '/contact-us/'

    def get_success_url(self):
        messages.success(self.request, 'Message sent successfully !')
        return super().get_success_url()

    def form_valid(self, form):
        form.save()

        send_email({
            'data': {
                'email': form.data.get('email'),
                'name': form.data.get('name'),
                'content': form.data.get('content')
            }
        })
        return super().form_valid(form)
