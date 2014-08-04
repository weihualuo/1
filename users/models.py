# coding:utf8
from django.db import models
from django.contrib.auth.models import User
from invt import settings
from utils.thumbnail import ImageHelper
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext as _

EndUser = User

class UserImageHelper(ImageHelper):

    MAX_SIZE = (150, 150)
    MIN_SIZE = 150
    SIZES = {}

class Profile(models.Model):

    #Called by ImageHelper on save
    def get_name(self, seq):
        return self.user.username + '-' + get_random_string(5) + '.' + 'jpg'

    GENDER_CHOICES = (
        ('m', _('Male')),
        ('f', _('Female')),
    )
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to='avatar', storage=settings.STORAGE, blank=True, null=True)
    # 1: created  2: user email verified ...
    status = models.SmallIntegerField(default=0)
    gender = models.CharField(_("Gender"), max_length=1, choices=GENDER_CHOICES, blank=True)
    desc = models.TextField(_('Sign'), blank=True)

    def save(self, *args, **kwargs):

        # in case of new object
        from django.core.files.uploadedfile import UploadedFile
        if hasattr(self.image, 'file') and isinstance(self.image.file, UploadedFile):
            upload_file = self.image.file
            DJANGO_TYPE = upload_file.content_type
            if DJANGO_TYPE != 'image/jpeg':
                raise StandardError("do not support "+DJANGO_TYPE)
            UserImageHelper(self).save_init(True)

        super(Profile, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s" % self.user

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = 'user profiles'

class OAuth(models.Model):

    ORIGIN_CHOICES = (
        ('o', "self"),
        ('s', "SINA"),
        ('q', "QQ"),
        ('w', "WeChat"),
    )

    # user a unified name author
    author = models.ForeignKey(EndUser)
    openid = models.CharField(max_length=100)
    origin = models.CharField(max_length=1, choices=ORIGIN_CHOICES)
    expires = models.IntegerField(blank=True, null=True)
