from decimal import Decimal

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class Card(models.Model):
    """Model card"""
    TERM_CHOICES = (
        ('1', '1 месяц'),
        ('6', '6 месяцев'),
        ('12', '1 год'),
    )
    series_valid = RegexValidator(regex='^\d{4}$')
    series = models.PositiveSmallIntegerField(
        validators=[series_valid], verbose_name='серия',
        error_messages='серия карты состоит из 4х цифр')
    numbers = models.PositiveBigIntegerField(verbose_name='номер')
    release_data = models.DateTimeField(auto_now_add=True,
                                        verbose_name='дата выпуска')
    term = models.PositiveSmallIntegerField(choices=TERM_CHOICES,
                            verbose_name='срок')
    end_activity = models.DateTimeField(
        verbose_name='дата окончания активности')
    amount = models.DecimalField(max_digits=10,
                                 decimal_places=2, default=0,
                                 verbose_name='сумма',
                                 validators=[
                                     MinValueValidator(Decimal('0.00'))])
    is_active = models.BooleanField(default=False, verbose_name='активирована')
    overdue = models.BooleanField(default=False, verbose_name='просрочена')
    is_delete = models.BooleanField(default=False, verbose_name='удалена')

    class Meta:
        db_table = "card"
        verbose_name = "Карта"
        verbose_name_plural = "Карты"

    def __str__(self):
        return f'{self.series} №{self.numbers}'


class ProfileCard(models.Model):
    """Profile Card"""
    objects = None
    card = models.OneToOneField(Card, on_delete=models.CASCADE,
                                verbose_name='карта')
    first_name = models.CharField(max_length=128, verbose_name='имя')
    last_name = models.CharField(max_length=128, verbose_name='фамилия')
    email = models.EmailField(verbose_name='email')
    phone_number_regex = RegexValidator(regex=r"\+7\d{10,10}$")
    phone = models.CharField(validators=[phone_number_regex], max_length=12,
                             blank=True, verbose_name='телефон')

    class Meta:
        db_table = "profile"
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class HistoryCard(models.Model):
    """Date of use card"""
    card = models.ForeignKey(Card, on_delete=models.CASCADE,
                             verbose_name='карта')
    data_use = models.DateTimeField(verbose_name='дата использования')

    class Meta:
        db_table = "history_card"
        verbose_name = "История карты"
        verbose_name_plural = "История карты"

    def __str__(self):
        return f'{self.card}'
