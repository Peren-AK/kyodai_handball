from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image
from matches.models import MatchEntry
from blog.models import BlogPage
from core.models import Sponsor # Sponsorをインポート

class HomePage(Page):
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="トップ背景画像"
    )

    content_panels = Page.content_panels + [
        FieldPanel('hero_image'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['next_match'] = MatchEntry.objects.filter(status='scheduled', is_published=True).order_by('match_datetime').first()
        context['latest_result'] = MatchEntry.objects.filter(status='finished', is_published=True).order_by('-match_datetime').first()
        context['latest_blogs'] = BlogPage.objects.live().public().order_by('-first_published_at')[:3]
        
        # 公開設定になっているスポンサーをコンテキストに追加
        context['sponsors'] = Sponsor.objects.filter(is_published=True)
        return context