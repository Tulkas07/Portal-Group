"""Дрібні спільні помічники, щоб не повторювати код у застосунках."""
from django.urls import reverse


class FormPage:
    """Додає заголовок сторінки та спільний шаблон form.html.

    Якщо задано delete_url_name, на сторінці редагування з'являється кнопка «Видалити».
    """

    template_name = "form.html"
    page_title = ""
    delete_url_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.page_title
        obj = getattr(self, "object", None)
        if self.delete_url_name and obj is not None and obj.pk:
            context["delete_url"] = reverse(self.delete_url_name, args=[obj.pk])
        return context


class DeletePage:
    """Спільний шаблон підтвердження видалення."""

    template_name = "confirm_delete.html"


def split_lines(text):
    """Рядки з textarea без порожніх."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def sync_children(manager, lines):
    """Робить так, щоб дочірні записи (варіанти відповіді) відповідали списку `lines`.

    Записи з незміненим текстом лишаються (разом із голосами/відповідями),
    видалені рядки прибираються, нові додаються.
    """
    existing = {obj.text: obj for obj in manager.all()}
    for text, obj in existing.items():
        if text not in lines:
            obj.delete()
    for line in lines:
        if line not in existing:
            manager.create(text=line)
