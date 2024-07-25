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
        fields = "__all__"
        # exclude = ('owner',)


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('next_time_mailing',)


# class ManagerMailingForm(StyleFormMixin, forms.ModelForm):
#     class Meta:
#         model = Mailing
#         fields = ('status',)
#
#
class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        # exclude = ('owner',)
