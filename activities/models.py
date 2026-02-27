from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

class StandardPage(Page):
    """部紹介や活動場所など、シンプルなテキストメインのページ用"""
    body = RichTextField(verbose_name="本文")
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

class ActivitiesPage(Page):
    """活動情報ページ"""
    
    # クラブプロフィール情報
    club_profile = RichTextField(blank=True, verbose_name="クラブプロフィール", help_text="所属や部員数などを記入してください")
    
    practice_schedule = RichTextField(blank=True, verbose_name="通常練習日程", help_text="例: 火・木 17:00~19:00 / 土 9:00~12:00")
    monthly_schedule = RichTextField(blank=True, verbose_name="年間スケジュール", help_text="1月〜12月の予定をリストで記載してください")

    content_panels = Page.content_panels + [
        FieldPanel('club_profile'),
        FieldPanel('practice_schedule'),
        FieldPanel('monthly_schedule'),
    ]