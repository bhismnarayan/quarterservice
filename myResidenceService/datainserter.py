import pandas as pd
from .models import SSE_Colony,Employee,Colony,Quarter,Qtr_occupancy
from django.contrib.auth.models import User
import logging
logger = logging.getLogger(__name__)
class UploadtoTable:
    def SSETableInserter(df):
        try:            
            for ind in df.index:
                try:
                    user = User.objects.create_user(username=df['GroupName'][ind],                                 
                                 password='Mango12$')
                except Exception as e:
                    logger.error("Error creating user",user)
        except Exception as e:
            logger.error(e)    
        
        SSE_Colony_data = [
             SSE_Colony(
                Colony_code = df.iloc[i, 2], 
                Department=df.iloc[i, 3],
                groupName=User.objects.get(username= df.iloc[i, 0]),                      
                active=df.iloc[i, 4], 
                Empno= df.iloc[i, 1],#Employee.objects.get(Empno= df.iloc[i, 2]),                      
                )           
                  for i in range(len(df))]
        SSE_Colony.objects.all().delete()
        SSE_Colony.objects.bulk_create(SSE_Colony_data)

    
    def EmployeeInserter(df):
        df=df.drop_duplicates(subset=['EMPNO']).copy()
        logger.error("Employee Data insertion")
        Employee_data = [
            Employee(
                Name = df.iloc[i, 4], 
                Empno = df.iloc[i, 3],
                Desig = df.iloc[i, 5], 
                PAN = df.iloc[i,6 ],                      
                )           
                  for i in range(len(df))]
        Employee.objects.all().delete()
        Employee.objects.bulk_create(Employee_data)

    def ColonyInserter(df):
        col_df=df.drop_duplicates(subset=['COLONYCODE']).copy()
        Colony.objects.all().delete()                        
        Colony_data=[
                Colony(
                Colony_code = col_df.iloc[i, 0], 
                Col_name = col_df.iloc[i,1],
                Station = col_df.iloc[i, 2],                                      
                )           
                  for i in range(len(col_df))]
        Colony.objects.bulk_create(Colony_data)          

    def QuarterOccupancyInserter(df):
        df["OCC_DT"] = pd.to_datetime(df['OCC_DT']).dt.date  
        Quarter_occ_data=[                
            Qtr_occupancy(
                Qtr_ID =Quarter.objects.get(Qtr_ID= df.iloc[i, 7]), 
                Empno = Employee.objects.get(Empno=df.iloc[i,3]),
                Occ_dt = df.iloc[i, 10]        
                                                    
                )           
                  for i in range(len(df))
                     
                  ]
        Qtr_occupancy.objects.all().delete() 
        
        Qtr_occupancy.objects.bulk_create(Quarter_occ_data)           

    def QuarterInserter(df):
        Quarter_data=[
                
                Quarter(
                Qtr_ID = df.iloc[i, 7], 
                Colony_code = Colony.objects.get(Colony_code=df.iloc[i,0]),
                Qtr_no = df.iloc[i, 8],
                Qtr_type=df.iloc[i,9]                                      
                )           
                  for i in range(len(df))]
        Quarter.objects.all().delete() 
        Quarter.objects.bulk_create(Quarter_data)           
        
      
    def fileHandler(csv_file,filename):
        df=pd.read_csv(csv_file,sep=',')
        if filename=='sse':
            # try:
            #   pass  
            #   #UploadtoTable.SecInchargeInserter(df)
              
            # except Exception as e:
            #   logger.error("Sec Incharge Inserter Failed ",e)    
                 
            try:
                
                UploadtoTable.SSETableInserter(df)                
            except Exception as e:
                logger.error("SSE inserter failed ",e)  

            
        else:
            try:
              UploadtoTable.EmployeeInserter(df)  
            except Exception as e:
                logger.error("Employee Inserter Failed ",e)
            
            try:
                UploadtoTable.ColonyInserter(df)
            except Exception as e:
                logger.error("Colony Inserter Failed ",e)
            
            try:
                 UploadtoTable.QuarterInserter(df)
            except Exception as e:
                logger.error("Quarter Inserter Failed ",e)

            try:
                 UploadtoTable.QuarterOccupancyInserter(df)
            except Exception as e:
                logger.error("Quarter occupancy Inserter Failed ",e)    
                
            
            
    
