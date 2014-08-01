# -*- coding: utf-8 -*-


'''
PIL's Image.thumbnail() returns an image that fits inside of a given size (preserving aspect ratios)
but the size of the actual image will vary and is certainly not guaranteed to be the requested size.
This is often inconvenient since the size of the returned thumbnail cannot be predicted. The django-thumbs
library solves this for square thumbnails by cropping the image to a square and then resizing it. However,
this only works for exact squares.
 
This function generalizes that approach to work for thumbnails of any aspect ratio. The returned thumbnail
is always exactly the requested size, and edges (left/right or top/bottom) are cropped off to adjust to
make sure the thumbnail will be the right size without distorting the image.
'''
 
# TODO: this is only used for the Image.ANTIALIAS constant. seems kind of trivial...
from PIL import Image
from PIL import ExifTags
from StringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def flat( *nums ):
    'Build a tuple of ints from float or integer arguments. Useful because PIL crop and resize require integer points.'
    
    return tuple( int(round(n)) for n in nums )
 
class Size(object):
    def __init__(self, pair):
        self.width = float(pair[0])
        self.height = float(pair[1])
 
    @property
    def aspect_ratio(self):
        return self.width / self.height
 
    @property
    def size(self):
        return flat(self.width, self.height)
 
def cropped_thumbnail(img, size):
    '''
    Builds a thumbnail by cropping out a maximal region from the center of the original with
    the same aspect ratio as the target size, and then resizing. The result is a thumbnail which is
    always EXACTLY the requested size and with no aspect ratio distortion (although two edges, either
    top/bottom or left/right depending whether the image is too tall or too wide, may be trimmed off.)
    '''
    
    original = Size(img.size)
    target = Size(size)
 
    if target.aspect_ratio > original.aspect_ratio:
        # image is too tall: take some off the top and bottom
        scale_factor = target.width / original.width
        crop_size = Size( (original.width, target.height / scale_factor) )
        top_cut_line = (original.height - crop_size.height) / 2
        img = img.crop( flat(0, top_cut_line, crop_size.width, top_cut_line + crop_size.height) )
    elif target.aspect_ratio < original.aspect_ratio:
        # image is too wide: take some off the sides
        scale_factor = target.height / original.height
        crop_size = Size( (target.width/scale_factor, original.height) )
        side_cut_line = (original.width - crop_size.width) / 2
        img = img.crop( flat(side_cut_line, 0,  side_cut_line + crop_size.width, crop_size.height) )
        
    return img.resize(target.size, Image.ANTIALIAS)

class ImageHelper():
    """
    #sizes of houzz
    SIZES = [(80,80, False), (160, 160, False), (240, 240, False), (320, 320, False), (640, 640, False),
        (75, 55, True), (160, 120, True), (240, 190, True), (500, 2560, False), (500, 500, False), (363, 363, False),
        (105, 105, True), (220, 220, True), (550, 2560, False), (990, 990, False), (1600, 1060, True), (2560, 2560, False)
        ]

    ipad ratio = 1.33:  4:3
    (2048, 1536, 2), (1024, 768)

    iphone4, LG ratio = 1.5 3:2
    (960, 640, 3), (480, 320)

    common android tabs, ratio = 1.6
    (2560, 1600, 2), (1920, 1200, (1.5, 2)), (1280, 800), (1, 1.5, 2)), (960, 600, 2)

    google nexus, LG, HTC, blackberry, samsung s, s2, Nokia lumia,  ratio = 1.67  5:3
    (1280, 768, 2), (800, 480, 1.5)

    samsung tab, blackberry, amazon kindle ratio = 1.7
    (1024, 600)

    iphone5, google,  sony, samsung s4, nokia, moto, HTC, blackberry, xiaomi ratio = 1.78 16:9
    (1920, 1080, 3), (1280, 720, 2), (1136, 640, 2), (960, 540, 1.5), (854, 480, 1), (640, 360)

    """
    MAX_SIZE = (2560, 2560)
    MIN_SIZE = 480
    SIZES = {
        1: (2048, 1536),
        2: (1280, 800),
        #3: (1280, 720),
        #4: (1136, 640),
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


    def __init__(self, obj):
        self.obj = obj
        self.image = obj.image
        self._im = None
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        self.orientTag = orientation

    def rotate(self, im):
        if hasattr(im, '_getexif'):  # only present in JPEGs
            e = im._getexif()       # returns None if no EXIF data
            if e is not None:
                exif = dict(e.items())
                orientation = exif.get(self.orientTag)
                if orientation == 3:
                    im = im.transpose(Image.ROTATE_180)
                elif orientation == 6:
                    im = im.transpose(Image.ROTATE_270)
                elif orientation == 8:
                    im = im.transpose(Image.ROTATE_90)
        return im

    @property
    def im(self):
        if self._im is None:
            self._im = self.rotate(Image.open(self.image.file))
        return self._im

    @property
    def size(self):
        return self.im.size

    def resize(self, size, crop=True):
        if crop:
            thumb = cropped_thumbnail(self.im, size)
        else:
            thumb = self.im
            thumb.thumbnail(size, Image.ANTIALIAS)
        temp = StringIO()
        #quality=80 progressive=True, optimize=True
        thumb.save(temp, 'jpeg')
        data = InMemoryUploadedFile(temp, None, 'foo.jpg', 'image/jpeg', temp.len, None)
        return data, thumb.size

    def save_init(self, crop=False):

        width, height = self.size
        if width < self.MIN_SIZE or height < self.MIN_SIZE:
            raise ImageSaveError("invalid image dimension")
        filename = self.obj.get_name(0)
        data, (width, height) = self.resize(self.MAX_SIZE, crop)
        self.image.save(filename, data, save=False)

        # Mark if landscape picture
        array = 0 if width < height else 1
        thumbs = []
        for i in self.SIZES:
            size = self.SIZES[i]
            if (width >= size[0] and height >= size[1]) or\
                (width >= size[1] and height >= size[0]):
                array |= (1 << i)
                thumbs.append(i)
        self.obj.array = array
        self.obj.thumbs = thumbs

    def save(self, key):
        size = self.SIZES.get(key)
        if not size:
            return False
        width, height = self.size
        #thumbnail use strict mode, should not revert
        if key < 16 and width < height:
            size = size[1], size[0]

        filename = self.obj.get_name(key)
        data, s = self.resize(size)
        self.image.save(filename, data, save=False)
        return True