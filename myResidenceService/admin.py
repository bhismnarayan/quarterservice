# Register your models here.
from django.contrib import admin

from .models import Employee,Complaint_details,Quarter,Colony,SSE_Colony,Qtr_occupancy


admin.site.register(Quarter)
admin.site.register(Employee)
admin.site.register(Colony)
admin.site.register(Complaint_details)
admin.site.register(SSE_Colony)
admin.site.register(Qtr_occupancy)

