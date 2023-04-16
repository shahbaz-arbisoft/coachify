from django.contrib import admin
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Client
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.contrib import messages
from django.template.loader import render_to_string
from utils.email_sender import send_email
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # specify the fields to be displayed in the add form
    add_fields = ("client_name", "email", "industry")
    list_display = ["client_name", "industry", "email_link", "city", "user_type"]
    search_fields = ["client_name", "industry", "email", "city"]
    # list_display_links = ('email',)
    list_display_links = None

    def client_name(self, obj):
        return obj.client_name

    client_name.admin_order_field = "client_name"

    @transaction.atomic()
    def save_model(self, request, obj, form, change):
        # Create a new User with user_type='Client'
        password = User.objects.make_random_password()
        user = User.objects.create_user(
            username=obj.email,
            email=obj.email,
            password=password,
            user_type="Client",
        )

        #TODO update client login url for email link
        current_site = Site.objects.get_current()
        login_url = f"{'https'}://{current_site.domain}"

        subject = "[Sloan Leaders] Client Account Created"
        username = user.username
        # password = user.password
        context = {
            "username": username,
            "password": password,
            "login_url": login_url
        }
        html_content = render_to_string("admin/clients/client/email.html", context)
        response = send_email(user.email, subject, html_content)

        if not response:
            # rollback the transaction and show error message
            transaction.set_rollback(True)
            # show error message
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Error: Email could not be sent. Client not created.')
        else:
            # Assign the user_type of the Client and save the object
            obj.user = user
            obj.save()
            # Show success message
            # messages.set_level(request, messages.SUCCESS)
            # self.message_user(request, "Client successfully created.", level=messages.SUCCESS)


    # override the add_view method
    def add_view(self, request, form_url="", extra_context=None):
        # display only the fields specified in add_fields
        self.fields = self.add_fields
        extra_context = extra_context or {}
        app_label, model_name = self.model._meta.app_label, self.model._meta.model_name
        extra_context["title"] = "Add {model_name}".format(
            model_name=model_name.capitalize()
        )
        return super().add_view(request, form_url, extra_context)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(id=search_term_as_int)
        except ValueError:
            pass
        return queryset, use_distinct

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = "Search Clients"
        # extra_context['add_button_label'] = self.add_button_label
        return super().changelist_view(request, extra_context=extra_context)

    list_display_links = ("client_name",)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = "Client detail"
        # extra_context['breadcrumb'] = 'Home › Clients › Viewing client details'
        return super().change_view(request, object_id, form_url, extra_context)

    def email_link(self, obj):
        url = reverse("admin:clients_client_change", args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.email)

    # email_link.allow_tags = True
    email_link.short_description = "Email"