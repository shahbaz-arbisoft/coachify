from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

class User(AbstractUser):
    # WARNING!
    """
    Some officially supported features of Crowdbotics Dashboard depend on the initial
    state of this User model (Such as the creation of superusers using the CLI
    or password reset in the dashboard). Changing, extending, or modifying this model
    may lead to unexpected bugs and or behaviors in the automated flows provided
    by Crowdbotics. Change it at your own risk.


    This model represents the User instance of the system, login system and
    everything that relates with an `User` is represented by this model.
    """

    # First Name and Last Name do not cover name patterns
    # around the globe.
    class Meta:
        verbose_name = 'List of all admin panel user'
        verbose_name_plural = 'List of all admin panel users'

    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)
    contact_number = models.CharField(_("Contact Number"), blank=True, null=True, max_length=255)
    USER_TYPE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('coach', 'Coach'),
        ('coachee', 'Coachee'),

    )
    user_type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES, default='superadmin')

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
