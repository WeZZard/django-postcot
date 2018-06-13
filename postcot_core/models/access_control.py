from django.db import models
from django.core import exceptions

from ..base_types import AccessControlPhase
from ..base_types import AccessControlInputKind
from .access_action import AccessAction

from ..validators import PostfixIdentifierValidator

import enumfields


class AccessControl(models.Model):
    phase: AccessControlPhase = enumfields.EnumField(
        AccessControlPhase, max_length=1
    )

    input_kind: AccessControlInputKind = enumfields.EnumField(
        AccessControlInputKind, max_length=1
    )

    reverses_hostname: bool = models.BooleanField(
        blank=True
    )

    postfix_identifier: str = models.CharField(
        max_length=256,
        validators=[PostfixIdentifierValidator()]
    )

    pattern: str = models.CharField(max_length=256)

    action: AccessAction = models.ForeignKey(
        to='AccessAction',
        on_delete=models.CASCADE,
        related_name='access_controls'
    )

    notes: str = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text='Notes on the account.'
    )

    def __str__(self) -> str:
        return '<%s> %s: %s' % (
            self.postfix_identifier,
            self.pattern,
            self.action.action
        )

    def clean(self):
        self._validate_subject_components_consistency()
        self._validate_pattern()

    def _validate_pattern(self):
        try:
            validate = self.input_kind.pattern_validator()
            validate()(self.pattern)
        except exceptions.ValidationError:
            raise exceptions.ValidationError(
                message='Invalid pattern: %s.' % self.pattern,
                params={'field': 'pattern'}
            )

    def _validate_subject_components_consistency(self):
        # TODO: Implement server-side consistency validation.
        pass

    class Meta:
        verbose_name = 'Access Control'
        verbose_name_plural = 'Access Controls'
