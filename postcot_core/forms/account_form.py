from typing import Any, Optional, Dict, Set

from django import forms
from django.forms import widgets

from ..base_types import PasswordSchema
from ..models import Account
from ..utils import hash_password
from ..utils import verify_password

import enum


class PasswordUpdateProcess(enum.Enum):
    """Password update process."""

    """Set the hashed password directly"""
    SET = 0

    """Hash the password and then set."""
    HASH_AND_SET = 1


class AccountForm(forms.ModelForm):
    _PASSWORD_RELATED_FIELDS: set = {
        'password_schema',
        'old_password',
        'password',
        'password_again',
    }

    is_newly_created: bool = False

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.is_newly_created = kwargs.get('instance') is None

        self.fields['password_schema'].required = self.is_newly_created
        self.fields['password'].required = self.is_newly_created
        self.fields['password_again'].required = self.is_newly_created

    sets_hashed_password: bool = forms.BooleanField(
        label='Sets Encrypted Password Directly',
        help_text='''\
This system protects your password by storing its encrypted version with \
the encryption schema you specified. By checking this option, you can \
set the password's encrypted version directly.\
''',
        required=False
    )

    old_password: str = forms.CharField(
        label='Old Password',
        widget=widgets.PasswordInput,
        required=False
    )

    password: str = forms.CharField(
        widget=widgets.PasswordInput,
        required=False
    )

    password_again: str = forms.CharField(
        label='Password (again)',
        widget=widgets.PasswordInput,
        required=False
    )

    hashed_password: str = forms.CharField(
        label='Encrypted Password',
        max_length=256,
    )

    def clean(self) -> Dict[str, str]:
        account: Account = self.instance

        cleaned_data = super().clean()

        password_update_process = self._get_password_update_process(
            cleaned_data
        )

        if password_update_process:
            self._update_password(
                account,
                password_update_process,
                cleaned_data
            )

        return cleaned_data

    def _has_any_updates_to_password(self) -> bool:
        changed_fields = set(self.changed_data)
        required_fields = self._PASSWORD_RELATED_FIELDS
        return len(changed_fields.intersection(required_fields)) > 0

    def _get_password_update_process(
            self,
            cleaned_data: Dict[str, Any]
    ) -> Optional[PasswordUpdateProcess]:
        if self.is_newly_created or self._has_any_updates_to_password():
            sets_hashed_password = cleaned_data['sets_hashed_password']
            assert isinstance(sets_hashed_password, bool)
            if sets_hashed_password:
                return PasswordUpdateProcess.SET
            else:
                return PasswordUpdateProcess.HASH_AND_SET
        return None

    def _update_password(
            self,
            account: Account,
            update_process: PasswordUpdateProcess,
            cleaned_data: Dict[str, Any]
    ):
        password = cleaned_data['password']
        password_again = cleaned_data['password_again']

        if update_process == PasswordUpdateProcess.SET:
            if (
                self._validate_changes_consistency({
                    'password',
                    'password_again',
                }) and
                self._validate_password_consistency(
                    password,
                    password_again
                )
            ):
                account.hashed_password = password

        if update_process == PasswordUpdateProcess.HASH_AND_SET:
            old_password = cleaned_data['old_password']
            required_fields: Set[str] = {
                'password',
                'password_again',
            } if self.is_newly_created else {
                'old_password',
                'password',
                'password_again',
            }
            if (
                self._validate_changes_consistency(required_fields)
                and self._validate_password_consistency(
                    password,
                    password_again
                )
                and self._validate_password_not_empty(password)
                and (
                    self.is_newly_created
                    or self._verify_password(account, old_password)
                )
            ):
                schema = cleaned_data['password_schema']
                hashed_password = hash_password(
                    password,
                    PasswordSchema(schema)
                )
                account.hashed_password = hashed_password

    def _validate_password_not_empty(self, password: str):
        if len(password) == 0:
            self.add_error(
                field='password',
                error='Empty password is not allowed.'
            )
            self.add_error(
                field='password_again',
                error='Empty password is not allowed.'
            )
            return False
        return True

    def _validate_password_consistency(
            self,
            password: str,
            password_again: str
    ) -> bool:

        if password != password_again:
            self.add_error(
                field='password_again',
                error='Not the same to the password above.'
            )
            return False
        return True

    def _verify_password(
            self,
            account: Account,
            old_password: str
    ) -> bool:
        if self.is_newly_created:
            return True
        else:
            if not account.verify_password(
                    old_password
            ):
                self.add_error(
                    field='old_password',
                    error='Incorrect old password.'
                )
                return False
            else:
                return True

    def _validate_changes_consistency(self, fields: Set[str]) -> bool:
        changed_fields = set(self.changed_data)
        missing_fields = (fields - changed_fields)
        if len(missing_fields) > 0:
            for each_missing_field in missing_fields:
                self.add_error(
                    field=each_missing_field,
                    error='This field is required for updating password.'
                )
            return False
        return True

    class Meta:
        model = Account
        exclude = []

    class Media:
        js = (
            '//code.jquery.com/jquery-3.3.1.slim.min.js',
            'postcot/admin/js/account_change_form.js',
        )
