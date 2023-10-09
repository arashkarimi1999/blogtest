from django.contrib.auth.models import AbstractUser
from django.db import models
# from apps.teacher_module.models import TalentCategory
# from sorl.thumbnail import ImageField, get_thumbnail
from PIL import Image


class Avatar(models.Model):
    user = models.ForeignKey("User",on_delete=models.CASCADE,related_name="user",default=0)
    avatar = models.ImageField(verbose_name="avatar gallery ",blank=True,null=True,upload_to="User-avatar")

# Create your models here.

class User(AbstractUser):
    activation_code = models.CharField(max_length=200, verbose_name='email-code verification')
    about = models.TextField(verbose_name="about user",null=True,blank=True)

    number =  models.IntegerField(blank=True,null=True,verbose_name="mobile-phone")

    
    # avatars = models.ManyToManyField('Avatar', blank=True)

    

    class Meta:

        verbose_name_plural = 'Users'
        verbose_name = 'User'

    def __str__(self):
        if self.first_name is not  "" and self.last_name is not  "":
            return self.get_full_name()
        return self.email
    
    # def save(self):
    #     super().save()  # saving image first

    #     img = Image.open(self.avatar.path) # Open image using self

    #     if img.height > 150 or img.width > 150:
    #         new_img = (150, 150)
    #         img.thumbnail(new_img)
    #         img.save(self.avatar.path)