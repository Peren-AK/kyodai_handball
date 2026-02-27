from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # ★追加

class BlogIndexPage(Page):
    intro = models.CharField(max_length=250, blank=True, verbose_name="説明文")

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        now = timezone.now()
        
        blogpages = BlogPage.objects.child_of(self).live().filter(
            published_date__lte=now
        ).order_by('-published_date')

        # ページネーションの設定（1ページにつき10件表示）
        paginator = Paginator(blogpages, 10)
        page = request.GET.get('page')
        
        try:
            blogpages_paginated = paginator.page(page)
        except PageNotAnInteger:
            blogpages_paginated = paginator.page(1)
        except EmptyPage:
            blogpages_paginated = paginator.page(paginator.num_pages)
        
        context['blogpages'] = blogpages_paginated
        return context

class BlogPage(Page):
    published_date = models.DateTimeField("公開日時", default=timezone.now)
    category = models.CharField("カテゴリ", max_length=50, blank=True, help_text="例: 試合レポート, イベント")
    body = RichTextField(blank=True, verbose_name="本文")

    content_panels = Page.content_panels + [
        FieldPanel('published_date'),
        FieldPanel('category'),
        FieldPanel('body'),
    ]