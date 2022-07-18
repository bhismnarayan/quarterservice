from cmath import log
from django.forms import ModelForm
from django.forms.models import fields_for_model
from .models import Complaint_details,Employee,RepairSubType,Repair
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django import forms
import logging
logger = logging.getLogger(__name__)

class ComplaintForm(ModelForm):
    disabled_fields = ('Qtr','Empno')    

    class Meta:
        model= Complaint_details
        fields=['Empno','Qtr','Repair_type','Repair_sub_type','Complaint_detail','Currently_with']
    
    def __init__(self, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args, **kwargs)
        for field in self.disabled_fields:
            self.fields[field].disabled = True
        self.fields['Empno'].label = "Employee Name"
        self.fields['Repair_sub_type'].queryset = RepairSubType.objects.none() 
        logger.error(self.data.get('Repair_type'))
        if 'Repair_type' in self.data:
            logger.error("if!!")    
            try:
                id = int(self.data.get('Repair_type'))                
                self.fields['Repair_sub_type'].queryset = RepairSubType.objects.filter(repair_id=id).order_by('name')
            except Exception as e:
                logger.error(e)  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:            
            self.fields['Repair_sub_type'].queryset = self.instance.Repair.RepairSubType_set.order_by('name')
    #class Media:
    #    js = ('book_form.js', )

    #def clean(self):
    #    if self.cleaned_data['Repair_type'] is None:
    #        raise ValidationError('You should indicate the sequel if the book has one.')    

class UpdateComplaintForm(ModelForm):   
    disabled_fields = ('Qtr','Empno','Complaint_detail')
    
    class Meta:
        model= Complaint_details
        fields=['Empno','Qtr','Repair_type','Complaint_detail','Service_status','Service_detail','Currently_with']
    
    def __init__(self, *args, **kwargs):
        super(UpdateComplaintForm, self).__init__(*args, **kwargs)
        for field in self.disabled_fields:
            self.fields[field].disabled = True
    #class Media:
    #    js = ('book_form.js', )

    #def clean(self):
    #    if self.cleaned_data['Repair_type'] is None:
    #        raise ValidationError('You should indicate the sequel if the book has one.')    


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()  

class NewUserForm(UserCreationForm):
    PAN = forms.CharField(max_length=10,min_length=10,required=True)

    class Meta:
        model = User
        fields = ("username", "PAN", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.PAN = self.cleaned_data['PAN']        
        data = Employee.objects.filter(PAN=user.PAN ,Empno=user.username)
        
        
        if data.count!=0:
            if commit:
                user.save()
            return user
        else:
            return None    
