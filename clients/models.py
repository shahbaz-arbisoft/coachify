from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete
from users.models import User
from django.dispatch import receiver


class Client(models.Model):
    class Meta:
        verbose_name = "List of all client"
        # verbose_name_plural = 'List of all clients'

    profile_picture = models.ImageField(
        upload_to="client_profile_pictures/", blank=True, null=True
    )
    client_name = models.CharField(max_length=100, blank=False, null=False)
    industry = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=100, blank=True, null=True)
    company_employees = models.PositiveIntegerField(null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=False, blank=False, related_name="client"
    )

    @property
    def user_type(self):
        return self.user.user_type if self.user else None

    def __str__(self):
        return self.client_name


@receiver(post_delete, sender=Client)
def delete_related_user(sender, instance, **kwargs):
    """
    A signal receiver which deletes the corresponding User object when a Client object is deleted.
    """
    instance.user.delete()
