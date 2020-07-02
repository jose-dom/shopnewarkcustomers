from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image
from django.urls import reverse
from phone_field import PhoneField
from multiselectfield import MultiSelectField

BANNER_CHOICES = (
    ("Please create my banners. I understand there is a cost of $25","Please create my banners. I understand there is a cost of $25"),
    ("No, thank you. I will email you my banners (No Cost). If I do not email you my banners within 5 business days, I authorize you to create the banners for us at the above cost of $25 for both banners.","No, thank you. I will email you my banners (No Cost). If I do not email you my banners within 5 business days, I authorize you to create the banners for us at the above cost of $25 for both banners.")
)

BUSINESS_STRUCTURE_CHOICES = (
    ("Sole Proprietorship","Sole Proprietorship"),
    ("Limited Liability Corporation","Limited Liability Corporation"),
    ("S Corp","S Corp"),
    ("Other","Other")
)

LOCATION_TYPE = (
    ("Physical Location","Physical Location"),
    ("Home-based","Home-based"),
    ("Online","Online")
)

SPECIAL_BUSINESS = (
    ("Minority Owned","Minority Owned"),
    ("Woman Owned","Woman Owned"),
    ("MWBE Certified","MWBE Certified"),
    ("DBE Certified","DBE Certified"),
    ("VOSBE Certified","VOSBE Certified"),
    ("None","None")
)

TAX_CREDIT_OPTIONS = (
    ("On line, manually (Free)","On line, manually (Free)"),
    ("Downloading the application onto my own Android (Free)","Downloading the application onto my own Android (Free)"),
    ("Fincredit’s Dedicated Device and Stand ($90)","Fincredit’s Dedicated Device and Stand ($90)")
)

TAX_CREDITS_RATES = (
    ("Cost to me: 10%, Net Discount to Customer: 7.0%","Cost to me: 10%, Net Discount to Customer: 7.0%"),
    ("Cost to me: 14.3%, Net Discount to Customer: 10%","Cost to me: 14.3%, Net Discount to Customer: 10%"),
    ("Cost to me: 17.1%, Net Discount to Customer: 12%","Cost to me: 17.1%, Net Discount to Customer: 12%"),
    ("Other","Other")
)

TERMS_CONDITIONS = (
    ("Agree", "Agree"),
)

APPROVED_OPTIONS = (
    ("Yes", "Yes"),
    ("No", "No")
)

class Manager(BaseUserManager):
    def create_user(self, email, first_name, last_name, address, phone_number, is_vendor, password=None):
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
            is_vendor=is_vendor,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, address, phone_number, is_vendor, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone_number=phone_number,
            is_vendor=is_vendor,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_vendor = False
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

    first_name = models.CharField(max_length=30, unique=False, verbose_name="First Name")
    last_name = models.CharField(max_length=30, unique=False, verbose_name="Last Name")
    address = models.CharField(max_length=3000, unique=False, verbose_name="Address", help_text='Ex: 123 Broad St, Newark, NJ, 07102', default='')
    phone_number = models.CharField(blank=False, help_text='Contact Phone Number', max_length=12, verbose_name="Phone Number")
    is_vendor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name', 'address', 'phone_number', 'is_vendor']

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

class Vendor(models.Model):
    #owner
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    ##company info
    company_name = models.CharField(max_length=100, unique=False, verbose_name="Name of Business")
    legal_name = models.CharField(max_length=100, unique=False, verbose_name="Legal Name")
    address = models.CharField(max_length=100, unique=False, verbose_name="Address")
    business_type = models.CharField(max_length=100, unique=False, verbose_name="Type of Business")
    contact_name = models.CharField(max_length=100, unique=False, verbose_name="Contact Name")
    phone_number = models.CharField(max_length=12, blank=False, verbose_name="Contact Phone Number", help_text="Ex: 800-786-8765")
    website = models.CharField(max_length=30, unique=False, verbose_name="Website", help_text="Ex: www.example.com")

    ##banking info
    bank_name = models.CharField(max_length=100, unique=False, verbose_name="Bank Name", default="", blank=True)
    branch_location = models.CharField(max_length=100, unique=False, verbose_name="Branch Location", default="", blank=True)
    aba_number = models.CharField(max_length=100, unique=False, verbose_name="ABA Number", default="", blank=True)
    account_number = models.CharField(max_length=100, unique=False, verbose_name="Account Number", default="", blank=True)

    ##banner info
    banner = models.CharField(max_length=1000, choices=BANNER_CHOICES, verbose_name="Options", blank=True)

    ##speical business info
    business_structure = models.CharField(max_length=1000, choices=BUSINESS_STRUCTURE_CHOICES, verbose_name="Business Structure")
    length_of_operation = models.CharField(max_length=100, unique=False, verbose_name="Length of Operation", help_text="Ex: 10 months")
    number_of_employees = models.CharField(max_length=100, unique=False, verbose_name="Number of Employees", help_text="Ex: 12 employees")
    location_type = MultiSelectField(choices=LOCATION_TYPE, unique=False, verbose_name="Does your business have a physical location? (Check all that apply)")
    special_business = MultiSelectField(choices=SPECIAL_BUSINESS, unique=False, verbose_name="Is your business: (Check all that apply)")

    ##tax credits
    tax_credits = models.CharField(max_length=1000, choices=TAX_CREDIT_OPTIONS, verbose_name="Tax Credits", default="On line, manually (Free)")
    rate = models.CharField(choices=TAX_CREDITS_RATES, max_length=50, verbose_name="Percentage of Discount", default='', null=False)

    ##terms and conditions
    terms_conditions = MultiSelectField(choices=TERMS_CONDITIONS, unique=False, verbose_name="I will honor the Shop Newark Buy Local Rebate Program by processing Shop Newark rebates in the web portal on a weekly basis. By checking below you confirm and agree to all terms and conditions.")

    ##approved
    approved = models.CharField(choices=APPROVED_OPTIONS, default="No", verbose_name="Application Approved", max_length=3)

    def __str__(self):
        return self.company_name

    def get_absolute_url(self):
        return reverse('vendor-detail', kwargs={'pk': self.pk})