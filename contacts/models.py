from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page


class ContactsPage(Page):
    parent_page_types = ["core.HomePage"]
    subpage_types: list[str] = []

    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    legal_address = models.CharField("Юридический адрес", max_length=255, blank=True)
    actual_address = models.CharField("Фактический адрес", max_length=255, blank=True)
    schedule = models.CharField(
        "График работы",
        max_length=255,
        default="ПН–ЧТ 08:00–17:00, ПТ 08:00–16:00, перерыв 12:00–13:00",
    )
    full_name = models.CharField("Полное наименование", max_length=255, blank=True)
    short_name = models.CharField("Сокращённое наименование", max_length=255, blank=True)
    yandex_map_embed = models.TextField(
        "Yandex Maps embed URL / iframe code",
        blank=True,
        help_text="Вставьте URL или iframe-код с yandex.ru / yandex.com.",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("phone"),
                FieldPanel("email"),
                FieldPanel("legal_address"),
                FieldPanel("actual_address"),
                FieldPanel("schedule"),
                FieldPanel("full_name"),
                FieldPanel("short_name"),
            ],
            heading="Контактная информация",
        ),
        FieldPanel("yandex_map_embed"),
    ]

    class Meta:
        verbose_name = "Контакты"

    def clean(self):
        super().clean()
        if not self.yandex_map_embed:
            return
        value = self.yandex_map_embed.strip()
        url = value
        if "<iframe" in value:
            start = value.find("src=")
            if start == -1:
                raise ValidationError({"yandex_map_embed": "Iframe должен содержать src."})
            quote = '"' if '"' in value[start:] else "'"
            url = value.split("src=")[1].split(quote)[1]
        parsed = urlparse(url)
        if not parsed.netloc.endswith(("yandex.ru", "yandex.com")):
            raise ValidationError({"yandex_map_embed": "Допустимы только домены yandex.ru или yandex.com."})

    def map_embed_url(self):
        if not self.yandex_map_embed:
            return ""
        value = self.yandex_map_embed.strip()
        if "<iframe" in value:
            start = value.find("src=")
            quote = '"' if '"' in value[start:] else "'"
            return value.split("src=")[1].split(quote)[1]
        return value
