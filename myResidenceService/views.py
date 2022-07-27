from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from .models import Colony, Complaint_details, Employee, Qtr_occupancy, Quarter,SSE_Colony,Repair,RepairSubType
from django.db.models import Q,Count   
from .forms import ComplaintForm,UploadFileForm,NewUserForm,UpdateComplaintForm
from django.contrib.auth.decorators import login_required
import pandas as pd
from .datainserter import UploadtoTable
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
import logging
logger = logging.getLogger(__name__)


def memberGroup(user):
    if user.groups.filter(name='Resolver').exists():
        return 'Resolver'
    elif user.groups.filter(name='Officer').exists():
        return 'Officer'
    else:
        return ''    

def getCurrentUserDetails(username):
    userdetail={}
    try: 
        userdetail['user']=Employee.objects.filter(Empno= username).values()[0]
        qtr_id=Qtr_occupancy.objects.filter(Empno__Empno= username).values()[0]
        userdetail['qtr_occ']=qtr_id
        userdetail['qtr']=Quarter.objects.filter(id=qtr_id['Qtr_ID_id']).values()[0]    
        userdetail['colony']=Colony.objects.filter(id=userdetail['qtr']['Colony_code_id']).values()[0]
    except Exception as e:
        logger.error("Error getting detail for ",username,"Error-",e)
        
    return userdetail

@login_required
def index(request):
    
    latest_complaint_list={}
    member=False
    reopen=False
    if memberGroup(request.user)=='Resolver':
        member=True            
        colonyList=SSE_Colony.objects.filter(groupName=request.user.id).values('id')
              
        latest_complaint_list = Complaint_details.objects.filter( ~Q(Service_status = "CLOSED")).filter(Currently_with_id=colonyList[0]['id']) #and ~Q(Service_status = "CLOSED"))
        logger.error(latest_complaint_list)
        context = {'latest_complaint_list': latest_complaint_list,'member':member,'reopen':False}       
        return render(request, 'myResidenceService/resolver.html', context)

    elif memberGroup(request.user)=='Officer':        
        latest_complaint_list={}
        response=officerReport(request)
        return HttpResponse(response)
    else:  
        userdetail={}
        try:
            userdetail=getCurrentUserDetails(request.user.username)
        
        except Exception as e:
            logger.error(e)     
        reopen=True
        try:
            latest_complaint_list = Complaint_details.objects.filter( ~Q(Service_status = "CLOSED")).filter(Empno=userdetail['user']['id'] ).order_by('-Complaint_date')#and ~Q(Service_status = "CLOSED") )        
        except Exception as e:
            logger.error(e)    
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
            logger.error(e)
        try:
            csv_file = request.FILES['occupant_file']
            UploadtoTable.fileHandler(csv_file,'occupant_file')
        except Exception as e:
            logger.error(e)    
        return render(request, 'myResidenceService/index.html')
    else:
        form = UploadFileForm()
    return render(request,'myResidenceService/upload_file.html', {'form': form})
   
        

@login_required
def services(request):
   latest_complaint_list = Complaint_details.objects.all()
   
   context = {'latest_complaint_list': latest_complaint_list}
   return render(request, 'myResidenceService/index.html', context)


#Create new request
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
        
        result = SSE_Colony.objects.filter(Colony_code__contains=userdetails['colony']['Colony_code']).filter(Department=Repair.objects.filter(id=int(request.POST.get('Repair_type'))).values('name')[0]['name']).values('id')
        logger.error(result)
        #groupName=userdetails['colony']['Colony_code']+Repair.objects.filter(id=int(request.POST.get('Repair_type'))).values('name')[0]['name']
        #userid = User.objects.filter(username=groupName).values('id')
        assignee=result[0]['id']
        #userid[0]['id']).values('id')
        form.fields['Currently_with'].initial = assignee

        if form.is_valid():         
            obj = form.save(commit=False)
            obj.Currently_with_id= assignee
            obj.save()
            #form.save()           
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
    colonyList=SSE_Colony.objects.filter(groupName=request.user.id).values('id')        
    latest_complaint_list = Complaint_details.objects.filter( ~Q(Service_status = "CLOSED")).filter(Currently_with_id=colonyList[0]['id']) #and ~Q(Service_status = "CLOSED")) 
             
    closedComplaintList = Complaint_details.objects.all().order_by('Repair_type').filter(Service_status = "CLOSED").filter(Currently_with=colonyList[0]['id'])
    openComplaint = {}
    # (Complaint_details.objects
    # .values('Currently_with','Currently_with')    
    # .filter( ~Q(Service_status = "CLOSED")) 
    # .filter(Currently_with_id=colonyList[0]['id'])   
    # .order_by('Currently_with_id')
    # .annotate(dcount=Count('Currently_with_id'))    
    # )   
    context = {'latest_complaint_list': latest_complaint_list,
    'closedComplaint':closedComplaintList,
    'openComplaint':openComplaint} 
    return render(request, 'myResidenceService/report.html',context)    

@login_required
def officerReport(request):  
    latest_complaint_list = Complaint_details.objects.filter( ~Q(Service_status = "CLOSED"))    
    closedComplaintList = Complaint_details.objects.all().order_by('Repair_type').filter(Service_status = "CLOSED")
    openComplaint = (Complaint_details.objects
    #.values('Currently_with')
    #.values('Currently_with_id','Currently_with')
    
    .filter( ~Q(Service_status = "CLOSED"))    
    .annotate(dcount=Count('Currently_with_id'))
    .order_by('Currently_with')
    )
 
    context = {'latest_complaint_list': latest_complaint_list,
    'closedComplaint':closedComplaintList,
    'openComplaint':openComplaint} 
    return render(request, 'myResidenceService/officerreport.html',context)    

@login_required
def myrequest(request):
    userdetail={}
    try:
        userdetail=getCurrentUserDetails(request.user.username)        
    except Exception as e:
        logger.error(e)    
    latest_complaint_list={}
    latest_complaint_list = Complaint_details.objects.filter(Empno=userdetail['user']['id'])
    
    context = {'latest_complaint_list': latest_complaint_list,
              'userdetail':userdetail}
    return render(request, 'myResidenceService/index.html', context)

@login_required
def detail(request, Complaint_no):
    complaint_details = get_object_or_404(Complaint_details, Complaint_no=Complaint_no)    
    context= {'service': complaint_details}
    return render(request, 'myResidenceService/detail.html',context)

@login_required
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
    return render(request,'myResidenceService/editService.html',context)

def load_repairSubType(request):
    
    repair_id = request.GET['Repair']
    
    #logger.info("Repair",repair_id)
    repairSubTypes = RepairSubType.objects.filter(repair_id=repair_id).order_by('name')
    logger.error(repairSubTypes)
    return render(request, 'myResidenceService/repairSubtype_dropdown_list_options.html', {'repairSubTypes': repairSubTypes})