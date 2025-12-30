from wagtail import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from news.models import NewsPage


@hooks.register("insert_global_admin_css")
def add_admin_css():
    return '<link rel="stylesheet" href="/static/css/admin.css">'


@hooks.register("construct_main_menu")
def customize_main_menu(request, menu_items):
    for item in menu_items:
        if item.name == "explorer":
            item.label = "Страницы"
        if item.name == "images":
            item.label = "Медиа"
        if item.name == "documents":
            item.label = "Файлы"


class NewsAdmin(ModelAdmin):
    model = NewsPage
    menu_label = "Новости"
    menu_icon = "doc-full"
    add_to_settings_menu = False
    list_display = ("title", "first_published_at")
    search_fields = ("title",)


modeladmin_register(NewsAdmin)
