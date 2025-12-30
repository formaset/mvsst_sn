from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock


class HeadingBlock(blocks.StructBlock):
    text = blocks.CharBlock(label="Текст заголовка")

    class Meta:
        template = "blocks/heading.html"
        icon = "title"
        label = "Заголовок"


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(label="Изображение")
    caption = blocks.CharBlock(label="Подпись", required=False)

    class Meta:
        template = "blocks/image.html"
        icon = "image"
        label = "Изображение"


class VideoBlock(blocks.StructBlock):
    file = DocumentChooserBlock(label="Файл видео")
    caption = blocks.CharBlock(label="Подпись", required=False)

    class Meta:
        template = "blocks/video.html"
        icon = "media"
        label = "Видео"


class QuoteBlock(blocks.StructBlock):
    text = blocks.TextBlock(label="Цитата")
    author = blocks.CharBlock(label="Автор", required=False)

    class Meta:
        template = "blocks/quote.html"
        icon = "openquote"
        label = "Цитата"


class CalloutBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок", required=False)
    text = blocks.TextBlock(label="Текст")

    class Meta:
        template = "blocks/callout.html"
        icon = "warning"
        label = "Выделение"


class DividerBlock(blocks.StructBlock):
    class Meta:
        template = "blocks/divider.html"
        icon = "horizontalrule"
        label = "Разделитель"


class KeyFigureBlock(blocks.StructBlock):
    value = blocks.CharBlock(label="Число")
    label = blocks.CharBlock(label="Подпись")

    class Meta:
        template = "blocks/key_figure.html"
        icon = "pick"
        label = "Ключевая цифра"


class GalleryBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(ImageChooserBlock(label="Изображение"), **kwargs)

    class Meta:
        template = "blocks/gallery.html"
        icon = "image"
        label = "Галерея"
