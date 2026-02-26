from django.db import models
from django.core.exceptions import ValidationError
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.contrib.table_block.blocks import TableBlock

@register_snippet
class MatchEntry(models.Model):
    CATEGORY_CHOICES = [('spring', '春リーグ'), ('autumn', '秋リーグ'), ('other', 'その他')]
    STATUS_CHOICES = [('scheduled', '予定'), ('finished', '終了'), ('cancelled', '中止')]
    OUTCOME_CHOICES = [('win', '勝ち'), ('lose', '負け'), ('draw', '引き分け'), ('none', '未定')]

    competition_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="大会カテゴリ")
    # ★ヘルプテキストを追加して「その他」の用途をわかりやすくしました
    competition_name = models.CharField(max_length=100, blank=True, verbose_name="大会名", help_text="「その他」を選択した場合は、ここに大会名（例: 西日本インカレ、七大戦など）を入力してください")
    opponent_name = models.CharField(max_length=100, verbose_name="対戦相手")
    match_datetime = models.DateTimeField(verbose_name="試合日時")
    venue_name = models.CharField(max_length=100, verbose_name="会場名")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name="ステータス")
    result_outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES, default='none', verbose_name="勝敗")

    # スコア
    score_kyodai_total = models.PositiveIntegerField(null=True, blank=True, verbose_name="京大 合計")
    score_opponent_total = models.PositiveIntegerField(null=True, blank=True, verbose_name="相手 合計")
    score_kyodai_first_half = models.PositiveIntegerField(null=True, blank=True, verbose_name="京大 前半")
    score_opponent_first_half = models.PositiveIntegerField(null=True, blank=True, verbose_name="相手 前半")
    score_kyodai_second_half = models.PositiveIntegerField(null=True, blank=True, verbose_name="京大 後半")
    score_opponent_second_half = models.PositiveIntegerField(null=True, blank=True, verbose_name="相手 後半")

    is_published = models.BooleanField(default=True, verbose_name="公開する")
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('competition_category'), FieldPanel('competition_name'),
        FieldPanel('opponent_name'), FieldPanel('match_datetime'),
        FieldPanel('venue_name'), FieldPanel('status'), FieldPanel('result_outcome'),
        FieldPanel('score_kyodai_total'), FieldPanel('score_opponent_total'),
        FieldPanel('score_kyodai_first_half'), FieldPanel('score_opponent_first_half'),
        FieldPanel('score_kyodai_second_half'), FieldPanel('score_opponent_second_half'),
        FieldPanel('is_published'),
    ]

    def clean(self):
        super().clean()
        if self.status == 'finished':
            required_scores = [
                self.score_kyodai_total, self.score_opponent_total,
                self.score_kyodai_first_half, self.score_opponent_first_half,
                self.score_kyodai_second_half, self.score_opponent_second_half
            ]
            if any(score is None for score in required_scores):
                raise ValidationError("試合終了(finished)の場合、すべてのスコアを入力してください。")
        elif self.status == 'scheduled':
            self.score_kyodai_total = self.score_opponent_total = None
            self.score_kyodai_first_half = self.score_opponent_first_half = None
            self.score_kyodai_second_half = self.score_opponent_second_half = None
            self.result_outcome = 'none'

    def __str__(self):
        return f"[{self.get_status_display()}] {self.match_datetime.strftime('%Y/%m/%d')} vs {self.opponent_name}"

@register_snippet
class StandingTable(models.Model):
    title = models.CharField(max_length=100, verbose_name="表タイトル（例: 2024年 春リーグ）")
    competition_category = models.CharField(max_length=20, choices=MatchEntry.CATEGORY_CHOICES)
    table_data = StreamField([('table', TableBlock(table_options={'renderer': 'html'}))], use_json_field=True, verbose_name="星取表")
    is_published = models.BooleanField(default=True)

    panels = [FieldPanel('title'), FieldPanel('competition_category'), FieldPanel('table_data'), FieldPanel('is_published')]

    def __str__(self):
        return self.title

class MatchHubPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        matches = MatchEntry.objects.filter(is_published=True).order_by('-match_datetime')
        context['spring_matches'] = matches.filter(competition_category='spring')
        context['autumn_matches'] = matches.filter(competition_category='autumn')
        # ★「その他」の試合をテンプレートに送る
        context['other_matches'] = matches.filter(competition_category='other')
        context['tables'] = StandingTable.objects.filter(is_published=True)
        return context