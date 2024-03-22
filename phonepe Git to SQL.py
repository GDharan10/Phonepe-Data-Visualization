import pandas as pd
import json
import os
import psycopg2

from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:1005@localhost/phonepay')



#1 aggregated/transaction
path="C:/GD/Notes/DS Class/DTM15/Project/Phonepe project/github/pulse/data/aggregated/transaction/country/india/state/"
state_list=os.listdir(path)

agg_trans_clm={'States':[], 'Years':[],'Quater':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}

for state in state_list:
    p_s=path+state+"/"
    years_list=os.listdir(p_s)
    for year in years_list:
        p_y=p_s+year+"/"
        quater_list=os.listdir(p_y)
        for quater in quater_list:
            p_q=p_y+quater
            Data=open(p_q,'r')
            D=json.load(Data)
            for i in D['data']['transactionData']:
              Name=i['name']
              count=i['paymentInstruments'][0]['count']
              amount=i['paymentInstruments'][0]['amount']
              agg_trans_clm['Transaction_type'].append(Name)
              agg_trans_clm['Transaction_count'].append(count)
              agg_trans_clm['Transaction_amount'].append(amount)
              agg_trans_clm['States'].append(state)
              agg_trans_clm['Years'].append(year)
              agg_trans_clm['Quater'].append(int(quater.strip('.json')))

agg_trans=pd.DataFrame(agg_trans_clm)

