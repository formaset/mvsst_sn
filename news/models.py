from django.core.paginator import Paginator
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.images import get_image_model_string

from .blocks import (
    CalloutBlock,
    DividerBlock,
    GalleryBlock,
    HeadingBlock,
    ImageBlock,
    KeyFigureBlock,
    QuoteBlock,
    VideoBlock,
)
from core.blocks import RichTextBlock


class NewsIndexPage(Page):
    subpage_types = ["news.NewsPage"]
    parent_page_types = ["core.HomePage"]

    paginate_by = models.PositiveIntegerField("Новостей на странице", default=6)

    content_panels = Page.content_panels + [
        FieldPanel("paginate_by"),
    ]

    class Meta:
        verbose_name = "Новости"

    def get_context(self, request):
        context = super().get_context(request)
        news_items = NewsPage.objects.child_of(self).live().order_by("-date")
        paginator = Paginator(news_items, self.paginate_by)
        page_number = request.GET.get("page")
        context["news_page"] = paginator.get_page(page_number)
        return context


class NewsPage(Page):
    parent_page_types = ["news.NewsIndexPage"]
    subpage_types: list[str] = []

    date = models.DateField("Дата публикации")
    lead = models.TextField("Краткий лид", max_length=300, blank=True)
    cover_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Обложка",
    )

    body = StreamField(
        [
            ("heading", HeadingBlock()),
            ("paragraph", RichTextBlock()),
            ("image", ImageBlock()),
            ("video", VideoBlock()),
            ("quote", QuoteBlock()),
            ("callout", CalloutBlock()),
            ("divider", DividerBlock()),
            ("key_figure", KeyFigureBlock()),
            ("gallery", GalleryBlock()),
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Контент новости",
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("lead"),
        FieldPanel("cover_image"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Новость"
