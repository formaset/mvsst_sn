from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock


class HeroBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок", required=True)
    text = blocks.TextBlock(label="Текст", required=False)
    image = ImageChooserBlock(label="Изображение", required=False)
    button_text = blocks.CharBlock(label="Текст кнопки", required=False)
    button_link = blocks.PageChooserBlock(label="Ссылка", required=False)

    class Meta:
        template = "blocks/hero.html"
        icon = "image"
        label = "Hero-блок"


class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок")
    text = blocks.TextBlock(label="Описание", required=False)
    image = ImageChooserBlock(label="Изображение", required=False)
    link = blocks.PageChooserBlock(label="Ссылка", required=False)

    class Meta:
        template = "blocks/card.html"
        icon = "placeholder"
        label = "Карточка"


class CardsBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(CardBlock(), **kwargs)

    class Meta:
        template = "blocks/cards.html"
        icon = "list-ul"
        label = "Карточки"


class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        template = "blocks/rich_text.html"
        icon = "doc-full"
        label = "Текст"


class ValueItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Название")
    text = blocks.TextBlock(label="Описание")

    class Meta:
        template = "blocks/value_item.html"
        icon = "form"
        label = "Ценность"


class ValuesBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(ValueItemBlock(), **kwargs)

    class Meta:
        template = "blocks/values.html"
        icon = "list-ul"
        label = "Ценности"


class DirectionsBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(blocks.CharBlock(label="Направление"), **kwargs)

    class Meta:
        template = "blocks/directions.html"
        icon = "list-ul"
        label = "Направления деятельности"


class NewsSelectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок", required=False)
    items = blocks.ListBlock(
        blocks.PageChooserBlock(label="Новость", page_type=["news.NewsPage"]),
        label="Выбранные новости",
    )

    class Meta:
        template = "blocks/news_selection.html"
        icon = "doc-full-inverse"
        label = "Выбранные новости"


class LatestNewsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок", required=False, default="Последние новости")

    class Meta:
        template = "blocks/latest_news.html"
        icon = "time"
        label = "Последние новости (авто)"


class MediaBlock(blocks.StructBlock):
    file = DocumentChooserBlock(label="Файл видео")
    caption = blocks.CharBlock(label="Подпись", required=False)

    class Meta:
        template = "blocks/video.html"
        icon = "media"
        label = "Видео (файл)"
