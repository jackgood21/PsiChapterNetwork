from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageOps, ExifTags
import datetime
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to='profile_pics')
    year =  models.CharField(max_length=100)
    major = models.CharField(max_length =200, default = "")
    company =  models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length = 10)

    def printPhoneNumber(self):
        clean = self.phone.strip('(').strip(')').strip('+').strip(' ').strip('-')
        if len(clean) and clean != None and clean != "":
            return '{}-{}-{}'.format(clean[0:3], clean[3:6], clean[6:])
        else:
            return ""
    def __str__(self):
        return f'{self.user.username} Profile'

    def is_future_event(self):
        year =0
        if self.year != "":
            year = int(self.year)
        return year > datetime.datetime.now().year

    # def save(self, *args, **kwargs):
    #     super().save(*args,**kwargs)
    #     im = Image.open(self.image.path)
    #     width, height = im.size   # Get dimensions
    #     file_format = im.format
    #     exif = im._getexif()
    #
    #     orientation_key = 274
    #     if exif and orientation_key in exif:
    #         orientation = exif[orientation_key]
    #         rotate_values = {
    #             3: Image.ROTATE_180,
    #             6: Image.ROTATE_270,
    #             8: Image.ROTATE_90
    #         }
    #
    #         if orientation in rotate_values:
    #             im = im.transpose(rotate_values[orientation])
    #




    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)
        im = Image.open(self.image.path)
        file_format = im.format

        try:
            exif = im._getexif()
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation]=='Orientation':
                    break
            exif=dict(im._getexif().items())
            if exif[orientation] == 3:
                im=im.rotate(180, expand=True)
            elif exif[orientation] == 6:
                im=im.rotate(270, expand=True)
            elif exif[orientation] == 8:
                im=im.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            pass
        width, height = im.size   # Get dimensions

        if height - width > 50:
            left = 0
            top = 0
            right = width
            bottom = width+20
            im = im.crop((left, top, right, bottom))
            im.save(self.image.path)
        else:
            output_size = (300,300)
            im.thumbnail(output_size)
            im.save(self.image.path)
            # cases: image don't have getexif

        # basewidth = 1000
        #
        # wpercent = (basewidth/float(img.size[0]))
        # hsize = int((float(img.size[1])*float(wpercent)))
        # img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        # img.save(self.image.path)
