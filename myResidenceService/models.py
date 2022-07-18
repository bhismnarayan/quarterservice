from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from django import forms
import datetime
from django.contrib.auth.models import User
import logging
logger = logging.getLogger(__name__)

class Employee(models.Model):
    Empno = models.CharField(max_length=30)
    Name = models.CharField(max_length=100)
    Desig=models.CharField(max_length=30)
    PAN=models.CharField(max_length=30)

    def __str__(self):
       return self.Name


class Colony(models.Model):
    Colony_code = models.CharField(max_length=30)
    Col_name = models.CharField(max_length=30)
    Station=models.CharField(max_length=30)

    def __str__(self):
        return self.Col_name

class Quarter(models.Model):
    Qtr_ID = models.CharField(max_length=30)
    Colony_code = models.ForeignKey(Colony,on_delete=models.CASCADE)
    Qtr_no=models.CharField(max_length=30)
    Qtr_type=models.CharField(max_length=30)    

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
     
  

class SSE_Colony(models.Model):
    class Department(models.TextChoices):
        Civil = 'Civil', _('Civil')
        Electrical= 'Electrical', _('Electrical')
        Telnet= 'Telnet', _('Telnet')
         
    #Empno=models.ForeignKey(Employee,on_delete=models.CASCADE)
    Empno=models.CharField(max_length=60)
    Colony_code=models.CharField(max_length=750)
    Department=models.CharField(
        max_length=30,
        choices=Department.choices,
        null=True
    )
    groupName = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    active = models.BooleanField(verbose_name=_('active'), default=True)
    
    def __str__(self):
        if type(self.groupName)==None:
            return str(self.groupName)+self.Colony_code
        else:
            return str(self.groupName)#+self.Colony_code


def return_date_time():
    now = django.utils.timezone.now()
    return now

def increment_booking_number():
    try:
        last_booking = Complaint_details.objects.all().order_by('id').last()
        if not last_booking:
          return 'REQ' + str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '0000'
        booking_id = last_booking.Complaint_no
        booking_int = int(booking_id[9:13])
        new_booking_int = booking_int + 1
        new_booking_id = 'REQ' + str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_booking_int).zfill(4)
        return new_booking_id
    except Exception as e:
        logger.error(e)     



class Repair(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class RepairSubType(models.Model):
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Complaint_details(models.Model):
    
    class STATUS(models.TextChoices):
        CREATED = 'CREATED', _('Created')
        ASSIGNED= 'ASSIGNED', _('Assigned')
        INPROGRESS = 'INPROGRESS', _('In Progress')
        COMPLETED = 'COMPLETED', _('Completed')
        CLOSED = 'CLOSED', _('Closed')
        REOPENED = 'REOPENED', _('Reopen')

    Complaint_no =  models.CharField(max_length = 20, default = increment_booking_number, editable=False)
    Empno=models.ForeignKey(Employee,on_delete=models.CASCADE)
    Qtr=models.ForeignKey(Qtr_occupancy,on_delete=models.PROTECT, null=True)
    Repair_id=models.CharField(max_length=20,default=None, blank=True, null=True)
    Repair_type = models.ForeignKey(Repair, on_delete=models.SET_NULL, null=True)
    Repair_sub_type = models.ForeignKey(RepairSubType, on_delete=models.SET_NULL, null=True)
    
    Complaint_date=models.DateTimeField(auto_now_add=True)
    Complaint_detail=models.CharField(max_length=200)
    #Repair_type=models.CharField(
    #    max_length=15,
    #    choices=REPAIR_TYPE.choices, 
    #    default=REPAIR_TYPE.Select,      
    #)
    Service_status=models.CharField(
        max_length=10,
        choices=STATUS.choices,
        default=STATUS.CREATED,
    )
    Service_detail=models.CharField(max_length=20,blank=True)
    Reopend=models.IntegerField(blank=True,default=0)
    Service_date=models.DateTimeField(default=None, blank=True, null=True)    
    Currently_with=models.ForeignKey(SSE_Colony,default=None, blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.Complaint_no


    
