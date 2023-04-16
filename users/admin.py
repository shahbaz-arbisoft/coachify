from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from users.forms import UserChangeForm, UserCreationForm

User = get_user_model()
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter


class UserTypeListFilter(SimpleListFilter):
    title = _("user role")
    parameter_name = "user_type"

    def lookups(self, request, model_admin):
        return (
            ("admin", _("Admin")),
            ("superadmin", _("Super Admin")),
        )

    def queryset(self, request, queryset):
        if self.value() == "admin":
            return queryset.filter(user_type="admin")
        elif self.value() == "superadmin":
            return queryset.filter(user_type="superadmin")


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_filter = [UserTypeListFilter]
    ordering = ["-is_superuser", "user_type"]
    filter_horizontal = []
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "contact_number",
        "is_superuser",
        "user_type",
    ]
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "contact_number",
        "is_superuser",
        "user_type",
    ]


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(user_type__in=["admin", "superadmin"])

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = "Search Admin Panel Users"
        return super().changelist_view(request, extra_context=extra_context)
