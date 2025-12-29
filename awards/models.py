from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


@register_snippet
class Award(models.Model):
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Изображение",
    )
    sort_order = models.PositiveIntegerField("Порядок", default=0)

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("image"),
        FieldPanel("sort_order"),
    ]

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "Награда"
        verbose_name_plural = "Награды"

    def __str__(self) -> str:
        return self.title


class AwardsPage(Page):
    parent_page_types = ["core.OrganizationIndexPage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Оценка деятельности"

    def get_context(self, request):
        context = super().get_context(request)
        context["awards"] = Award.objects.all()
        return context
