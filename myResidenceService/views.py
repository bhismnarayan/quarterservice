from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from .models import Colony, Complaint_details, Employee, Qtr_occupancy, Quarter,SSE_Colony,SimpleTable
from django.db.models import Q
from .forms import ComplaintForm,UploadFileForm,NewUserForm,UpdateComplaintForm
from django.contrib.auth.decorators import login_required
import pandas as pd
from .datainserter import UploadtoTable
from django.contrib.auth import login
from django.contrib import messages


def is_member(user):
    return user.groups.filter(name='Resolver').exists()

def getCurrentUserDetails(username):
    userdetail={}
    userdetail['user']=Employee.objects.filter(Empno= username).values()[0]
    qtr_id=Qtr_occupancy.objects.filter(Empno__Empno= username).values()[0]
    userdetail['qtr_occ']=qtr_id
    userdetail['qtr']=Quarter.objects.filter(id=qtr_id['Qtr_ID_id']).values()[0]    
    userdetail['colony']=Colony.objects.filter(id=userdetail['qtr']['Colony_code_id']).values()[0]
    return userdetail

@login_required
def index(request):
    userdetail={}
    try:
        userdetail=getCurrentUserDetails(request.user.username)
        
    except Exception as e:
        print(e)    
    latest_complaint_list={}
    member=False
    reopen=False
    if is_member(request.user):
        member=True            
        colonyList=SSE_Colony.objects.filter(Empno=userdetail['user']['Empno']).values('Colony_code')        
        colonycode_id_list = Colony.objects.filter(Colony_code__in=colonyList).values('id')        
        quarter = Quarter.objects.filter(Colony_code__in=colonycode_id_list).values('id')
        quarteroccupancy = Qtr_occupancy.objects.filter(Qtr_ID__in=quarter).values('id')        
        latest_complaint_list = Complaint_details.objects.filter(Qtr_id__in=quarteroccupancy and ~Q(Service_status = "CLOSED"))        
    else:    
        reopen=True
        latest_complaint_list = Complaint_details.objects.filter(Empno=userdetail['user']['id'] and ~Q(Service_status = "CLOSED") )        
    context = {'latest_complaint_list': latest_complaint_list,
              'userdetail':userdetail,'member':member,'reopen':reopen}            
    return render(request, 'myResidenceService/index.html', context)

def register_request(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()            
            if user!=None:
                login(request, user)
                messages.success(request, "Registration successful." )
                return redirect("/")
            else:                
                messages.error(request, "Unsuccessful registration. Invalid information.")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        
    return render (request=request, template_name="myResidenceService/register.html", context={"register_form":form})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        csv_file = request.FILES['sse_file'] #returns a dict-like object        
        try:
            UploadtoTable.fileHandler(csv_file,'sse')
            pass
        except Exception as e:
            print(e)
        try:
            csv_file = request.FILES['occupant_file']
            UploadtoTable.fileHandler(csv_file,'occupant_file')
        except Exception as e:
            print(e)    
        return render(request, 'myResidenceService/index.html')
    else:
        form = UploadFileForm()
    return render(request,'myResidenceService/upload_file.html', {'form': form})
   
        

@login_required
def services(request):
   latest_complaint_list = Complaint_details.objects.all()
   
   context = {'latest_complaint_list': latest_complaint_list}
   return render(request, 'myResidenceService/index.html', context)

@login_required
def newRequest(request):
    userdetails=getCurrentUserDetails(request.user.username)  
   
    form=ComplaintForm()
    form.fields['Empno'].initial = userdetails['user']['id']    
    form.fields['Qtr'].initial = userdetails['qtr_occ']['id']
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        form = ComplaintForm(request.POST)
        form.fields['Empno'].initial = userdetails['user']['id']    
        form.fields['Qtr'].initial = userdetails['qtr_occ']['id']
        if form.is_valid():
            form.save()           
            return HttpResponseRedirect('/')
        else:
            pass
        # check whether it's valid:
    context={'form':form}
    
    return render(request, 'myResidenceService/newServiceRequest.html',context)

@login_required
def close(request,Complaint_no):            
    Complaint_details.objects.filter(Complaint_no=Complaint_no).update(Service_status="CLOSED")
    return render(request, 'myResidenceService/thanks.html')

@login_required
def reopen(request,Complaint_no):        
    reopen_value=Complaint_details.objects.filter(Complaint_no=Complaint_no).values('Reopend')         
    Complaint_details.objects.filter(Complaint_no=Complaint_no).update(Reopend=int(reopen_value[0]['Reopend'])+1,Service_status="REOPENED")
    return render(request, 'myResidenceService/thanks.html')    

@login_required
def report(request):          
    latest_complaint_list = Complaint_details.objects.filter( ~Q(Service_status = "CLOSED"))    
    table = SimpleTable(latest_complaint_list)
    return render(request, "myResidenceService/report.html", {
        "table": table
    })         
    #return render(request, 'myResidenceService/report.html',context)    

@login_required
def myrequest(request):
    userdetail={}
    try:
        userdetail=getCurrentUserDetails(request.user.username)
        #print(userdetail)
    except Exception as e:
        print(e)    
    latest_complaint_list={}
    latest_complaint_list = Complaint_details.objects.filter(Empno=userdetail['user']['id'])
    
    context = {'latest_complaint_list': latest_complaint_list,
              'userdetail':userdetail}
    return render(request, 'myResidenceService/index.html', context)

def detail(request, Complaint_no):
    complaint_details = get_object_or_404(Complaint_details, Complaint_no=Complaint_no)    
    context= {'service': complaint_details}
    return render(request, 'myResidenceService/detail.html',context)


def update(request,Complaint_no):
    serviceDetail=Complaint_details.objects.get(Complaint_no=Complaint_no)
    form=UpdateComplaintForm(instance=serviceDetail)

    if request.method=='POST':
        form=UpdateComplaintForm(request.POST or None,instance=serviceDetail)
        if form.is_valid():
            form.save()            
            return HttpResponseRedirect('/')
        else:
            pass   
    context={ 'form':form}
    return render(request,'myResidenceService/updateService.html',context)
