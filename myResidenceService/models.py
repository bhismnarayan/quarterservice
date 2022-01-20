from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from django import forms
import datetime

def return_date_time():
    now = django.utils.timezone.now()
    return now

def increment_booking_number():
      last_booking = Complaint_details.objects.all().order_by('id').last()      
      if not last_booking:
          return 'REQ' + str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '0000'
      booking_id = last_booking.Complaint_no
      booking_int = int(booking_id[9:13])
      new_booking_int = booking_int + 1
      new_booking_id = 'REQ' + str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_booking_int).zfill(4)
      return new_booking_id

class Employee(models.Model):
    Empno = models.CharField(max_length=20)
    Name = models.CharField(max_length=100)
    Desig=models.CharField(max_length=20)
    PAN=models.CharField(max_length=20)

    def __str__(self):
       return self.Name


class Colony(models.Model):
    Colony_code = models.CharField(max_length=20)
    Col_name = models.CharField(max_length=20)
    Station=models.CharField(max_length=20)

    def __str__(self):
        return self.Col_name

class Quarter(models.Model):
    Qtr_ID = models.CharField(max_length=20)
    Colony_code = models.ForeignKey(Colony,on_delete=models.CASCADE)
    Qtr_no=models.CharField(max_length=20)
    Qtr_type=models.CharField(max_length=20)    

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.Qtr_no}, {self.Qtr_type},{self.Colony_code}'
    

class Qtr_occupancy(models.Model):
    Qtr_ID = models.ForeignKey(Quarter,on_delete=models.CASCADE)
    Empno = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Occ_dt=models.DateField(default=None, blank=True, null=True)
    Vac_dt=models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.Qtr_ID}'
     
  
class Sec_incharge(models.Model):
    Empno=models.CharField(max_length=20)
    Name=models.CharField(max_length=100)
    Desig=models.CharField(max_length=100)
    Level=models.CharField(max_length=100,blank=True)
    Eng_ele=models.CharField(max_length=100,blank=True)
    PAN=models.CharField(max_length=11,blank=True)
    
    def __str__(self):
        return self.Name

class SSE_Colony(models.Model):
    #Empno=models.ForeignKey(Sec_incharge,on_delete=models.CASCADE)
    Empno=models.CharField(max_length=20)
    Colony_code=models.CharField(max_length=20)    
    


class Complaint_details(models.Model):
    
    class STATUS(models.TextChoices):
        CREATED = 'CREATED', _('Created')
        ASSIGNED= 'ASSIGNED', _('Assigned')
        INPROGRESS = 'INPROGRESS', _('In Progress')
        COMPLETED = 'COMPLETED', _('Completed')
        CLOSED = 'CLOSED', _('Closed')
        REOPENED = 'REOPENED', _('Reopen')

    class REPAIR_TYPE(models.TextChoices):
        Select = 'Select', _('Select')
        ROOFLEAKAGE = 'ROOF LEAKAGE', _('Roof Leakeage')
        MASONARY= 'Masonary', _('Masonary Work/Floor Plastering')
        PIPELINE = 'Pipeline', _('Pipeline/Sanitary')
        WATER = 'Water', _('Water Supply') 
        CARPENTARY = 'CARPENTARY', _('carpentary(Doors/Windows)') 
        DRAINS = 'DRAINS', _('Drains')         
        OTHERS = 'OTHERS', _('Other')    
    id =  models.AutoField(primary_key=True)
    Complaint_no =  models.CharField(max_length = 20, default = increment_booking_number, editable=False)

   
    Empno=models.ForeignKey(Employee,on_delete=models.CASCADE)
    Qtr=models.ForeignKey(Qtr_occupancy,on_delete=models.PROTECT, null=True)
    Repair_id=models.CharField(max_length=20,default=None, blank=True, null=True)
    Complaint_date=models.DateTimeField(auto_now_add=True)
    Complaint_detail=models.CharField(max_length=200)
    Repair_type=models.CharField(
        max_length=15,
        choices=REPAIR_TYPE.choices, 
        default=REPAIR_TYPE.Select,      
    )
    Service_status=models.CharField(
        max_length=10,
        choices=STATUS.choices,
        default=STATUS.CREATED,
    )
    Service_detail=models.CharField(max_length=20,blank=True)
    Reopend=models.IntegerField(blank=True,default=0)
    Service_date=models.DateTimeField(default=None, blank=True, null=True)    
    Currently_with=models.ForeignKey(Sec_incharge,default=None, blank=True, null=True,on_delete=models.CASCADE)

    

import django_tables2 as tables

class SimpleTable(tables.Table):
    class Meta:
        model = Complaint_details     


    
