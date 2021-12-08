from django.urls import path
from . import views

app_name = 'myResidenceService'

urlpatterns = [
    path('', views.index, name='index'),    
    path('newRequest', views.newRequest, name='newRequest'),    
    path('upload_file', views.upload_file, name='upload_file'),    
    path('<int:Complaint_no>/', views.detail, name='detail'),    
    path("register", views.register_request, name="register"),
    path('myrequest', views.myrequest, name='myrequest'),    
    path('<int:Complaint_no>/update/', views.update, name='update'),
]
