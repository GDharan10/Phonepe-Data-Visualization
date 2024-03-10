import pandas as pd
import json
import os
import psycopg2

from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:1005@localhost/phonepay')

#1 aggregated/transaction
path="C:/GD/Notes/DS Class/DTM15/Project/Phonepay project/github/pulse/data/aggregated/transaction/country/india/state/"
Agg_state_list=os.listdir(path)
Agg_state_list

clm={'State':[], 'Year':[],'Quater':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              clm['Transacion_type'].append(Name)
              clm['Transacion_count'].append(count)
              clm['Transacion_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quater'].append(int(k.strip('.json')))

agg_trans=pd.DataFrame(clm)

agg_trans['State']=agg_trans['State'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
agg_trans['State']=agg_trans['State'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
agg_trans['State']=agg_trans['State'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
agg_trans['State']=agg_trans['State'].str.replace("-"," ")
agg_trans['State']=agg_trans['State'].str.title()


#2 aggregated/user
path="C:/GD/Notes/DS Class/DTM15/Project/Phonepay project/github/pulse/data/aggregated/user/country/india/state/"
Agg_state_list=os.listdir(path)
Agg_state_list

clm={'State':[], 'Year':[],'Quater':[],'user_brand':[], 'reg_userbrand_count':[], 'reg_percentage':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            try:
                for z in D['data']['usersByDevice']:
                    Brand=z['brand']
                    count=z['count']
                    percentage=z['percentage']
                    clm['user_brand'].append(Brand)
                    clm['reg_userbrand_count'].append(count)
                    clm['reg_percentage'].append(percentage)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
            except:
                pass

agg_users=pd.DataFrame(clm)

agg_users['State']=agg_users['State'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
agg_users['State']=agg_users['State'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
agg_users['State']=agg_users['State'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
agg_users['State']=agg_users['State'].str.replace("-"," ")
agg_users['State']=agg_users['State'].str.title()


#3 map/transaction
path="C:/GD/Notes/DS Class/DTM15/Project/Phonepay project/github/pulse/data/map/transaction/hover/country/india/state/"
map_state_list=os.listdir(path)
map_state_list

clm={'State':[], 'Year':[],'Quater':[],'district_name':[], 'transaction_count':[], 'transaction_amount':[]}

for i in map_state_list:
    p_i=path+i+"/"
    map_yr=os.listdir(p_i)
    for j in map_yr:
        p_j=p_i+j+"/"
        map_yr_list=os.listdir(p_j)
        for k in map_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            try:
              for z in D['data']['hoverDataList']:
                Name=z['name']
                count=z['metric'][0]['count']
                amount=z['metric'][0]['amount']
                clm['district_name'].append(Name)
                clm['transaction_count'].append(count)
                clm['transaction_amount'].append(amount)
                clm['State'].append(i)
                clm['Year'].append(j)
                clm['Quater'].append(int(k.strip('.json')))
            except Exception as e:
              print(f"Error processing file '{p_k}': {e}")

map_trans=pd.DataFrame(clm)

map_trans['State']=map_trans['State'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
map_trans['State']=map_trans['State'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
map_trans['State']=map_trans['State'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
map_trans['State']=map_trans['State'].str.replace("-"," ")
map_trans['State']=map_trans['State'].str.title()


#4 map/User
path="C:/GD/Notes/DS Class/DTM15/Project/Phonepay project/github/pulse/data/map/user/hover/country/india/state/"
map_state_list=os.listdir(path)
map_state_list

clm={'State':[], 'Year':[],'Quater':[],'District_name':[], 'reg_users':[], 'app_opens':[]}

for i in map_state_list:
    p_i=path+i+"/"
    map_yr=os.listdir(p_i)
    for j in map_yr:
        p_j=p_i+j+"/"
        map_yr_list=os.listdir(p_j)
        for k in map_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['hoverData'].items():
              district=z[0]
              regusers=z[1]['registeredUsers']
              appopens=z[1]['appOpens']
              clm['District_name'].append(district)
              clm['reg_users'].append(regusers)
              clm['app_opens'].append(appopens)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quater'].append(int(k.strip('.json')))

map_users=pd.DataFrame(clm)

map_users['State']=map_users['State'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
map_users['State']=map_users['State'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
map_users['State']=map_users['State'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
map_users['State']=map_users['State'].str.replace("-"," ")
map_users['State']=map_users['State'].str.title()


#5 Top transaction
path="C:/GD/Notes/DS Class/DTM15/Project/Phonepay project/github/pulse/data/top/transaction/country/india/state/"
top_state_list=os.listdir(path)
top_state_list

clm={'State':[], 'Year':[],'Quater':[],'pincodes':[], 'transaction_count':[], 'transaction_amount':[]}

for i in top_state_list:
    p_i=path+i+"/"
    top_yr=os.listdir(p_i)
    for j in top_yr:
        p_j=p_i+j+"/"
        top_yr_list=os.listdir(p_j)
        for k in top_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['pincodes']:
                Entity_name=z['entityName']
                count=z['metric']['count']
                amount=z['metric']['amount']
                clm['pincodes'].append(Entity_name)
                clm['transaction_count'].append(count)
                clm['transaction_amount'].append(amount)
                clm['State'].append(i)
                clm['Year'].append(j)
                clm['Quater'].append(int(k.strip('.json')))

top_trans=pd.DataFrame(clm)

top_trans['State']=top_trans['State'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
top_trans['State']=top_trans['State'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
top_trans['State']=top_trans['State'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
top_trans['State']=top_trans['State'].str.replace("-"," ")
top_trans['State']=top_trans['State'].str.title()



#6 top/user
path="C:/GD/Notes/DS Class/DTM15/Project/Phonepay project/github/pulse/data/top/user/country/india/state/"
top_state_list=os.listdir(path)
top_state_list

clm={'State':[], 'Year':[],'Quater':[],'Pincodes': [], 'reg_users':[]}

for i in top_state_list:
    p_i=path+i+"/"
    top_yr=os.listdir(p_i)
    for j in top_yr:
        p_j=p_i+j+"/"
        top_yr_list=os.listdir(p_j)
        for k in top_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['pincodes']:
                Name=z['name']
                reg_users=z['registeredUsers']
                clm['Pincodes'].append(Name)
                clm['reg_users'].append(reg_users)
                clm['State'].append(i)
                clm['Year'].append(j)
                clm['Quater'].append(int(k.strip('.json')))

top_user=pd.DataFrame(clm)

top_user['State']=top_user['State'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
top_user['State']=top_user['State'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
top_user['State']=top_user['State'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
top_user['State']=top_user['State'].str.replace("-"," ")
top_user['State']=top_user['State'].str.title()



#SQL

agg_trans.to_sql('agg_trans', engine, if_exists='replace', index=False)
agg_users.to_sql('agg_users', engine, if_exists='replace', index=False)
map_trans.to_sql('map_trans', engine, if_exists='replace', index=False)
map_users.to_sql('map_users', engine, if_exists='replace', index=False)
top_trans.to_sql('top_trans', engine, if_exists='replace', index=False)
top_user.to_sql('top_user', engine, if_exists='replace', index=False)