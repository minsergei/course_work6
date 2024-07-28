from django import forms
from .models import Clients, Mailing, Message
from django.forms import BooleanField


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Clients
        exclude = ('owner',)


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('owner', 'is_active', 'next_time_mailing',)

    def __init__(self, *args, **kwargs):
        """Выводим только созданные пользователем клиентов и сообщения"""
        self.request = kwargs.pop("request")
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields["clients"].queryset = Clients.objects.filter(owner=user)
        self.fields["message"].queryset = Message.objects.filter(owner=user)


class ManagerMailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('is_active',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)
