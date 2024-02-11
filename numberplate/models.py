from django.db import models
import uuid
from django.utils import timezone

class Deal(models.Model):
    deal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Deal ID")
    trespassing_location = models.ForeignKey('TrespassingLocation', on_delete=models.CASCADE, verbose_name="Trespassing Location")
    plate_number = models.ForeignKey('TrespassingEvent', on_delete=models.CASCADE, related_name="related_deals", verbose_name="Trespassing Event")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    workflow_step = models.ForeignKey('WorkflowStep', on_delete=models.CASCADE, verbose_name="Workflow Step", blank=True, null=True, default=None)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return str(self.plate_number)


class TrespassingEvent(models.Model):
    trespassing_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Trespassing ID")
    trespassing_event = models.CharField(max_length=255, verbose_name="Trespassing Event")
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="trespassing_events", verbose_name="Deal")
    datetime_of_trespassing = models.DateTimeField(verbose_name="Datetime of Trespassing", )
    trespassing_location = models.ForeignKey('TrespassingLocation', on_delete=models.CASCADE, verbose_name="Trespassing Location")
    image_url = models.URLField(verbose_name="Image URL", blank=True)
    trespassing_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Trespassing Datetime")

    class Meta:
        verbose_name_plural = "Trespassing Events"

    def __str__(self):
        return f"Trespassing Event - {self.deal} - {self.datetime_of_trespassing}"

class TrespassingLocation(models.Model):
    trespassing_location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Trespassing Location ID")
    customer_name = models.CharField(max_length=255, verbose_name="Customer Name")
    location_owner = models.ForeignKey('Contact', on_delete=models.CASCADE, verbose_name="Location Owner")
    location_address = models.OneToOneField('Address', on_delete=models.CASCADE, verbose_name="Location Address")
    doc_poa_lawyer_id = models.CharField(max_length=255, verbose_name="POA Lawyer ID", blank=True, null=True, default=None)
    doc_poa_kkr_id = models.CharField(max_length=255, verbose_name="POA KKR ID", blank=True, null=True, default=None)
    doc_kkr_order_id = models.CharField(max_length=255, verbose_name="KKR Order ID", blank=True, null=True, default=None)
    location_shortname = models.CharField(max_length=32, unique=True, blank=True, default=None)

    def __str__(self):
        return self.customer_name

class Contact(models.Model):
    contact_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Contact ID")
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    address = models.OneToOneField('Address', on_delete=models.CASCADE, verbose_name="Address", default=None)
    birth_date = models.DateField(verbose_name="Birth Date", )
    email = models.EmailField(verbose_name="Email")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    company_name = models.CharField(max_length=255, verbose_name="Company Name", blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Address(models.Model):
    address_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Address ID")
    zip_code = models.CharField(max_length=20, verbose_name="Zip Code")
    city = models.CharField(max_length=100, verbose_name="City")
    street_name = models.CharField(max_length=255, verbose_name="Street Name")
    street_number = models.CharField(max_length=10, verbose_name="Street Number")
    country = models.CharField(max_length=100, verbose_name="Country")

    def __str__(self):
        return f"{self.street_number} {self.street_name}, {self.city}, {self.country}"

class WorkflowStep(models.Model):
    step_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Step ID")
    name_of_step = models.CharField(max_length=100, verbose_name="Name of Step")
    start_date = models.DateTimeField(verbose_name="Start Date", )
    end_date = models.DateTimeField(verbose_name="End Date", )

    def __str__(self):
        return self.name_of_step

class Thread(models.Model):
    license_plate = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="threads", verbose_name="License Plate")
    thread_info = models.TextField(verbose_name="Thread Information")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At", )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At", )

    class Meta:
        verbose_name_plural = "Threads"

    def __str__(self):
        return f"Thread - {self.license_plate}"

class ThreadImage(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="images", verbose_name="Thread")
    image_url = models.URLField(verbose_name="Image URL")

    def __str__(self):
        return f"Image for Thread - {self.thread}"

class LicencePlates(models.Model):
    license_plate = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="licence_plates", verbose_name="License Plate")
    responsible_authorities = models.ManyToManyField('Authorities', verbose_name="Responsible Authorities")

    def __str__(self):
        return f"{self.license_plate}"

class Authorities(models.Model):
    authority_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Authority ID")
    name = models.CharField(max_length=255, verbose_name="Authority Name")
    authority_iban = models.CharField(max_length=255, verbose_name="IBAN")
    authority_bic = models.CharField(max_length=255, verbose_name="BIC")
    authority_pipedrive_id = models.CharField(max_length=255, verbose_name="Pipedrive ID")
    authority_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="authorities_address", verbose_name="Address", default=None)

    def __str__(self):
        return self.name

class AccessToken(models.Model):
    access_token_id = models.AutoField(primary_key=True, verbose_name='Access Token ID')
    access_token = models.CharField(max_length=255, verbose_name="Access Token", default=uuid.uuid4)
    description = models.TextField(max_length=255, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "Access Tokens"
