from django.core import validators


_VALID_POSTFIX_IDENTIFIERS = {
    'check_ccert_access',
    'check_client_access',
    'check_client_a_access',
    'check_client_ns_access',
    'check_client_mx_access',
    'check_sasl_access',

    'check_reverse_client_hostname_access',
    'check_reverse_client_hostname_a_access',
    'check_reverse_client_hostname_ns_access',
    'check_reverse_client_hostname_mx_access',

    'check_helo_access',
    'check_helo_a_access',
    'check_helo_ns_access',
    'check_helo_mx_access',

    'check_recipient_access',
    'check_recipient_a_access',
    'check_recipient_ns_access',
    'check_recipient_mx_access',

    'check_sender_access',
    'check_sender_a_access',
    'check_sender_ns_access',
    'check_sender_mx_access',
}


@validators.deconstructible
class PostfixIdentifierValidator(validators.RegexValidator):
    def __init__(self):
        pattern = "|".join(_VALID_POSTFIX_IDENTIFIERS)
        super(PostfixIdentifierValidator, self).__init__(
            regex=r'^%s$' % pattern,
            message='Invalid Postfix identifier.',
        )
