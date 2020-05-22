from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image
from django.urls import reverse
from phone_field import PhoneField

class Manager(BaseUserManager):
    def create_user(self, email, first_name, last_name, address, phone_number, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have an first name")
        if not last_name:
            raise ValueError("Users must have an last name")
        if not address:
            raise ValueError("Users must have an address")
        if not phone_number:
            raise ValueError("Users must have an phone number")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, address, phone_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(max_length=30, unique=False, verbose_name="<strong>First Name</strong>&nbsp;")
    last_name = models.CharField(max_length=30, unique=False, verbose_name="<strong>Last Name</strong>&nbsp;")
    address = models.CharField(max_length=3000, unique=False, verbose_name="<strong>Address</strong>&nbsp;", help_text='Ex: 123 Broad St, Newark, NJ, 07102', default='')
    phone_number = models.CharField(blank=False, help_text='Contact Phone Number', max_length=12, verbose_name="<strong>Phone Number</strong>&nbsp;")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name', 'address', 'phone_number']

    objects = Manager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics', verbose_name="Profile Image")

    def __str__(self):
        return f'{self.user.email} Profile'

        def save(self):
            super().save()

            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)
