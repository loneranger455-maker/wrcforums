from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
import datetime,uuid

class UserManager(BaseUserManager):
    def create_user(self, email, username,password=None,passwordconfirm=None):
       
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
           
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username=models.CharField(verbose_name='username',
        max_length=255,
        unique=True,)
    password=models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
            "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
            return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     #"Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

    
class Content(models.Model):
    posted_by=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    title=models.CharField(max_length=200)
    contentvalue=models.TextField()
    link=models.CharField(max_length=200,default="",blank=True)
    post_type=models.CharField(max_length=200,blank=True)
    def __str__(self):
        return str(self.title)

class Comments(models.Model):
    post=models.ForeignKey(Content,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    






