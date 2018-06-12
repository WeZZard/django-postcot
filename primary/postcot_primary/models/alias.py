from django.db import models

from .account import Account

from ..validators import UsernamePatternValidator


class Alias(models.Model):
    alias_name: str = models.CharField(
        max_length=256,
        validators=[UsernamePatternValidator()],
        verbose_name='Name'
    )

    account: Account = models.ForeignKey(
        to=Account,
        on_delete=models.CASCADE,
        related_name='aliases'
    )

    notes: str = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text='Notes on the alias.'
    )

    def email_address(self) -> str:
        return '%s@%s' % (self.alias_name, self.account.domain)

    def __str__(self) -> str:
        return '%s => %s' % (self.alias_name, self.account)

    class Meta:
        verbose_name = 'Alias'
        verbose_name_plural = 'Aliases'
