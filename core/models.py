from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from .blocks import (
    CardsBlock,
    DirectionsBlock,
    HeroBlock,
    LatestNewsBlock,
    NewsSelectionBlock,
    RichTextBlock,
    ValuesBlock,
)


class HomePage(Page):
    max_count = 1

    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("cards", CardsBlock()),
            ("rich_text", RichTextBlock()),
            ("values", ValuesBlock()),
            ("directions", DirectionsBlock()),
            ("news_selection", NewsSelectionBlock()),
            ("latest_news", LatestNewsBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    subpage_types = ["core.OrganizationIndexPage", "news.NewsIndexPage", "contacts.ContactsPage"]

    class Meta:
        verbose_name = "Главная"


class OrganizationIndexPage(Page):
    max_count = 1
    subpage_types = ["core.OrganizationPage", "people.LeadershipPage", "awards.AwardsPage"]

    class Meta:
        verbose_name = "Раздел: Организация"


class OrganizationPage(Page):
    parent_page_types = ["core.OrganizationIndexPage"]
    subpage_types: list[str] = []

    body = StreamField(
        [
            ("rich_text", RichTextBlock()),
            ("values", ValuesBlock()),
            ("directions", DirectionsBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Об организации"
