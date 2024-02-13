from django.contrib import admin
from .models import Address, Contact, Authorities, WorkflowStep, TrespassingLocation, AccessToken

admin.site.register(AccessToken)
admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Authorities)
admin.site.register(WorkflowStep)
admin.site.register(TrespassingLocation)
