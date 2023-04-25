
## _Installation process_

App helps with complaint registration
AngularJS-powered HTML5 Markdown editor.


## Features
Install postgreSQL by following the link
https://sbp.enterprisedb.com/getfile.jsp?fileid=1258422

###Installing git on Windows 
https://git-scm.com/download/win

Installing git on Linux
'''
sudo yum install git  -y
'''
Install python  by following below link -

https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe

make sure you check the add to path 

https://pip.pypa.io/en/stable/installation/

### Getting source code on machine :- create directory where you want to keep you the source code 
'''
git clone https://github.com/bhismnarayan/quarterservice.git
'''

###  Then navaigate to and use to pip to install packages using requirements.txt

```
cd  quarterservice
pip install psycopg2-binary pandas django psycopg2 django-crispy-forms crispy-bootstrap4

```

### Running the application
```
python manage.py migrate
python manage.py runserver 0.0.0.0:80 &
```

# quarterservice

- Create group Resolver,Officer 
- create data for repair and repairsubtype
- INSERT INTO public."myResidenceService_repair"(	id, name)	VALUES (1, 'Civil');
- INSERT INTO public."myResidenceService_repair"(	id, name)	VALUES (2, 'Electrical');
- INSERT INTO public."myResidenceService_repair"(	id, name)	VALUES (3, 'Telnet');

INSERT INTO public."myResidenceService_repairsubtype"(id, name, repair_id)
	VALUES (1, 'Roof Leakeage', 1);
INSERT INTO public."myResidenceService_repairsubtype"(id, name, repair_id)
	VALUES (2, 'Electrical issue', 2);
INSERT INTO public."myResidenceService_repairsubtype"(id, name, repair_id)
	VALUES (3, 'Telnet', 3);
		

###Separate department for telephone and internet
	
- create admin account
- - python manage.py createsuperuser


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