from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


@register_snippet
class LeadershipMember(models.Model):
    name = models.CharField("ФИО", max_length=255)
    position = models.CharField("Должность", max_length=255)
    photo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Фото",
    )
    sort_order = models.PositiveIntegerField("Порядок", default=0)

    panels = [
        FieldPanel("name"),
        FieldPanel("position"),
        FieldPanel("photo"),
        FieldPanel("sort_order"),
    ]

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Руководитель"
        verbose_name_plural = "Руководство"

    def __str__(self) -> str:
        return self.name


class LeadershipPage(Page):
    parent_page_types = ["core.OrganizationIndexPage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Руководство"

    def get_context(self, request):
        context = super().get_context(request)
        context["leaders"] = LeadershipMember.objects.all()
        return context
