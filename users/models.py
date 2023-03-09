from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, address, phone_number, user_type, password=None):
        """
        Creates and saves a User with the given email, first name, last name, address, phone number, password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone_number=phone_number,
            user_type=user_type
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_type, first_name=None, last_name=None, address=None, phone_number=None,  password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email,
                                first_name=first_name,
                                last_name=last_name,
                                address=address,
                                phone_number=phone_number,
                                password=password,
                                user_type=user_type)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    USER_TYPES = (
                ('S', 'Student'),
                ('F', 'Faculty'),
                ('A', 'Admin')
            )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=500, null=True)
    user_type = models.CharField(max_length=1, choices=USER_TYPES, default='S')
    phone_number = PhoneNumberField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

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

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="College Management System"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
