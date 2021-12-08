from django.forms import ModelForm

from django.forms.models import fields_for_model
from .models import Complaint_details,Employee,Sec_incharge
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django import forms

class ComplaintForm(ModelForm):
    disabled_fields = ('Qtr','Empno')    

    class Meta:
        model= Complaint_details
        fields=['Empno','Qtr','Repair_type','Complaint_detail']
    
    def __init__(self, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args, **kwargs)
        for field in self.disabled_fields:
            self.fields[field].disabled = True
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
        print(user)
        data = Employee.objects.filter(PAN=user.PAN ,Empno=user.username)
        secuser=Sec_incharge.objects.filter(Empno=user.username)
        if secuser.count==1:
            my_group = Group.objects.get(name='Resolver') 
            my_group.user_set.add(user)

        print(data.count)
        if data.count!=0:
            if commit:
                user.save()
            return user
        else:
            return None    
