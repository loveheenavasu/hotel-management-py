from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin, )
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Role(models.Model):
    role_name = models.CharField(max_length=100, unique=True)
    permissions = ArrayField(models.CharField(max_length=10, blank=True, null=True), size=8,)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True, unique=True)
    phone_number = models.BigIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    brand_colour = models.CharField(max_length=255, null=True, blank=True)
    cover_image = models.CharField(max_length=500, null=True, blank=True)


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
    is_general_manager = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
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
    company_name = models.CharField(max_length=300, null=True, blank=True)
    logo = models.CharField(max_length=300, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    # class Meta:
    #     db_table = "user"
    #     verbose_name = 'user'
    #     verbose_name_plural = 'users'


class Company(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    logo = models.CharField(max_length=300, null=True, blank=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    subdomain = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Menu(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    image = models.CharField(max_length=300, null=True, blank=True)
    time_scheduling = models.BooleanField()
    earnings = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    item_stock = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class MenuCategory(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

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
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class AddonItem(models.Model):
    addon_category = models.ForeignKey(AddonCategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Items(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.CharField(max_length=300, null=True, blank=True)
    price = models.CharField(max_length=255)
    disc_price = models.CharField(max_length=255)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True)
    menu_category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    addon_category = models.ForeignKey(AddonCategory, on_delete=models.CASCADE, null=True, blank=True)
    is_veg = models.BooleanField()
    is_recommended = models.BooleanField()
    is_popular = models.BooleanField()
    is_new = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


# Standard Model
class Standard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


# Room Model
Room_Choices = (('room', 'Room'), ('table', 'Table'))


class Room(models.Model):
    resident = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, null=True, blank=True)
    room_number = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=255, choices=Room_Choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Guests(models.Model):
    # company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    # room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True, unique=True)
    phone = models.BigIntegerField(null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    tag_along_guests = models.CharField(max_length=100, null=True, blank=True)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    # wallet_amount = models.IntegerField(null=True, blank=True)
    # identity_proof = models.CharField(max_length=100, null=True, blank=True)


class Affiliate(models.Model):
    pass


class Coupon(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE, null=True, blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    discount_type = models.CharField(max_length=100, null=True, blank=True)
    discount_amount = models.IntegerField(null=True, blank=True)
    valid_till = models.DateTimeField(null=True, blank=True)
    max_usage = models.IntegerField(null=True, blank=True)
    min_subtotal = models.IntegerField(null=True, blank=True)
    subtext = models.TextField(max_length=300, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Order(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)
    guest = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Items, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


# class Room_service(models.Model):
#     room = models.ForeignKey(Company, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     company = models.CharField(max_length=255)
#     created = models.DateTimeField(auto_now_add=True)






