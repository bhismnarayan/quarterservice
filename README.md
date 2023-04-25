# _Installation process_

## Software installation 

 1. Install postgreSQL by downloading executable for windowsfrom  and do not change the default port number and keep the password safe which be used in django setting- https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
 2. Install git  by downloading 64 bit executable from -https://git-scm.com/download/win  
     Installing git on Linux
     ```
     sudo yum install git  -y
    ```
 3. Install python  by getting exe from  -https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe
make sure you check the add to path 


## Application Configuration

###  Getting source code on machine  and installing python packages

 1. create directory where you want to keep you the source code ,open git bash  navigate into it and execute below command to clone repository
 ```                                                             

    git clone https://github.com/bhismnarayan/quarterservice.git
```
 2. navaigate to quarterservice folder and use pip to install python packages .Excecute below command in git bash


```
py -m venv quarterservice
cd  quarterservice
\Scripts\activate
pip install psycopg2-binary pandas django psycopg2 django-crispy-forms crispy-bootstrap4

```

## Configuring  and  running the application

 1. Run below command to create table into the database be sure to update the  database password at QuarterServiceNow\settings.py 

```
python manage.py migrate
```
2.  Start the django application

```												                     
 python manage.py runserver 0.0.0.0:8080 &
```
3.  Navigate  to  localhost/myResidenceService/uploaddata and use 
select sse.csv and occupant data.csv for each of the file selector and click upload which would upload the data and get database filled with prerequisite record
4. create admin account
```
     python manage.py createsuperuser
```
- Create group Resolver,Officer if not created by doing admin login on locahost:portnumber/admin

- create data for repair and repairsubtype
```
 INSERT INTO public."myResidenceService_repair"(	id, name)	VALUES (1, 'Civil');
 INSERT INTO public."myResidenceService_repair"(	id, name)	VALUES (2, 'Electrical');
 INSERT INTO public."myResidenceService_repair"(	id, name)	VALUES (3, 'Telnet');

INSERT INTO public."myResidenceService_repairsubtype"(id, name, repair_id)
	VALUES (1, 'Roof Leakeage', 1);
INSERT INTO public."myResidenceService_repairsubtype"(id, name, repair_id)
	VALUES (2, 'Electrical issue', 2);
INSERT INTO public."myResidenceService_repairsubtype"(id, name, repair_id)
	VALUES (3, 'Telnet', 3);
```		

###Separate department for telephone and internet


##Flow
- create group with
- update the database table with occupant data and sse data
- 
###
- Register with the username as EMPID and PANcard and create password
- create a request to for compaints

Resolver-
 500001_07_Civil
 500001_07_Electrical
 500001_54_TelNet