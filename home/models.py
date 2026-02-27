from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image
from matches.models import MatchEntry
from blog.models import BlogPage
from core.models import Sponsor
from django.utils import timezone # ★この1行が足りていませんでした！

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
        
        # ★現在時刻より過去のブログだけを取得
        now = timezone.now()
        context['latest_blogs'] = BlogPage.objects.live().public().filter(
            published_date__lte=now
        ).order_by('-published_date')[:3]
        
        context['sponsors'] = Sponsor.objects.filter(is_published=True)
        return context