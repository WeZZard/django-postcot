from django.contrib import admin

from .models import (Domain, Account, Alias, AccessAction, AccessControl)


from .forms import (
    DomainForm,
    AccountForm,
    AliasForm,
    AccessActionForm,
    AccessControlForm
)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    form = DomainForm

    list_display = ('domain_name', 'notes')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    form = AccountForm

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self._fieldsets_for_creation
        else:
            return self._fieldsets_for_update

    readonly_fields = ['hashed_password']

    list_display = ('email_address', 'local_part', 'domain', 'is_active', 'notes')

    ordering = ('local_part', 'domain', 'is_active')

    _fieldsets_for_creation = [
        (None, {'fields': ['local_part', 'domain', 'notes']}),

        ('Password', {
            'fields': [
                'password_schema',
                'sets_hashed_password',
                'password',
                'password_again',
            ]
        })
    ]

    _fieldsets_for_update = [
        (None, {'fields': [('local_part', 'is_active'), 'domain', 'notes']}),

        ('Password', {
            'fields': [
                'hashed_password',
                'password_schema',
                'sets_hashed_password',
                'old_password',
                'password',
                'password_again',
            ],
        })
    ]


@admin.register(Alias)
class AliasAdmin(admin.ModelAdmin):
    form = AliasForm

    list_display = ('alias_name', 'account', 'email_address', 'notes')

    ordering = ('alias_name', 'account')


@admin.register(AccessAction)
class AccessActionAdmin(admin.ModelAdmin):
    form = AccessActionForm

    list_display = ('action', 'notes')

    change_form_template = 'admin/access_action_change_form.html'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return 'action',
        return ()

    fields = ['action', 'notes']


@admin.register(AccessControl)
class AccessControlAdmin(admin.ModelAdmin):
    form = AccessControlForm

    list_display = ('postfix_identifier', 'pattern', 'action')

    ordering = ('postfix_identifier', )

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self._fieldsets_for_creation
        else:
            return self._fieldsets_for_update

    _fieldsets_for_creation = [
        (None, {
            'fields': [
                ('phase', 'input_kind', 'reverses_hostname'),
                'postfix_identifier',
                'pattern',
                'action',
                'notes'
            ]
        }),
    ]

    _fieldsets_for_update = [
        (None, {
            'fields': [
                ('phase', 'input_kind', 'reverses_hostname'),
                'postfix_identifier',
                'pattern',
                'action',
                'notes'
            ]
        }),
    ]
