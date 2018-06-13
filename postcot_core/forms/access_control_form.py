from django import forms
from django.contrib.admin import widgets as admin_widgets

from ..base_types import AccessControlRole, AccessControlContent
from ..models import AccessAction

import enumfields


class AccessControlForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['postfix_identifier'].widget.attrs['readonly']='readonly'

    subject_role: AccessControlRole = enumfields.EnumField(
        AccessControlRole,
        max_length=1,
    ).formfield(
        label='Subject Role',
        initial=AccessControlRole.CLIENT
    )

    subject_content: AccessControlContent = enumfields.EnumField(
        AccessControlContent,
        max_length=1,
    ).formfield(
        label='Subject Content',
        initial=AccessControlContent.HOSTNAME
    )

    reverses_hostname: bool = forms.BooleanField(
        label='Reverses Hostname',
        required=False
    )

    postfix_identifier: str = forms.CharField(
        widget=admin_widgets.AdminTextInputWidget,
        max_length=256,
    )

    pattern: str = forms.CharField(
        widget=admin_widgets.AdminTextInputWidget,
        help_text='''
<h5>Email Address Patterns</h5>
<dl>
    <dt>user@domain</dt>
    <dd>
        <p>Matches the specified mail address.</p>
    </dd>
    <dt>domain.tld</dt>
    <dd>
        <p>Matches domain.tld as the domain part of an email address.</p>
    </dd>
    <dt>user@Matches</dt>
    <dd>
        <p>All mail addresses with the specified user part.</p>
    </dd>
</dl>
<h5>Email Address Extension</h5>
<dl>
    <dd>
        When a mail address local-part contains the optional recipient 
        delimiter (e.g., user+foo@domain), the lookup order becomes: 
        user+foo@domain, user@domain, domain, user+foo@, and user@.
    </dd>
</dl>
<h5>HOST NAME/ADDRESS PATTERNS</h5>
<dl>
    <dt>domain.tld</dt>
    <dd>
        <p>Matches domain.tld.</p>
        <p>
            The pattern domain.tld also matches subdomains, but only when
            the string smtpd_access_maps is listed in the Postfix 
            parent_domain_matches_subdomains configuration setting. 
            Otherwise, specify .domain.tld (note the initial dot) in order 
            to match subdomains.
        </p>
    </dd>
    <dt>net.work.addr.ess</dt>
    <dt>net.work.addr</dt>
    <dt>net.work</dt>
    <dt>net</dt>
    <dd>
        <p>
            Matches the specified IPv4 host address or subnetwork. An IPv4 
            host address is a sequence of four decimal octets separated by
             ".".
        </p>
        <p>
            Subnetworks are matched by repeatedly truncating the last 
            ".octet" from the remote IPv4 host address string until a 
            match is found in the access table, or until further 
            truncation is not possible.
        </p>
        <ul>
            <li>
                NOTE 1: The access map lookup key must be in canonical 
                form: do not specify unnecessary null characters, and do 
                not enclose network address information with "[]" 
                characters.
            </li>
            <li>
                NOTE 2: use the cidr lookup table type to specify 
                network/netmask patterns. See cidr_table(5) for details.
            </li>
        </ul>
    </dd>
    <dt>net:work:addr:ess</dt>
    <dt>net:work:addr</dt>
    <dt>net:work</dt>
    <dt>net</dt>
    <dd>
        <p>
            Matches the specified IPv6 host address or subnetwork. An IPv6
            host address is a sequence of three to eight hexadecimal octet 
            pairs separated by ":".
        </p>

        <p>
            Subnetworks are matched by repeatedly truncating the last 
            ":octetpair" from the remote IPv6 host address string until a
            match is found in the access table, or until further 
            truncation is not possible.
        </p>
        
        <ul>
            <li>
                NOTE 1: the truncation and comparison are done with the 
                string representation of the IPv6 host address. Thus, not 
                all the ":" subnetworks will be tried.
            </li>
            <li>
                NOTE 2: The access map lookup key must be in canonical 
                form: do not specify unnecessary null characters, and do 
                not enclose network address information with "[]" 
                characters.
            </li>
            <li>
                NOTE 3: use the cidr lookup table type to specify 
                network/netmask patterns. See cidr_table(5) for details.
            </li>
        </ul>
        <p>IPv6 support is available in Postfix 2.2 and later.</p>
    </dd>
</dl>
'''
    )

    class Meta:
        model = AccessAction
        exclude = []

    class Media:
        js = (
            '//code.jquery.com/jquery-3.3.1.slim.min.js',
            'postcot/admin/js/access_control_change_form.js',
        )
        css = {
            'all': (
                'postcot/admin/css/change_form_help_text_postfix.css',
            ),
        }
