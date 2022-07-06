from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin, )
from django.db import models


class Role(models.Model):
    role_name = models.CharField(max_length=100)
    permission = models.CharField(max_length=100)


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str = None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str = None, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email=email, password=password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self._create_user(email=email, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(
        'email address',
        max_length=255,
        unique=True,
        error_messages={'unique': "A user with that email already exists.", }
    )
    is_email_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_created=True, auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField('active',
                                    default=True,
                                    help_text=('Designates whether this user should be treated as active. '
                                               'Unselect this instead of deleting accounts.'
                                               ),
                                    )
    is_staff = models.BooleanField('staff status',
                                   default=False,
                                   help_text='Designates whether the user can log into this admin site.',
                                   )
    date_joined = models.DateTimeField(auto_now_add=True)
    contact = models.BigIntegerField(null=True, blank=True)
    is_contact_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    #
    # class Meta:
    #     db_table = "User"
    #     verbose_name = 'user'
    #     verbose_name_plural = 'users'


class Company(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField()
    owner = models.CharField(max_length=255, null=True, blank=True)
    subdomain = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


class Menu(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField()
    time_scheduling = models.BooleanField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class MenuCategory(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

#
# class Sliders(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     image = models.ImageField()
#     heading = models.CharField(max_length=100)
#     description = models.TextField()
#     link = models.URLField(max_length=10000)
#     coupon = models.CharField(max_length=100)
#     created = models.DateTimeField(auto_now_add=True)


# class Profile(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     user = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     desigination = models.CharField(max_length=255)
#     type = models.CharField(max_length=255)


# class Guests(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     phone_number = models.BigIntegerField()


# class Coupons(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     code = models.CharField(max_length=255)
#     discount_type = models.CharField(max_length=255)
#     discount_amt = models.CharField(max_length=100)
#     valid_till = models.DateTimeField()
#     max_usage = models.IntegerField()
#     min_subtotal = models.CharField(max_length=255)
#     sub_text = models.TextField(max_length=1000)
#     type = models.CharField(max_length=255)
#     is_active = models.BooleanField()


# class Order(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     guest = models.ForeignKey(Guests, on_delete=models.CASCADE)
#     coupon = models.ForeignKey(Coupons, on_delete=models.CASCADE)


class AddonCategory(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class AddonItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    addon_category = models.ForeignKey(AddonCategory, on_delete=models.CASCADE)


class Items(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()
    price = models.CharField(max_length=255)
    disc_price = models.CharField(max_length=255)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    menu_category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    addon_category = models.ForeignKey(AddonCategory, on_delete=models.CASCADE)
    is_veg = models.BooleanField()
    is_recommended = models.BooleanField()
    is_popular = models.BooleanField()
    is_new = models.BooleanField()


# class Order_item(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     item = models.ForeignKey(Items, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#
#
# class Room_service(models.Model):
#     room = models.ForeignKey(Company, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     company = models.CharField(max_length=255)
#     created = models.DateTimeField(auto_now_add=True)


# Standard Model
class Standard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


# Room Model
Room_Choices = (('room', 'Room'), ('table', 'Table'))


class Room(models.Model):

    room_number = models.IntegerField()
    type = models.CharField(max_length=255, choices=Room_Choices)
    resident = models.ForeignKey(User, on_delete=models.CASCADE)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)