from django.db import models
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel

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


# スポンサーモデル
@register_snippet
class Sponsor(models.Model):
    name = models.CharField(max_length=100, verbose_name="スポンサー名")
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="ロゴ画像"
    )
    url = models.URLField(blank=True, verbose_name="リンク先URL", help_text="クリック時の飛び先")
    display_order = models.IntegerField(default=0, verbose_name="表示順", help_text="数字が小さいほど左に表示されます")
    is_published = models.BooleanField(default=True, verbose_name="公開する")

    panels = [
        FieldPanel('name'),
        FieldPanel('logo'),
        FieldPanel('url'),
        FieldPanel('display_order'),
        FieldPanel('is_published'),
    ]

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "スポンサー"
        verbose_name_plural = "スポンサー一覧"

    def __str__(self):
        return self.name