agg_trans['States']=agg_trans['States'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
agg_trans['States']=agg_trans['States'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
agg_trans['States']=agg_trans['States'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
agg_trans['States']=agg_trans['States'].str.replace("-"," ")
agg_trans['States']=agg_trans['States'].str.title()



#2 aggregated/user
path="C:/GD/Notes/DS Class/DTM15/Project/Phonepe project/github/pulse/data/aggregated/user/country/india/state/"
state_list=os.listdir(path)

agg_user_clm={'States':[], 'Years':[],'Quater':[],'Brands':[], 'Reg_user_count':[], 'Reg_percentage':[]}

for state in state_list:
    p_s=path+state+"/"
    years_list=os.listdir(p_s)
    for year in years_list:
        p_y=p_s+year+"/"
        quater_list=os.listdir(p_y)
        for quater in quater_list:
            p_q=p_y+quater
            Data=open(p_q,'r')
            D=json.load(Data)
            try:
                for i in D['data']['usersByDevice']:
                    Brand=i['brand']
                    count=i['count']
                    percentage=i['percentage']
                    agg_user_clm['Brands'].append(Brand)
                    agg_user_clm['Reg_user_count'].append(count)
                    agg_user_clm['Reg_percentage'].append(percentage)
                    agg_user_clm['States'].append(state)
                    agg_user_clm['Years'].append(year)
                    agg_user_clm['Quater'].append(int(quater.strip('.json')))
            except:
                pass

agg_users=pd.DataFrame(agg_user_clm)

agg_users['States']=agg_users['States'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
agg_users['States']=agg_users['States'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
agg_users['States']=agg_users['States'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
agg_users['States']=agg_users['States'].str.replace("-"," ")
agg_users['States']=agg_users['States'].str.title()



#3 map/transaction
path="C:/GD/Notes/DS Class/DTM15/Project/Phonepe project/github/pulse/data/map/transaction/hover/country/india/state/"
state_list=os.listdir(path)


map_trans_clm={'States':[], 'Years':[],'Quater':[],'District_name':[], 'Transaction_count':[], 'Transaction_amount':[]}

for state in state_list:
    p_s=path+state+"/"
    years_list=os.listdir(p_s)
    for year in years_list:
        p_y=p_s+year+"/"
        quater_list=os.listdir(p_y)
        for quater in quater_list:
            p_q=p_y+quater
            Data=open(p_q,'r')
            D=json.load(Data)
            try:
              for i in D['data']['hoverDataList']:
                Name=i['name']
                count=i['metric'][0]['count']
                amount=i['metric'][0]['amount']
                map_trans_clm['District_name'].append(Name)
                map_trans_clm['Transaction_count'].append(count)
                map_trans_clm['Transaction_amount'].append(amount)
                map_trans_clm['States'].append(state)
                map_trans_clm['Years'].append(year)
                map_trans_clm['Quater'].append(int(quater.strip('.json')))
            except Exception as e:
              print(f"Error processing file '{p_q}': {e}")

map_trans=pd.DataFrame(map_trans_clm)

map_trans['States']=map_trans['States'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
map_trans['States']=map_trans['States'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
map_trans['States']=map_trans['States'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
map_trans['States']=map_trans['States'].str.replace("-"," ")
map_trans['States']=map_trans['States'].str.title()



#4 map/User
path="C:/GD/Notes/DS Class/DTM15/Project/Phonepe project/github/pulse/data/map/user/hover/country/india/state/"
state_list=os.listdir(path)

map_User_clm={'States':[], 'Years':[],'Quater':[],'District_name':[], 'Reg_users':[], 'App_opens':[]}

for state in state_list:
    p_s=path+state+"/"
    years_list=os.listdir(p_s)
    for year in years_list:
        p_y=p_s+year+"/"
        quater_list=os.listdir(p_y)
        for quater in quater_list:
            p_q=p_y+quater
            Data=open(p_q,'r')
            D=json.load(Data)
            for i in D['data']['hoverData'].items():
              district=i[0]
              regusers=i[1]['registeredUsers']
              appopens=i[1]['appOpens']
              map_User_clm['District_name'].append(district)
              map_User_clm['Reg_users'].append(regusers)
              map_User_clm['App_opens'].append(appopens)
              map_User_clm['States'].append(state)
              map_User_clm['Years'].append(year)
              map_User_clm['Quater'].append(int(quater.strip('.json')))

map_users=pd.DataFrame(map_User_clm)

map_users['States']=map_users['States'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
map_users['States']=map_users['States'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
map_users['States']=map_users['States'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
map_users['States']=map_users['States'].str.replace("-"," ")
map_users['States']=map_users['States'].str.title()



#5 Top transaction
path="C:/GD/Notes/DS Class/DTM15/Project/Phonepe project/github/pulse/data/top/transaction/country/india/state/"
state_list=os.listdir(path)

top_trans_clm={'States':[], 'Years':[],'Quater':[],'Pincodes':[], 'Transaction_count':[], 'Transaction_amount':[]}

for state in state_list:
    p_s=path+state+"/"
    years_list=os.listdir(p_s)
    for year in years_list:
        p_y=p_s+year+"/"
        quater_list=os.listdir(p_y)
        for quater in quater_list:
            p_q=p_y+quater
            Data=open(p_q,'r')
            D=json.load(Data)
            for i in D['data']['pincodes']:
                Entity_name=i['entityName']
                count=i['metric']['count']
                amount=i['metric']['amount']
                top_trans_clm['Pincodes'].append(Entity_name)
                top_trans_clm['Transaction_count'].append(count)
                top_trans_clm['Transaction_amount'].append(amount)
                top_trans_clm['States'].append(state)
                top_trans_clm['Years'].append(year)
                top_trans_clm['Quater'].append(int(quater.strip('.json')))

top_trans=pd.DataFrame(top_trans_clm)

top_trans['States']=top_trans['States'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
top_trans['States']=top_trans['States'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
top_trans['States']=top_trans['States'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
top_trans['States']=top_trans['States'].str.replace("-"," ")
top_trans['States']=top_trans['States'].str.title()



#6 top/user
path="C:/GD/Notes/DS Class/DTM15/Project/Phonepe project/github/pulse/data/top/user/country/india/state/"
state_list=os.listdir(path)


top_user_clm={'States':[], 'Years':[],'Quater':[],'Pincodes': [], 'Reg_users':[]}

for state in state_list:
    p_s=path+state+"/"
    years_list=os.listdir(p_s)
    for year in years_list:
        p_y=p_s+year+"/"
        quater_list=os.listdir(p_y)
        for quater in quater_list:
            p_q=p_y+quater
            Data=open(p_q,'r')
            D=json.load(Data)
            for i in D['data']['pincodes']:
                Name=i['name']
                reg_users=i['registeredUsers']
                top_user_clm['Pincodes'].append(Name)
                top_user_clm['Reg_users'].append(reg_users)
                top_user_clm['States'].append(state)
                top_user_clm['Years'].append(year)
                top_user_clm['Quater'].append(int(quater.strip('.json')))

top_user=pd.DataFrame(top_user_clm)

top_user['States']=top_user['States'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
top_user['States']=top_user['States'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
top_user['States']=top_user['States'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
top_user['States']=top_user['States'].str.replace("-"," ")
top_user['States']=top_user['States'].str.title()



#SQL

agg_trans.to_sql('agg_trans', engine, if_exists='replace', index=False)
agg_users.to_sql('agg_users', engine, if_exists='replace', index=False)
map_trans.to_sql('map_trans', engine, if_exists='replace', index=False)
map_users.to_sql('map_users', engine, if_exists='replace', index=False)
top_trans.to_sql('top_trans', engine, if_exists='replace', index=False)
top_user.to_sql('top_user', engine, if_exists='replace', index=False)