from django.urls import path
from django.views.decorators.cache import cache_page

from sending_emails.views import ClientsListView, ClientsDetailView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView

app_name = "sending_emails"

urlpatterns = [
    path("", ClientsListView.as_view(), name="clients_list"),
    path("clients/", ClientsListView.as_view(), name="clients_list"),
    path("client/<int:pk>/", ClientsDetailView.as_view(), name="client"),
    path("create/", ClientCreateView.as_view(), name="client_create"),
    path("update/<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),

    path("messages/", MessageListView.as_view(), name="messages_list"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("message/delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),

    path("mailings/", MailingListView.as_view(), name="mailings_list"),
    path("mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing"),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),

    # path("contacts/", catalog_contacts, name="catalog_contacts"),
    # path("category/", CategoryListView.as_view(), name="category_list"),
]