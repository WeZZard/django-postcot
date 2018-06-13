from django.db import models

from .domain import Domain
from ..base_types import PasswordSchema
from ..utils import verify_password
from ..validators import UsernamePatternValidator


class Account(models.Model):
    PASSWORD_SCHEMA_CHOICES = (
        ('Plain', (
            PasswordSchema.PLAIN,
        )),
        ('CRYPT Schemas', (
            PasswordSchema.CRYPT,
            PasswordSchema.DES_CRYPT,
            PasswordSchema.MD5_CRYPT,
            PasswordSchema.SHA256_CRYPT,
            PasswordSchema.SHA512_CRYPT,
            PasswordSchema.BLF_CRYPT,
        )),
        ('MD5 Based Schemas', (
            PasswordSchema.PLAIN_MD5,
            PasswordSchema.LDAP_MD5,
            PasswordSchema.SALTED_MD5,
        )),
        ('SHA Based Schemas', (
            PasswordSchema.SHA,
            PasswordSchema.SHA256,
            PasswordSchema.SHA512,
            PasswordSchema.SALTED_SHA,
            PasswordSchema.SALTED_SHA256,
            PasswordSchema.SALTED_SHA512,
        )),
        ('Other', (
            PasswordSchema.PBKDF2,
        )),
    )

    is_active: bool = models.BooleanField(
        default=True,
        verbose_name='Active'
    )

    local_part: str = models.CharField(
        max_length=256,
        verbose_name='Name',
        validators=[UsernamePatternValidator()],
    )

    domain: Domain = models.ForeignKey(
        to=Domain,
        on_delete=models.CASCADE,
        related_name='accounts',
        null=True,
        blank=True
    )

    notes: str = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text='Notes on the account.'
    )

    password_schema: str = models.CharField(
        choices=PASSWORD_SCHEMA_CHOICES,
        default=PasswordSchema.BLF_CRYPT.value,
        verbose_name='Password Schema',
        help_text='''\
<p>
    Schema for encrypting the stored password. The password would never be 
    stored with what it is when you input it unless you choose the 
    <b>PLAIN</b> schema. This is a way to protect your password from
    stealing by hacking into your server and pulling your database off.
</p>
<ul>
    <li>
        <b>PLAIN</b> is discouraged. If you want to set the stored 
        password directly, check <b>Sets Encrypted Password Directly</b>
    </li>
    <li>
        <b>CRYPT</b> schemas are generated with libc's crypt() function.
    </li>
</ul>
''',
        max_length=256
    )

    hashed_password: str = models.CharField(max_length=256)

    def email_address(self) -> str:
        return '%s@%s' % (self.local_part, self.domain.domain_name)

    def verify_password(self, old_password: str) -> bool:
        return verify_password(
            old_password,
            self.hashed_password,
            PasswordSchema(self.password_schema)
        )

    def __str__(self) -> str:
        return self.email_address()
