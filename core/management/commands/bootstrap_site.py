import base64
from datetime import date

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from wagtail.images import get_image_model
from wagtail.models import Page, Site
from wagtail.models import GroupPagePermission

from awards.models import Award, AwardsPage
from contacts.models import ContactsPage
from core.models import HomePage, OrganizationIndexPage, OrganizationPage
from news.models import NewsIndexPage, NewsPage
from people.models import LeadershipMember, LeadershipPage


PLACEHOLDER_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABHUlEQVR4nO3XMQrCUBAF0a8Q"
    "8F4o0d6QrqBRB2ls4Q9gJq0S4g1E5Ni7nV8czOac4X2y7t8BAAAAAAAAAAB4mPM5dV7+H3uE"
    "w+W90C0Q0Xg7rAj6F2Q3wV0K+w3wV0K+w3wV0K+w3wV0K+w3wV0K+w3wV0K+w3wV0K+w3wV0K"
    "+w3wV0K+w3wV0K+w3wV0K+w3wV0K+w3wV0K+w3wV0K+w3wV0K+w3wV0K+w3wV0K+w3wV0K+w3"
    "wV0K+w3wV0K+0/6Ue0b4lqfdPp0AAAAAAAAAAB8RrI6IuKxq4wAAAAASUVORK5CYII="
)


