
## _Installation process_

App helps with complaint registration
AngularJS-powered HTML5 Markdown editor.


## Features
'''
sudo yum install git  -y
git clone https://github.com/bhismnarayan/quarterservice.git
cd  quarterservice
pip3 install 
pip install psycopg2-binary pandas
'''
- change ip address in machine in setting file
- python3 manage.py runserver 0.0.0.0:80 &
 
# quarterservice
##Required packages to be installed
-django
-psycopg2
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