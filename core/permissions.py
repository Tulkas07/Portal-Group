"""Ролі доступу.

* Адміністратор  - superuser або is_staff (викладач, керівник проекту).
* Модератор      - користувач із групи «Модератори» (група створюється міграцією users.0002).
* Користувач     - будь-який інший зареєстрований акаунт.
"""
from django.contrib.auth.mixins import UserPassesTestMixin

MODERATOR_GROUP = "Модератори"


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


def is_moderator(user):
    return user.is_authenticated and user.groups.filter(name=MODERATOR_GROUP).exists()


def can_manage(user):
    """Адміністратор або модератор."""
    return is_admin(user) or is_moderator(user)


def role_name(user):
    if is_admin(user):
        return "Адміністратор"
    if is_moderator(user):
        return "Модератор"
    return "Користувач"


class ManagerRequiredMixin(UserPassesTestMixin):
    """Доступ для адміністраторів і модераторів."""

    def test_func(self):
        return can_manage(self.request.user)


class AdminRequiredMixin(UserPassesTestMixin):
    """Доступ лише для адміністраторів."""

    def test_func(self):
        return is_admin(self.request.user)
