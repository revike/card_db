from django.contrib import admin
from django.contrib.auth.models import Group

from main_app.models import HistoryCard, Card, ProfileCard


class ProfileCardInline(admin.StackedInline):
    """Profile card inline"""
    model = ProfileCard
    can_delete = False


class HistoryCardInline(admin.StackedInline):
    """History Card Inline"""
    model = HistoryCard
    extra = 0
    max_num = 0
    min_num = 0
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    """Card Admin"""
    inlines = [ProfileCardInline, HistoryCardInline]
    inline_reverse = ['card']
    list_display = ('series', 'numbers', 'is_active', 'overdue', 'is_delete')
    list_display_links = ('series', 'numbers')
    fields = (
        'series', 'numbers', 'release_data', 'term', 'amount',
        'is_active',
        'overdue', 'is_delete')
    readonly_fields = (
        'series', 'numbers', 'release_data', 'term', 'amount',
        'overdue')
    list_filter = ('series', 'term', 'is_active', 'overdue', 'is_delete',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.unregister(Group)
admin.site.site_header = 'Бонусные карты'
