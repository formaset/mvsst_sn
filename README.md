# АНО «МосводостокСтройТрест»

Сайт организации на Django + Wagtail. Проект рассчитан на простой деплой на виртуальный хостинг (Beget), с хранением медиа в `MEDIA_ROOT` и сборкой статики через `collectstatic`.

## Быстрый старт (локально)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py bootstrap_site
python manage.py runserver
```

## Сборка статики

```bash
python manage.py collectstatic
```

## Админ-панель

Админка по умолчанию доступна по пути `/control/`.

Чтобы изменить путь, установите переменную окружения:

```bash
export ADMIN_PATH=custom-admin
```

## Переключение на MySQL

В `.env` укажите:

```env
DB_ENGINE=mysql
MYSQL_DATABASE=mvsst
MYSQL_USER=mvsst
MYSQL_PASSWORD=secret
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

## Загрузка медиа

Медиа сохраняются в `MEDIA_ROOT` (`./media`). Для переноса медиа достаточно скопировать содержимое папки на сервер.

## Заполнение сайта стартовыми данными

```bash
python manage.py bootstrap_site
```

Команда создаст структуру страниц и примерные записи новостей, руководства и наград.
