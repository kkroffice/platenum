from django.db import models
import uuid
import datetime

class LicensePlate(models.Model):
    plate_number = models.CharField(max_length=20, unique=True, verbose_name="Plate Number")
    # owner
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.plate_number
    

    
class TrespassingEvent(models.Model):
    license_plate = models.ForeignKey(LicensePlate, on_delete=models.CASCADE, related_name="trespassing_events", verbose_name="License Plate")
    datetime_of_trespassing = models.DateTimeField(verbose_name="Datetime of Trespassing")
    location = models.CharField(max_length=255, verbose_name="Location")
    image_url = models.URLField(verbose_name="Image URL", blank=True)

    class Meta:
        verbose_name_plural = "Trespassing Events"

    def __str__(self):
        return f"Trespassing Event - {self.license_plate} - {self.datetime_of_trespassing}"


class Thread(models.Model):
    license_plate = models.ForeignKey(LicensePlate, on_delete=models.CASCADE, related_name="threads", verbose_name="License Plate")
    thread_info = models.TextField(verbose_name="Thread Information")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name_plural = "Threads"

    def __str__(self):
        return f"Thread - {self.license_plate}"

class ThreadImage(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="images", verbose_name="Thread")
    image_url = models.URLField(verbose_name="Image URL")

    def __str__(self):
        return f"Image for Thread - {self.thread}"


class AccessToken(models.Model):
    access_token = models.CharField(max_length=255, verbose_name="Access Token", default=uuid.uuid4)
    description = models.TextField(max_length=255, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "Access Tokens"