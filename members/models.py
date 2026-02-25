from django.db import models
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image

@register_snippet
class Member(models.Model):
    ROLE_CHOICES = [('player', '選手'), ('manager', 'マネージャー')]
    
    name = models.CharField(max_length=50, verbose_name="名前")
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES, default='player', verbose_name="役職")
    grade = models.CharField(max_length=20, verbose_name="学年", help_text="例: 3回生")
    position = models.CharField(max_length=50, blank=True, verbose_name="ポジション")
    hometown = models.CharField(max_length=50, blank=True, verbose_name="出身地/出身校")
    profile_text = models.TextField(blank=True, verbose_name="紹介文")
    intro_url = models.URLField(blank=True, verbose_name="紹介記事のURL", help_text="クリック時の飛び先URL（空欄の場合はリンクになりません）")
    
    # 画像はWagtail標準のImageモデルと紐づけ
    photo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    
    display_order = models.IntegerField(default=0, verbose_name="表示順", help_text="数字が小さいほど上に表示されます")
    is_published = models.BooleanField(default=True, verbose_name="公開する")

    panels = [
        FieldPanel('name'), FieldPanel('role_type'), FieldPanel('grade'),
        FieldPanel('position'), FieldPanel('hometown'), FieldPanel('profile_text'),
        FieldPanel('intro_url'),
        FieldPanel('photo'), FieldPanel('display_order'), FieldPanel('is_published'),
    ]

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.name} ({self.get_role_type_display()})"

class MembersPage(Page):
    """メンバー一覧ページ"""
    def get_context(self, request):
        context = super().get_context(request)
        members = Member.objects.filter(is_published=True)
        context['players'] = members.filter(role_type='player')
        context['managers'] = members.filter(role_type='manager')
        return context