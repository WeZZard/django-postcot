from django.db import models

from ..validators import ActionValidator


class AccessAction(models.Model):
    action: str = models.TextField(
        unique=True,
        help_text='Cannot edit after created.',
        validators=[ActionValidator()]
    )

    notes: str = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text='Notes on the action.'
    )

    def __str__(self) -> str:
        return self.action

    class Meta:
        verbose_name = 'Access Action'
        verbose_name_plural = 'Access Actions'
