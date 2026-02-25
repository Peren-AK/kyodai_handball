from django.db import models
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

@register_setting
class SiteSettings(BaseSiteSetting):
    ga4_measurement_id = models.CharField(max_length=50, blank=True, help_text="例: G-XXXXXXXXXX")
    contact_form_url = models.URLField(blank=True, help_text="GoogleフォームのURL")
    sponsor_form_url = models.URLField(blank=True, help_text="スポンサー用GoogleフォームのURL")
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    x_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "サイト全体設定"