from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
# Create your models here.


class MyUserManager(BaseUserManager):           # This is a database field
    def create_user(self, email, username=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
        	username = username,
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
        	username,
            email,
            password=password
            # username =username,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$' 


class MyUser(AbstractBaseUser):      # This is a main model field
    username = models.CharField(max_length=255, validators=[
                                                 RegexValidator(
                                                 	  regex=USERNAME_REGEX,
                                                      message='username must be AlphaNumeric',
                                                      code ='Invalid username'
                                                   )] ,# Python regular expression validator field
                                                 unique = True,
                                              )      

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    # date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

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
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin






# class Profile(models.Model):
# 	user = models.OneToOneField(settings.AUTH_USER_MODEL)
# 	city = models.CharField(max_length=255, null=True, blank=True)
# 	content = models.TextField(max_length=250, null=True, blank=True)
# 	integer = models.IntegerField(default=0)

# 	def __str__(self):
# 		return str(self.user.username)

# def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
# 	if created:
# 		try:
# 			Profile.object.create(user=instance)
# 		except:
# 			pass
# post_save.connect(post_save_user_model_receiver,sender=settings.AUTH_USER_MODEL)