# quarterservice
Required packages to be installed
django
psycopg2
Create group Resolver,Officer 
create data for repair and repairsubtype
INSERT INTO public."myResidenceService_repair"(	id, name)	VALUES (1, 'Civil Engg.');
INSERT INTO public."myResidenceService_repair"(	id, name)	VALUES (2, 'Electrical');
INSERT INTO public."myResidenceService_repair"(	id, name)	VALUES (3, 'Telephone');
INSERT INTO public."myResidenceService_repair"(	id, name)	VALUES (4, 'Internet');

INSERT INTO public."myResidenceService_repairsubtype"(id, name, repair_id)
	VALUES (1, 'Roof Leakeage', 1);

Todo
	#Separate department for telephone and internet