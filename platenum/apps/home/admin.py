from django.contrib import admin
from .models import Address, Contact, Authorities, WorkflowStep, TrespassingLocation, AccessToken, Deal, Lawyer, Thread, ThreadImage, LicencePlate

class DealAdmin(admin.ModelAdmin):
    list_display = ('deal_id', 'trespassing_location', 'license_plate_uuid', 'lawyer', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Authorities)
admin.site.register(WorkflowStep)
admin.site.register(TrespassingLocation)
admin.site.register(AccessToken)
admin.site.register(Lawyer)
admin.site.register(Thread)
admin.site.register(ThreadImage)
admin.site.register(LicencePlate)
admin.site.register(Deal, DealAdmin)
