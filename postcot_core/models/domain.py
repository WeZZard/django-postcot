from django.db import models

from ..validators import DomainValidator


class Domain(models.Model):
    domain_name: str = models.CharField(
        max_length=256,
        verbose_name='Name',
        validators=[DomainValidator()]
    )

    notes: str = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text='Notes on the domain.'
    )

    def __str__(self) -> str:
        return self.domain_name
