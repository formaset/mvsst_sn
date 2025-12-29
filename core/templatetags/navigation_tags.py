from django import template
from wagtail.models import Site

from core.models import OrganizationIndexPage
from news.models import NewsIndexPage, NewsPage
from contacts.models import ContactsPage

register = template.Library()


@register.inclusion_tag("includes/navigation.html", takes_context=True)
def main_navigation(context):
    request = context["request"]
    site = Site.find_for_request(request)
    root = site.root_page if site else None

    organization = None
    organization_children = []
    if root:
        organization = OrganizationIndexPage.objects.child_of(root).first()
        if organization:
            organization_children = organization.get_children().live()

    news = NewsIndexPage.objects.child_of(root).first() if root else None
    contacts = ContactsPage.objects.child_of(root).first() if root else None

    return {
        "organization": organization,
        "organization_children": organization_children,
        "news": news,
        "contacts": contacts,
    }


@register.simple_tag
def latest_news(limit=3):
    return NewsPage.objects.live().order_by("-date")[:limit]