class Command(BaseCommand):
    help = "Создать стартовые страницы и примеры контента"

    def handle(self, *args, **options):
        root = Page.get_first_root_node()
        home = HomePage.objects.child_of(root).first()

        if not home:
            home = HomePage(title="Главная", slug="home")
            root.add_child(instance=home)
            home.save_revision().publish()
            Site.objects.update_or_create(
                hostname="localhost",
                defaults={"root_page": home, "site_name": "МосводостокСтройТрест"},
            )

        organization_index = OrganizationIndexPage.objects.child_of(home).first()
        if not organization_index:
            organization_index = OrganizationIndexPage(title="Организация", slug="organization")
            home.add_child(instance=organization_index)
            organization_index.save_revision().publish()

        organization_page = OrganizationPage.objects.child_of(organization_index).first()
        if not organization_page:
            organization_page = OrganizationPage(
                title="Об организации",
                slug="about",
                body=[
                    ("rich_text", "АНО по развитию городской среды «МосводостокСтройТрест» основана 1 октября 2024 года. Учредитель — ГУП «Мосводосток»."),
                    ("rich_text", "Деятельность: благоустройство улиц, сезонная инфраструктура, капитальный ремонт МКД и объектов образования, строительство производственных баз, специальные задачи учредителя. В организации работает около 4000 специалистов."),
                    ("rich_text", "Миссия: Создавать комфортную и безопасную городскую среду, объединяя традиции столичного строительства с современными технологиями благоустройства для миллионов жителей Москвы."),
                    ("values", [
                        {"title": "Качество", "text": "Строим на совесть и отвечаем за результат своим именем."},
                        {"title": "Сроки", "text": "Ценим ритм мегаполиса и работаем без срывов графика."},
                        {"title": "Безопасность", "text": "Жизнь людей — безусловный приоритет."},
                        {"title": "Команда", "text": "Мы — единый механизм, основанный на взаимном уважении."},
                    ]),
                    ("directions", [
                        "Благоустройство улиц и городских пространств",
                        "Капитальный ремонт жилых домов",
                        "Объекты образования и социальная инфраструктура",
                        "Строительство производственных баз",
                    ]),
                ],
            )
            organization_index.add_child(instance=organization_page)
            organization_page.save_revision().publish()
        if not home.body:
            home.body = [
                (
                    "hero",
                    {
                        "title": "Развитие городской среды Москвы",
                        "text": "АНО «МосводостокСтройТрест» объединяет опыт столичного строительства и современные технологии благоустройства.",
                        "button_text": "Об организации",
                        "button_link": organization_page,
                    },
                ),
                (
                    "cards",
                    [
                        {
                            "title": "Благоустройство",
                            "text": "Комплексные работы по развитию городской инфраструктуры.",
                        },
                        {
                            "title": "Капитальный ремонт",
                            "text": "Современные стандарты качества и безопасности.",
                        },
                        {
                            "title": "Спецпроекты",
                            "text": "Реализация задач учредителя и городских программ.",
                        },
                    ],
                ),
                (
                    "rich_text",
                    "АНО «МосводостокСтройТрест» работает для повышения комфорта жителей и гостей столицы.",
                ),
                ("latest_news", {"title": "Последние новости"}),
            ]
            home.save_revision().publish()

        if not LeadershipPage.objects.child_of(organization_index).exists():
            leadership_page = LeadershipPage(title="Руководство", slug="leadership")
            organization_index.add_child(instance=leadership_page)
            leadership_page.save_revision().publish()

        if not AwardsPage.objects.child_of(organization_index).exists():
            awards_page = AwardsPage(title="Оценка деятельности организации", slug="evaluation")
            organization_index.add_child(instance=awards_page)
            awards_page.save_revision().publish()

        news_index = NewsIndexPage.objects.child_of(home).first()
        if not news_index:
            news_index = NewsIndexPage(title="Новости", slug="news")
            home.add_child(instance=news_index)
            news_index.save_revision().publish()

        if not ContactsPage.objects.child_of(home).exists():
            contacts_page = ContactsPage(
                title="Контакты",
                slug="contacts",
                phone="+7 (495) 000-00-00",
                email="info@mvsst.ru",
                legal_address="Москва, ул. Примерная, д. 1",
                actual_address="Москва, ул. Примерная, д. 1",
                full_name="Автономная некоммерческая организация по развитию городской среды «МосводостокСтройТрест»",
                short_name="АНО «МосводостокСтройТрест»",
            )
            home.add_child(instance=contacts_page)
            contacts_page.save_revision().publish()

        image = self._get_placeholder_image()

        if not NewsPage.objects.child_of(news_index).exists():
            news_page = NewsPage(
                title="Запуск новой программы благоустройства",
                slug="new-program",
                date=date.today(),
                lead="Стартовала программа комплексного обновления городской инфраструктуры.",
                cover_image=image,
                body=[
                    ("heading", {"text": "Городские пространства становятся комфортнее"}),
                    ("paragraph", "Команда АНО «МосводостокСтройТрест» приступила к реализации ключевых проектов."),
                    ("quote", {"text": "Мы объединяем традиции строительства и современные технологии.", "author": "Пресс-служба"}),
                    ("key_figure", {"value": "4 000+", "label": "сотрудников вовлечены в проекты"}),
                ],
            )
            news_index.add_child(instance=news_page)
            news_page.save_revision().publish()

        LeadershipMember.objects.get_or_create(
            name="Иванов Иван Иванович",
            defaults={"position": "Генеральный директор", "photo": image, "sort_order": 1},
        )
        Award.objects.get_or_create(
            title="Благодарность за вклад в развитие городской среды",
            defaults={"description": "Почётная грамота за вклад в проекты благоустройства.", "image": image, "sort_order": 1},
        )

        editor_group, _ = Group.objects.get_or_create(name="Редактор новостей")
        permissions = Permission.objects.filter(codename__in=["add_page", "change_page", "publish_page"])
        editor_group.permissions.add(*permissions)
        GroupPagePermission.objects.get_or_create(
            group=editor_group,
            page=news_index,
            permission_type="add",
        )
        GroupPagePermission.objects.get_or_create(
            group=editor_group,
            page=news_index,
            permission_type="edit",
        )
        GroupPagePermission.objects.get_or_create(
            group=editor_group,
            page=news_index,
            permission_type="publish",
        )

        self.stdout.write(self.style.SUCCESS("Bootstrap завершён."))

    def _get_placeholder_image(self):
        Image = get_image_model()
        image = Image.objects.first()
        if image:
            return image
        file_name = "placeholder.png"
        image_file = ContentFile(PLACEHOLDER_PNG, name=file_name)
        return Image.objects.create(title="Placeholder", file=image_file)
