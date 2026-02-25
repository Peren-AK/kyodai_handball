from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.utils import timezone

class BlogIndexPage(Page):
    """ブログ一覧ページ"""
    intro = models.CharField(max_length=250, blank=True, verbose_name="説明文")

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # 公開済みの記事（子ページ）を新しい順に取得
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

class BlogPage(Page):
    """個別のブログ記事ページ"""
    published_date = models.DateField("公開日", default=timezone.now)
    category = models.CharField("カテゴリ", max_length=50, blank=True, help_text="例: 試合レポート, イベント")
    body = RichTextField(blank=True, verbose_name="本文")

    content_panels = Page.content_panels + [
        FieldPanel('published_date'),
        FieldPanel('category'),
        FieldPanel('body'),
    ]