import re, os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from invt import settings
from utils.thumbnail import ImageHelper
from django.utils.crypto import get_random_string

class Style(models.Model):
    cn = models.CharField(max_length=20, verbose_name=_("Style"))
    en = models.CharField(max_length=20, verbose_name="Style")

    def __unicode__(self):
        return self.en

    class Meta:
        verbose_name = _("Style")
        verbose_name_plural = _("Style")


class TemplateImageHelper(ImageHelper):

    MAX_SIZE = (1920, 1080)
    MIN_SIZE = 480
    SIZES = {
        1: (1920, 1080),
        4: (1136, 640),
        5: (1024, 768),
        6: (960, 640),
        7: (960, 540),
        8: (800, 480),
        10: (480, 320),

        17: (188, 188),
        18: (175, 175),
        19: (155, 155),
        20: (105, 105)
    }


API_BASE = 'api/templates/'
URI = 'templates'
# Create your models here.
class Template(models.Model):

    class Meta:
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')
        ordering = ['credit']

    title = models.CharField(_('Title'), max_length=60, blank=True)
    desc = models.TextField(_('Description'), blank=True)
    uri = models.URLField(_('uri'), blank=True)
    author = models.ForeignKey(User, related_name="templates", verbose_name=_("author"), blank=True)

    style = models.ForeignKey(Style, verbose_name=_('style'), blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    # Additional information about the templates
    meta = models.CharField(max_length=30, blank=True, unique=True)
    # bit array to indicate whether a thumb image exist
    array = models.IntegerField(default=0)
    # a value with the image, maybe used for ranking, priority
    credit = models.IntegerField(default=1)

    def get_image_path(self, filename):
        #Let it raise a error if not match
        m = re.search(r'-(\d+)\.', filename)
        return os.path.join('t', m.group(1), filename)

    def get_name(self, seq):
        s = self.style.en if self.style else ''
        return self.meta + '-' + s + '-' + str(seq) + '.' + 'jpg'

    #Thumbnail path is calculated from this name
    image = models.ImageField(upload_to=get_image_path, storage=settings.STORAGE)

    def __unicode__(self):
        return self.title

    def save_thumb(self, seq):
        return TemplateImageHelper(self).save(seq)

    def save(self, *args, **kwargs):

        helper = None
        # in case of new object
        if not self.pk:

            upload_file = self.image.file
            DJANGO_TYPE = upload_file.content_type
            if DJANGO_TYPE != 'image/jpeg':
                raise StandardError("do not support "+DJANGO_TYPE)

            helper = TemplateImageHelper(self)

            # meta is in unicode
            self.meta = 'U' + str(get_random_string(20))
            helper.save_init()

        super(Template, self).save(*args, **kwargs)

        if helper:
            from utils.async import add_task
            import pylibmc as memcache
            #from django.utils.crypto import get_random_string
            mc = memcache.Client()
            base = API_BASE + str(self.pk) + '/thumb?seq='
            thumbs = self.thumbs
            for i in thumbs:
                key = URI + str(self.pk) + '-' + str(i)
                value = get_random_string(8)
                mc.set(key, value)
                url = base + str(i) + '&token=' + value
                add_task('thumb', url)
