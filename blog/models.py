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
        
        # ★現在の日時（秒単位まで）を取得
        now = timezone.now()
        
        # ★BlogPageの中から「公開日時が今より過去（lte=now）」のものだけを取得！
        # （self.get_children() ではなく BlogPage.objects を使うのがポイントです）
        blogpages = BlogPage.objects.child_of(self).live().filter(
            published_date__lte=now
        ).order_by('-published_date')
        
        context['blogpages'] = blogpages
        return context

class BlogPage(Page):
    """個別のブログ記事ページ"""
    # ★DateField(日だけ) から DateTimeField(時間まで) に変更
    published_date = models.DateTimeField("公開日時", default=timezone.now)
    category = models.CharField("カテゴリ", max_length=50, blank=True, help_text="例: 試合レポート, イベント")
    body = RichTextField(blank=True, verbose_name="本文")

    content_panels = Page.content_panels + [
        FieldPanel('published_date'),
        FieldPanel('category'),
        FieldPanel('body'),
    ]