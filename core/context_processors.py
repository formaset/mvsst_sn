from wagtail.contrib.settings.context_processors import SettingsProxy


def site_settings(request):
    return {"site_settings": SettingsProxy(request)}
