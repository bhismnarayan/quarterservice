from django.urls import path
from . import views

app_name = 'myResidenceService'

urlpatterns = [
    path('', views.index, name='index'),    
    path('newRequest', views.newRequest, name='newRequest'),
    path('report', views.report, name='report'),    
    path('upload_file', views.upload_file, name='upload_file'),    
    path('<str:Complaint_no>/', views.detail, name='detail'),    
    path("register", views.register_request, name="register"),
    path('myrequest', views.myrequest, name='myrequest'), 
    path('<str:Complaint_no>/close/', views.close, name='close'), 
    path('<str:Complaint_no>/reopen/', views.reopen, name='reopen'),    
    path('<str:Complaint_no>/update/', views.update, name='update'),
]
