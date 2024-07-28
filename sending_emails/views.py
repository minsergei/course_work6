from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView, TemplateView,
)
import random
from django.forms import inlineformset_factory
from blog.models import Blog
from sending_emails.forms import ClientForm, MessageForm, MailingForm, ManagerMailingForm, AttemptForm, AdminMailingForm
from sending_emails.models import Clients, Message, Mailing, MailingAttempt


class ClientsListView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечающий за отображение списка клиентов
    """
    model = Clients

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientsDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер отвечающий за отображение клиента
    """
    model = Clients

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер отвечающий за создание клиента
    """
    model = Clients
    form_class = ClientForm
    success_url = reverse_lazy('sending_emails:clients_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер отвечающий за редактирование клиента
    """
    model = Clients
    form_class = ClientForm

    def get_success_url(self):
        return reverse('sending_emails:client', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер отвечающий за удаление клиента
    """
    model = Clients
    success_url = reverse_lazy('sending_emails:clients_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


# ---------------------------------------------------------------------------------------------

class MessageListView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечающий за отображение списка сообщений
    """
    model = Message

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер отвечающий за отображение сообщения
    """
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер отвечающий за создание сообщения
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('sending_emails:messages_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер отвечающий за редактирование сообщение
    """
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('sending_emails:message', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер отвечающий за удаление сообщения
    """
    model = Message
    success_url = reverse_lazy('sending_emails:messages_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


# ----------------------------------------------------------------------------------------------


class MailingListView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечающий за отображение списка рассылок
    """
    model = Mailing

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер отвечающий за отображение рассылки
    """
    model = Mailing

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        VersionFormset = inlineformset_factory(
            Mailing,
            MailingAttempt,
            AttemptForm,
            extra=0,
            can_delete=False,
        )
        context_data["formset"] = VersionFormset(instance=self.object)
        return context_data


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager') and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер отвечающий за создание рассылки
    """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('sending_emails:mailings_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер отвечающий за редактирование рассылки
    """
    model = Mailing
    form_class = MailingForm

    def get_form_kwargs(self):
        user = self.request.user
        if user == self.object.owner:
            kwargs = super().get_form_kwargs()
            kwargs.update({'request': self.request})
            return kwargs
        else:
            kwargs = super().get_form_kwargs()
            return kwargs

    def get_success_url(self):
        return reverse('sending_emails:mailing', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        """
        Функция, определяющая поля для редактирования в зависимости от прав пользователя
        """
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        elif user.is_superuser:
            return AdminMailingForm
        elif user.has_perm('sending_emails.deactivate_mailing'):
            return ManagerMailingForm
        else:
            raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер отвечающий за удаление расылки
    """
    model = Mailing
    success_url = reverse_lazy('sending_emails:mailings_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class HomeView(TemplateView):
    """
    Контроллер главной страницы сайта
    """
    template_name = 'sending_emails/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailings = Mailing.objects.all()
        clients = Clients.objects.all()
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)
        context_data['all_mailings'] = mailings.count()
        context_data['active_mailings'] = mailings.filter(mailing_status='executing').count()
        context_data['active_clients'] = clients.values('email').distinct().count()

        context_data['blog_list'] = blog_list[:3]
        return context_data


class LogListView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечающий за отображение списка попыток рассылок
    """
    model = MailingAttempt
