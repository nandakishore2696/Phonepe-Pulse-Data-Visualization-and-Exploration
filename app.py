import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
import mysql.connector
import streamlit as st

st.set_page_config(layout='wide')
st.header("Welcome to Phonepe Pulse Data Visualization and Exploration")

tab = st.tabs(["Geospatial Maps", " Standalone Data", "Chartbusters"])

with tab[0]:
    # Agg_Trans
    path1 = "pulse\\data\\aggregated\\transaction\\country\\india\\state\\"
    agg_state_list = os.listdir(path1)

    clm={'State':[], 'Year':[],'Quarter':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}
    for i in agg_state_list:
        p_i = path1+i+'\\'
        agg_year = os.listdir(p_i)
        for j in agg_year:
            p_j = p_i+j+"\\"
            qtr = os.listdir(p_j)
            for k in qtr:
                p_k = p_j+k
                data  = open(p_k,'r')
                dj = json.load(data)
                for z in dj['data']['transactionData']:
                    name = z['name']
                    count = z['paymentInstruments'][0]['count']
                    amount = z['paymentInstruments'][0]['amount']
                    clm['Transacion_type'].append(name)
                    clm['Transacion_count'].append(count)
                    clm['Transacion_amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(k.strip(".json"))

    Agg_Trans = pd.DataFrame(clm)
    Agg_Trans['State'] = Agg_Trans['State'].str.replace('andaman-&-nicobar-islands','Andaman & Nicobar')
    Agg_Trans['State'] = Agg_Trans['State'].str.replace('-',' ')
    Agg_Trans['State'] = Agg_Trans['State'].str.title()
    Agg_Trans['State'] = Agg_Trans['State'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

    # Agg_users
    path2 = "pulse\\data\\aggregated\\user\\country\\india\\state\\"
    agg_state_list = os.listdir(path2)

    clm = {"State": [], "Year": [], "Quarter": [], 'Registered_Users': [], 'AppOpens': []}

    for i in agg_state_list:
        p_i = path2 + i + '\\'
        agg_year = os.listdir(p_i)
        for j in agg_year:
            p_j = p_i + j + "\\"
            qtr = os.listdir(p_j)
            for k in qtr:
                p_k = p_j + k
                data = open(p_k, 'r')
                dj = json.load(data)
                registered_Users = dj['data']['aggregated']['registeredUsers']
                app_Opens = dj['data']['aggregated']['appOpens']
                clm['Registered_Users'].append(registered_Users)
                clm['AppOpens'].append(app_Opens)
                clm['State'].append(i)
                clm['Year'].append(j)
                clm['Quarter'].append(k.strip(".json"))

    Agg_users = pd.DataFrame(clm)
    Agg_users['State'] = Agg_users['State'].str.replace('andaman-&-nicobar-islands','Andaman & Nicobar')
    Agg_users['State'] = Agg_users['State'].str.replace('-',' ')
    Agg_users['State'] = Agg_users['State'].str.title()
    Agg_users['State'] = Agg_users['State'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

    # map_transaction
    path3 = "pulse\\data\\map\\transaction\\hover\\country\\india\\state\\"
    map_state_list = os.listdir(path3)

    clm = {"State":[], "Year":[], "Quarter":[],"District":[], "Transaction_count":[],"Transaction_amount":[]}

    for state in map_state_list:
        cur_states = path3+state+"\\"
        map_year_list = os.listdir(cur_states)
        
        for year in map_year_list:
            cur_years = cur_states+year+"\\"
            map_file_list = os.listdir(cur_years)
            
            for file in map_file_list:
                cur_files = cur_years+file
                data = open(cur_files,"r")
                C = json.load(data)

                for i in C['data']["hoverDataList"]:
                    name = i["name"]
                    count = i["metric"][0]["count"]
                    amount = i["metric"][0]["amount"]
                    clm["District"].append(name)
                    clm["Transaction_count"].append(count)
                    clm["Transaction_amount"].append(amount)
                    clm["State"].append(state)
                    clm["Year"].append(year)
                    clm["Quarter"].append(int(file.strip(".json")))

    map_transaction = pd.DataFrame(clm)

    map_transaction["State"] = map_transaction["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    map_transaction["State"] = map_transaction["State"].str.replace("-"," ")
    map_transaction["State"] = map_transaction["State"].str.title()
    map_transaction['State'] = map_transaction['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    # map_user
    path4 = "pulse\\data\\map\\user\\hover\\country\\india\\state\\"
    map_state_list = os.listdir(path4)

    clm = {"State":[], "Year":[], "Quarter":[], "District":[], "Registered_User":[], "AppOpens":[]}

    for state in map_state_list:
        cur_states = path4+state+"\\"
        map_year_list = os.listdir(cur_states)
        
        for year in map_year_list:
            cur_years = cur_states+year+"\\"
            map_file_list = os.listdir(cur_years)
            
            for file in map_file_list:
                cur_files = cur_years+file
                data = open(cur_files,"r")
                D = json.load(data)

                for i in D["data"]["hoverData"].items():
                    district = i[0]
                    registereduser = i[1]["registeredUsers"]
                    appopens = i[1]["appOpens"]
                    clm["District"].append(district)
                    clm["Registered_User"].append(registereduser)
                    clm["AppOpens"].append(appopens)
                    clm["State"].append(state)
                    clm["Year"].append(year)
                    clm["Quarter"].append(int(file.strip(".json")))

    map_user = pd.DataFrame(clm)

    map_user["State"] = map_user["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    map_user["State"] = map_user["State"].str.replace("-"," ")
    map_user["State"] = map_user["State"].str.title()
    map_user['State'] = map_user['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    # top_transaction
    path5 = "pulse\\data\\top\\transaction\\country\\india\\state\\"
    top_state_list = os.listdir(path5)

    clm = {"State":[], "Year":[], "Quarter":[], "Pincode":[], "Transaction_count":[], "Transaction_amount":[]}

    for state in top_state_list:
        cur_states = path5+state+"\\"
        top_year_list = os.listdir(cur_states)
        
        for year in top_year_list:
            cur_years = cur_states+year+"\\"
            top_file_list = os.listdir(cur_years)
            
            for file in top_file_list:
                cur_files = cur_years+file
                data = open(cur_files,"r")
                E = json.load(data)

                for i in E["data"]["pincodes"]:
                    entityName = i["entityName"]
                    count = i["metric"]["count"]
                    amount = i["metric"]["amount"]
                    clm["Pincode"].append(entityName)
                    clm["Transaction_count"].append(count)
                    clm["Transaction_amount"].append(amount)
                    clm["State"].append(state)
                    clm["Year"].append(year)
                    clm["Quarter"].append(int(file.strip(".json")))

    top_transaction = pd.DataFrame(clm)

    top_transaction["State"] = top_transaction["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    top_transaction["State"] = top_transaction["State"].str.replace("-"," ")
    top_transaction["State"] = top_transaction["State"].str.title()
    top_transaction['State'] = top_transaction['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    # top_user
    path6 = "pulse\\data\\top\\user\\country\\india\\state\\"
    top_state_list = os.listdir(path6)

    clm = {"State":[], "Year":[], "Quarter":[], "Pincode":[], "Registered_User":[]}

    for state in top_state_list:
        cur_states = path6+state+"\\"
        top_year_list = os.listdir(cur_states)

        for year in top_year_list:
            cur_years = cur_states+year+"\\"
            top_file_list = os.listdir(cur_years)

            for file in top_file_list:
                cur_files = cur_years+file
                data = open(cur_files,"r")
                pin = json.load(data)

                for i in pin["data"]["pincodes"]:
                    name = i["name"]
                    registeredusers = i["registeredUsers"]
                    clm["Pincode"].append(name)
                    clm["Registered_User"].append(registereduser)
                    clm["State"].append(state)
                    clm["Year"].append(year)
                    clm["Quarter"].append(int(file.strip(".json")))

    top_user = pd.DataFrame(clm)

    top_user["State"] = top_user["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    top_user["State"] = top_user["State"].str.replace("-"," ")
    top_user["State"] = top_user["State"].str.title()
    top_user['State'] = top_user['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'mysql123',
        'database': 'phonepe_pulse'
        }
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    create_query1 = '''CREATE TABLE if not exists aggregated_transaction (State varchar(50),
                                                                        Year int,
                                                                        Quarter int,
                                                                        Transacion_type varchar(50),
                                                                        Transacion_count int,
                                                                        Transacion_amount BIGINT
                                                                        )'''
    cursor.execute(create_query1)
    conn.commit()

    for index,row in Agg_Trans.iterrows():
        insert_query1 = '''INSERT INTO aggregated_transaction (State, Year, Quarter, Transacion_type, Transacion_count, Transacion_amount)
                                                            values(%s,%s,%s,%s,%s,%s)'''
        values = (row["State"],
                row["Year"],
                row["Quarter"],
                row["Transacion_type"],
                row["Transacion_count"],
                row["Transacion_amount"]
                )
        cursor.execute(insert_query1,values)
    conn.commit()

    create_query2 = '''CREATE TABLE if not exists aggregated_user (State varchar(50),
                                                                        Year int,
                                                                        Quarter int,
                                                                        Registered_Users BIGINT,
                                                                        AppOpens BIGINT
                                                                        )'''
    cursor.execute(create_query2)
    conn.commit()

    for index,row in Agg_users.iterrows():
        insert_query2 = '''INSERT INTO aggregated_user (State, Year, Quarter, Registered_Users, AppOpens)
                                                            values(%s,%s,%s,%s,%s)'''
        values = (row["State"],
                row["Year"],
                row["Quarter"],
                row["Registered_Users"],
                row["AppOpens"]
                )
        cursor.execute(insert_query2,values)
    conn.commit()

    create_query1 = '''CREATE TABLE if not exists map_transaction (State varchar(50),
                                                                        Year int,
                                                                        Quarter int,
                                                                        District varchar(255),
                                                                        Transaction_count BIGINT,
                                                                        Transaction_amount BIGINT
                                                                        )'''
    cursor.execute(create_query1)
    conn.commit()

    for index,row in map_transaction.iterrows():
        insert_query1 = '''INSERT INTO map_transaction (State, Year, Quarter,District, Transaction_count, Transaction_amount)
                                                            values(%s,%s,%s,%s,%s,%s)'''
        values = (row["State"],
                row["Year"],
                row["Quarter"],
                row['District'],
                row["Transaction_count"],
                row["Transaction_amount"]
                )
        cursor.execute(insert_query1,values)
    conn.commit()

    create_query1 = '''CREATE TABLE if not exists map_user (State varchar(50),
                                                                        Year int,
                                                                        Quarter int,
                                                                        District varchar(255),
                                                                        Registered_User BIGINT,
                                                                        AppOpens BIGINT
                                                                        )'''
    cursor.execute(create_query1)
    conn.commit()

    for index,row in map_user.iterrows():
        insert_query1 = '''INSERT INTO map_user (State, Year, Quarter, District,Registered_User, AppOpens)
                                                            values(%s,%s,%s,%s,%s,%s)'''
        values = (row["State"],
                row["Year"],
                row["Quarter"],
                row['District'],
                row["Registered_User"],
                row["AppOpens"]
                )
        cursor.execute(insert_query1,values)
    conn.commit()

    create_query1 = '''CREATE TABLE if not exists top_transaction (State varchar(50),
                                                                        Year int,
                                                                        Quarter int,
                                                                        Pincode int,
                                                                        Transaction_count BIGINT,
                                                                        Transaction_amount BIGINT
                                                                        )'''
    cursor.execute(create_query1)
    conn.commit()

    for index,row in top_transaction.iterrows():
        insert_query1 = '''INSERT INTO top_transaction (State, Year, Quarter,Pincode, Transaction_count, Transaction_amount)
                                                            values(%s,%s,%s,%s,%s,%s)'''
        values = (row["State"],
                row["Year"],
                row["Quarter"],
                row['Pincode'],
                row["Transaction_count"],
                row["Transaction_amount"]
                )
        cursor.execute(insert_query1,values)
    conn.commit()

    create_query1 = '''CREATE TABLE if not exists top_user (State varchar(50),
                                                                        Year int,
                                                                        Quarter int,
                                                                        Pincode int,
                                                                        Registered_User BIGINT
                                                                        )'''
    cursor.execute(create_query1)
    conn.commit()

    for index,row in top_user.iterrows():
        insert_query1 = '''INSERT INTO top_user (State, Year, Quarter, Pincode,Registered_User)
                                                            values(%s,%s,%s,%s,%s)'''
        values = (row["State"],
                row["Year"],
                row["Quarter"],
                row['Pincode'],
                row["Registered_User"]
                )
        cursor.execute(insert_query1,values)
    conn.commit()

    cursor.execute(''' select * from aggregated_transaction''')
    a = cursor.fetchall()
    Aggre_trans = pd.DataFrame(a,columns = ("State", "Year", "Quarter", "Transacion_type", "Transacion_count", "Transacion_amount"))

    cursor.execute(''' select * from aggregated_user''')
    a = cursor.fetchall()
    Aggre_user = pd.DataFrame(a,columns = ("State", "Year", "Quarter", "Registered_Users", "AppOpens"))

    cursor.execute(''' select * from map_transaction''')
    a = cursor.fetchall()
    Map_trans = pd.DataFrame(a,columns = ("State", "Year", "Quarter", "District", "Transaction_count", "Transaction_amount"))

    cursor.execute(''' select * from map_user''')
    a = cursor.fetchall()
    Map_user = pd.DataFrame(a,columns = ("State", "Year", "Quarter", "District", "Registered_User", "AppOpens"))

    cursor.execute(''' select * from top_transaction''')
    a = cursor.fetchall()
    Top_trans = pd.DataFrame(a,columns = ("State", "Year", "Quarter", "Pincode", "Transaction_count", "Transaction_amount"))

    cursor.execute(''' select * from top_user''')
    a = cursor.fetchall()
    Top_user = pd.DataFrame(a,columns = ("State", "Year", "Quarter", "Pincode", "Registered_User"))

    col1,col2 = st.columns(2)
    with col1:
        st.header("Transacion Amount")
        with st.expander("Transacion Amount of States"):
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response =requests.get(url)
            data1 = json.loads(response.content)
            fig_tra = px.choropleth(Aggre_trans, geojson= data1, locations= "State", featureidkey= "properties.ST_NM", color= "Transacion_amount",
                                    color_continuous_scale= "Sunsetdark", range_color= (0,2500000000), hover_name= "State", title = "Transacion Amount",
                                    animation_frame="Year", animation_group="Quarter")

            fig_tra.update_geos(fitbounds= "locations", visible =False)
            fig_tra.update_layout(width =600, height= 500)
            fig_tra.update_layout(title_font= {"size":25})
            st.plotly_chart(fig_tra)

        with st.expander("Transacion Amount by Transacion type"):
            df1 =Aggre_trans[["Transacion_type", "Transacion_amount"]].groupby('Transacion_type').sum()
            df = pd.DataFrame(df1).reset_index()
            fig_tra = px.pie(df,values=df['Transacion_amount'],names=df['Transacion_type'],title="Transacion type")
            fig_tra.update_layout(width =600, height= 500)
            fig_tra.update_layout(title_font= {"size":25})
            st.plotly_chart(fig_tra)

        with st.expander("Registered_Users by State"):
            #url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            #response =requests.get(url)
            #data1 = json.loads(response.content)
            fig_tra = px.choropleth(Aggre_user, geojson= data1, locations= "State", featureidkey= "properties.ST_NM", color= "Registered_Users",
                                    color_continuous_scale= "Sunsetdark",range_color= (0,70000000), hover_name= "State", title = "Registered_Users",
                                    animation_frame="Year")

            fig_tra.update_geos(fitbounds= "locations", visible =False)
            fig_tra.update_layout(width =600, height= 500)
            fig_tra.update_layout(title_font= {"size":25})
            st.plotly_chart(fig_tra)

    with col2:
        st.header("Transacion Count")
        with st.expander("Transacion Count of States"):
            #url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            #response =requests.get(url)
            #data1 = json.loads(response.content)
            fig_tra = px.choropleth(Aggre_trans, geojson= data1, locations= "State", featureidkey= "properties.ST_NM", color= "Transacion_count",
                                    color_continuous_scale= "Sunsetdark",range_color= (0,2000000), hover_name= "State", title = "Transacion Count",
                                    animation_frame="Year")

            fig_tra.update_geos(fitbounds= "locations", visible =False)
            fig_tra.update_layout(width =600, height= 500)
            fig_tra.update_layout(title_font= {"size":25})
            st.plotly_chart(fig_tra)

        with st.expander("Transacion Count by Transacion type"):
            df1 =Aggre_trans[["Transacion_type", "Transacion_count"]].groupby('Transacion_type').sum()
            df = pd.DataFrame(df1).reset_index()
            fig_tra = px.pie(df,values=df['Transacion_count'],names=df['Transacion_type'],title="Transacion type")
            fig_tra.update_layout(width =600, height= 500)
            fig_tra.update_layout(title_font= {"size":25})
            st.plotly_chart(fig_tra)

        with st.expander("App Opens by State"):
            #url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            #response =requests.get(url)
            #data1 = json.loads(response.content)
            fig_tra = px.choropleth(Aggre_user, geojson= data1, locations= "State", featureidkey= "properties.ST_NM", color= "AppOpens",
                                    color_continuous_scale= "Sunsetdark",range_color= (0,4500000000), hover_name= "State", title = "App Opens",
                                    animation_frame="Year")

            fig_tra.update_geos(fitbounds= "locations", visible =False)
            fig_tra.update_layout(width =600, height= 500)
            fig_tra.update_layout(title_font= {"size":25})
            st.plotly_chart(fig_tra)

with tab[1]:

    st_name = st.text_input("Enter the state name here")
    st.write('''[Andaman & Nicobar, Andhra Pradesh, Arunachal Pradesh,Assam, Bihar, Chandigarh, 
             Chhattisgarh,Dadra and Nagar Haveli and Daman and Diu, Delhi, Goa,Gujarat, Haryana, 
             Himachal Pradesh, Jammu & Kashmir,Jharkhand, Karnataka, Kerala, Ladakh, Lakshadweep,
             Madhya Pradesh, Maharashtra, Manipur, Meghalaya, Mizoram,Nagaland, Odisha, Puducherry,
              Punjab, Rajasthan,Sikkim, Tamil Nadu, Telangana, Tripura, Uttar Pradesh,
             Uttarakhand, West Bengal]''')
    df1 = Aggre_trans[Aggre_trans['State'] == st_name].groupby("Year").sum()[['Transacion_amount','Transacion_count']]
    df = pd.DataFrame(df1).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Transacion_amount'], mode='lines', name='Transacion_amount', yaxis='y1',line=dict(color='yellow')))
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Transacion_count'], mode='lines', name='Transacion_count', yaxis='y2',line=dict(color='white')))
    fig.update_layout(
        title='Transacion_amount & Transacion_count',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Transacion_amount', side='left', showgrid=False),
        yaxis2=dict(title='Transacion_count', overlaying='y', side='right') )
    st.plotly_chart(fig)


    df1 = Aggre_user[Aggre_user['State'] == st_name].groupby("Year").sum()[['Registered_Users','AppOpens']]
    df = pd.DataFrame(df1).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Registered_Users'], mode='lines', name='Registered_Users', yaxis='y1',line=dict(color='yellow')))
    fig.add_trace(go.Scatter(x=df['Year'], y=df['AppOpens'], mode='lines', name='AppOpens', yaxis='y2',line=dict(color='white')))
    fig.update_layout(
        title='Registered_Users & AppOpens',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Registered_Users', side='left', showgrid=False),
        yaxis2=dict(title='AppOpens', overlaying='y', side='right'))
    st.plotly_chart(fig)

with tab[2]:
    
    st.write("Chart toppers")
    with st.expander('Top state based on total amount transfered'):
        df = Aggre_trans.groupby("State").sum().sort_values("Transacion_amount",ascending=False).head(10)[['Transacion_amount']].reset_index()
        fig = px.bar(df,x=df['State'],y=df['Transacion_amount'], color='Transacion_amount',color_continuous_scale='viridis_r')
        st.plotly_chart(fig)

    with st.expander("Top state based on total count"):
        df = Aggre_trans.groupby("State").sum().sort_values("Transacion_count",ascending=False).head(10)[['Transacion_count']].reset_index()
        fig = px.bar(df,x=df['State'],y=df['Transacion_count'], color='Transacion_count',color_continuous_scale='viridis_r')
        st.plotly_chart(fig)

    with st.expander("Top state based on Registered_Users"):
        df = Aggre_user.groupby("State").sum().sort_values("Registered_Users",ascending=False).head(10)[['Registered_Users']].reset_index()
        fig = px.bar(df,x=df['State'],y=df['Registered_Users'], color='Registered_Users',color_continuous_scale='viridis_r')
        st.plotly_chart(fig)

    with st.expander("Top state based on AppOpens"):
        df = Aggre_user.groupby("State").sum().sort_values("AppOpens",ascending=False).head(10)[['AppOpens']].reset_index()
        fig = px.bar(df,x=df['State'],y=df['AppOpens'], color='AppOpens',color_continuous_scale='viridis_r')
        st.plotly_chart(fig)

    with st.expander("Top District based on Transaction_amount"):
        df = Map_trans.groupby("District").sum().sort_values("Transaction_amount",ascending=False).head(10)[['Transaction_amount']].reset_index()
        fig = px.bar(df,x=df['District'],y=df['Transaction_amount'], color='Transaction_amount',color_continuous_scale='viridis_r')
        st.plotly_chart(fig)

    with st.expander("Top District based on Transaction_count"):
        df = Map_trans.groupby("District").sum().sort_values("Transaction_count",ascending=False).head(10)[['Transaction_count']].reset_index()
        fig = px.bar(df,x=df['District'],y=df['Transaction_count'], color='Transaction_count',color_continuous_scale='viridis_r')
        st.plotly_chart(fig)

    with st.expander("Top District based on Registered_User"):
        df = Map_user.groupby("District").sum().sort_values("Registered_User",ascending=False).head(10)[['Registered_User']].reset_index()
        fig = px.bar(df,x=df['District'],y=df['Registered_User'], color='Registered_User',color_continuous_scale='viridis_r')
        st.plotly_chart(fig)

    with st.expander("Top District based on AppOpens"):
        df = Map_user.groupby("District").sum().sort_values("AppOpens",ascending=False).head(10)[['AppOpens']].reset_index()
        fig = px.bar(df,x=df['District'],y=df['AppOpens'], color='AppOpens',color_continuous_scale='viridis_r')
        st.plotly_chart(fig)

    with st.expander("Top Pincode based on Transaction_amount"):
        df = Top_trans.groupby("Pincode").sum().sort_values("Transaction_amount",ascending=False).head(10)[['Transaction_amount']].reset_index()
        df['Pincode'] = df['Pincode'].astype(int).astype(str)
        fig = px.bar(df,x=df['Pincode'],y=df['Transaction_amount'], color='Transaction_amount',color_continuous_scale='viridis_r')
        st.plotly_chart(fig)

    with st.expander("Top Pincode based on Transaction_count"):
        df = Top_trans.groupby("Pincode").sum().sort_values("Transaction_count",ascending=False).head(10)[['Transaction_count']].reset_index()
        df['Pincode'] = df['Pincode'].astype(int).astype(str)
        fig = px.bar(df,x=df['Pincode'],y=df['Transaction_count'], color='Transaction_count',color_continuous_scale='viridis_r')
        st.plotly_chart(fig)
