from django.contrib import admin
from .models import Address, Contact, Authorities, WorkflowStep, TrespassingLocation, AccessToken , Deal , Lawyer


admin.site.register(Deal)
admin.site.register(Lawyer)
admin.site.register(AccessToken)
admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Authorities)
admin.site.register(WorkflowStep)
admin.site.register(TrespassingLocation)
