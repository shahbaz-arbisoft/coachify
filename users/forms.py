from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms as django_forms

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):
    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    first_name = django_forms.CharField(max_length=30, required=True)
    last_name = django_forms.CharField(max_length=30, required=True)
    email = django_forms.EmailField(required=True)
    contact_number = django_forms.CharField(max_length=30, required=True)

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'contact_number']

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])
