import pandas as pd
import streamlit as st


from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:1005@localhost/phonepay')

import plotly.express as px


# all df
agg_trans_df = pd.read_sql('agg_trans', engine)
agg_users_df = pd.read_sql('agg_users', engine)
map_trans_df = pd.read_sql('map_trans', engine)
map_users_df = pd.read_sql('map_users', engine)
top_trans_df = pd.read_sql('top_trans', engine)
top_user_df = pd.read_sql('top_user', engine)

#agg_trans_df.query(' State == "Tamil Nadu" and Year == "2023" and Quater == 1 and Transaction_type == "Merchant payments" ')

#fig = px.pie(agg_trans_df, names='Transaction_type', values='Transaction_count')


def agg_t():

    agg_trans_df = pd.read_sql('agg_trans', engine)

    states = agg_trans_df['States'].unique()
    excluded_columns = ['States', 'Transaction_count', 'Transaction_amount']
    
    row1 = st.columns(2)
    row2 = st.columns(2)
    row3 = st.columns(2)
    row4 = st.columns(2)
    row5 = st.columns(2)
    row6 = st.columns(2)

    with row1[0]:
        pass
    
    with row1[1]:
        sub_columns = st.columns(2)
        
        with sub_columns[0]:
            coloum1 = [col for col in agg_trans_df.columns if col not in excluded_columns]
            selected_coloum1 = st.selectbox("Select a coloum1", coloum1) 
        
        with sub_columns[1]:
            if selected_coloum1:
                coloum2 = [col for col in coloum1 if col != selected_coloum1]
            selected_coloum2 = st.selectbox("Select a coloum2", coloum2) 

    with row2[0]:
        fig3 = px.sunburst(agg_trans_df, path=[selected_coloum1, selected_coloum2], values='Transaction_count')
        fig3.update_layout(title='Transaction Count', title_x=0.35)
        st.plotly_chart(fig3)

    with row2[1]:
        fig4 = px.sunburst(agg_trans_df, path=[selected_coloum1, selected_coloum2], values='Transaction_amount')
        fig4.update_layout(title='Transaction Amount', title_x=0.35)
        st.plotly_chart(fig4)

    with row3[0]:
        selected_state = st.selectbox("Select a state", ['All states'] + list(states))
        if selected_state == 'All states':
            stateAT = agg_trans_df
        else:
            stateAT = agg_trans_df.query('States == @selected_state')

    with row4[0]:
        fig1 = px.scatter(stateAT, x='Transaction_count', y='Transaction_amount', color='Transaction_type',
                        facet_col='Years', facet_col_wrap=3,
                        title='Transaction Count vs Transaction Amount by Transaction Type and Year')
        fig1.update_layout(xaxis_title='Transaction Count', yaxis_title='Transaction Amount')
        st.plotly_chart(fig1)
        

    with row5[0]:
        pass
    
    with row5[1]:
        sub_columns = st.columns(2)
        
        with sub_columns[0]:
            pass
        
        with sub_columns[1]:
            coloum1 = agg_trans_df["Years"].unique()
            selected_year = st.selectbox("Select a year", coloum1)

    with row6[0]:
        ATS = agg_trans_df[agg_trans_df["Years"]==selected_year]
        ATS_M = ATS.groupby('States')[['Transaction_count', 'Transaction_amount']].sum()
        ATS_M.reset_index(inplace = True)

        fig6 = px.choropleth(
            ATS_M,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_count',
            color_continuous_scale='turbo',
            range_color = (ATS_M['Transaction_count'].min(), ATS_M['Transaction_count'].max()),
            title = 'Transacion count'
            )

        fig6.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig6)

    with row6[1]:
        ATS = agg_trans_df[agg_trans_df["Years"]==selected_year]
        ATS_M = ATS.groupby('States')[['Transaction_count', 'Transaction_amount']].sum()
        ATS_M.reset_index(inplace = True)

        fig7 = px.choropleth(
            ATS_M,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_amount',
            color_continuous_scale='turbo',
            range_color = (ATS_M['Transaction_amount'].min(), ATS_M['Transaction_amount'].max()),
            title = 'Transacion amount'
            )

        fig7.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig7)





def map_t():
    map_trans_df = pd.read_sql('map_trans', engine)

    states = map_trans_df['States'].unique()
    excluded_columns = ['States', 'Transaction_count', 'Transaction_amount']
    
    row1 = st.columns(2)
    row2 = st.columns(2)
    row3 = st.columns(2)
    row4 = st.columns(3)
    row5 = st.columns(2)
    

    with row1[0]:
        selected_state = st.selectbox("Select a state", ['All states'] + list(states))
        
    
    with row1[1]:
        sub_columns = st.columns(2)
        
        with sub_columns[0]:
            pass
        
        with sub_columns[1]:
            coloum1 = map_trans_df["Years"].unique()
            selected_year = st.selectbox("Select a year", coloum1)

    with row2[0]:
        MTS = map_trans_df[map_trans_df["Years"]==selected_year]

        MT_S_Map = MTS.groupby('States')[['Transaction_count', 'Transaction_amount']].sum()
        MT_S_Map.reset_index(inplace = True)

        if selected_state == 'All states':
            stateMT = MT_S_Map
        else:
            stateMT = MT_S_Map[MT_S_Map['States'] == selected_state]
                
        fig1 = px.choropleth(
            stateMT,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_count',
            color_continuous_scale='turbo',
            range_color = (MT_S_Map['Transaction_count'].min(), MT_S_Map['Transaction_count'].max()),
            title = 'Transacion count'
            )

        fig1.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig1)

    with row2[1]:
        MTS = map_trans_df[map_trans_df["Years"]==selected_year]

        MT_S_Map = MTS.groupby('States')[['Transaction_count', 'Transaction_amount']].sum()
        MT_S_Map.reset_index(inplace = True)
        if selected_state == 'All states':
            stateMT = MT_S_Map
        else:
            stateMT = MT_S_Map[MT_S_Map['States'] == selected_state]
                

        fig2 = px.choropleth(
            stateMT,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_amount',
            color_continuous_scale='turbo',
            range_color = (MT_S_Map['Transaction_amount'].min(), MT_S_Map['Transaction_amount'].max()),
            title = 'Transacion amount'
            )

        fig2.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig2)

    if selected_state == 'All states':
            pass

    else:
        with row3[0]:

                MT_D = map_trans_df.query('States == @selected_state and Years == @selected_year')


                fig3 = px.bar(MT_D, y=MT_D['District_name'].apply(lambda x: x.replace("district", "")), 
                                x=['Transaction_count'],
                                color='Quater',
                                barmode='stack', orientation='h',
                                title='Transaction Count by District',
                                labels={'value': 'Transaction', 'variable': 'Type'})

                fig3.update_layout(xaxis_title='Transaction count', title_x=0.35, yaxis_title='Districts', legend_title='Type', height= 700)

                st.plotly_chart(fig3)
        
        with row3[1]:
            
                MT_D_M = map_trans_df.query('States == @selected_state and Years == @selected_year')


                fig4 = px.bar(MT_D_M, y=MT_D_M['District_name'].apply(lambda x: x.replace("district", "")), 
                                x=['Transaction_amount'],
                                color='Quater',
                                barmode='stack', orientation='h',
                                title='Transaction amount by District',
                                labels={'value': 'Transaction', 'variable': 'Type'})

                fig4.update_layout(xaxis_title='Transaction amount', title_x=0.35, yaxis_title='Districts', legend_title='Type', height= 700)

                st.plotly_chart(fig4)

        with row4[1]:
            selected_dic = st.selectbox("Select a district", sorted(MT_D_M['District_name'].unique()))

            MT_D_bar = MT_D_M.query('District_name == @selected_dic')
        
        with row5[0]:
            fig5 = px.bar(MT_D_bar, y='Transaction_count', 
                                x='Quater',
                                color='Quater',
                                barmode='stack',
                                title='Transaction count by District',
                                labels={'value': 'Transaction', 'variable': 'Type'})

            fig5.update_layout(xaxis_title='Quater', title_x=0.35, yaxis_title='Transaction count', legend_title='Type')

            st.plotly_chart(fig5)

        with row5[1]:
            fig6 = px.bar(MT_D_bar, y='Transaction_amount', 
                                x='Quater',
                                color='Quater',
                                barmode='stack',
                                title='Transaction amount by District',
                                labels={'value': 'Transaction', 'variable': 'Type'})

            fig6.update_layout(xaxis_title='Quater', title_x=0.35, yaxis_title='Transaction amount', legend_title='Type')

            st.plotly_chart(fig6)


def top_t():
    top_trans_df = pd.read_sql('top_trans', engine)

    states = top_trans_df['States'].unique()

    row1 = st.columns(2)
    row2 = st.columns(2)
    row3 = st.columns(4)
    row4 = st.columns(2)
    row5 = st.columns(2)
    row6 = st.columns(2)
    

    with row1[0]:
        selected_state = st.selectbox("Select a state", ['All states'] + list(states))
        
    
    with row1[1]:
        sub_columns = st.columns(2)
        
        with sub_columns[0]:
            pass
        
        with sub_columns[1]:
            coloum1 = top_trans_df["Years"].unique()
            selected_year = st.selectbox("Select a year", coloum1)

    with row2[0]:
        TTS = top_trans_df[top_trans_df["Years"]==selected_year]

        TT_S_Map = TTS.groupby('States')[['Transaction_count', 'Transaction_amount']].sum()
        TT_S_Map.reset_index(inplace = True)

        if selected_state == 'All states':
            stateTT = TT_S_Map
        else:
            stateTT = TT_S_Map[TT_S_Map['States'] == selected_state]
                
        fig1 = px.choropleth(
            stateTT,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_count',
            color_continuous_scale='turbo',
            range_color = (TT_S_Map['Transaction_count'].min(), TT_S_Map['Transaction_count'].max()),
            title = 'Transacion count'
            )

        fig1.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig1)

    with row2[1]:
        TTS = top_trans_df[top_trans_df["Years"]==selected_year]

        TT_S_Map = TTS.groupby('States')[['Transaction_count', 'Transaction_amount']].sum()
        TT_S_Map.reset_index(inplace = True)
        if selected_state == 'All states':
            stateTT = TT_S_Map
        else:
            stateTT = TT_S_Map[TT_S_Map['States'] == selected_state]
                

        fig2 = px.choropleth(
            stateTT,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_amount',
            color_continuous_scale='turbo',
            range_color = (TT_S_Map['Transaction_amount'].min(), TT_S_Map['Transaction_amount'].max()),
            title = 'Transacion amount'
            )

        fig2.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig2)

        if selected_state == 'All states':
            pass

        else:

            with row3[1]:
                selected_quater = st.selectbox("Select a quater", top_trans_df['Quater'].unique())

                
            with row4[0]:

                    TT_Pin = top_trans_df.query('States == @selected_state and Years == @selected_year and Quater == @selected_quater').reset_index(drop=True)

                    st.write(TT_Pin[['Pincodes', 'Transaction_count']])

                    fig3 = px.bar(TT_Pin, x ='Transaction_count',
                                            y= 'Pincodes',
                                            orientation='h',
                                            title='Top 10 Transaction count'
                                            )
                   
                    fig3.update_layout(xaxis_title='Transaction_count',title_x=0.35,  yaxis_title='Pincodes')

                    st.plotly_chart(fig3)
            
            with row4[1]:
                
                    TT_Pin = top_trans_df.query('States == @selected_state and Years == @selected_year and Quater == @selected_quater').reset_index(drop=True)

                    st.write(TT_Pin[['Pincodes', 'Transaction_amount']])

                    fig4 = px.bar(TT_Pin, y='Pincodes', 
                                x='Transaction_amount',
                                color='Transaction_amount',
                                barmode='stack',
                                title='Top 10 Transaction amount',
                                labels={'value': 'Transaction', 'variable': 'Type'})

                    

                    fig4.update_layout(xaxis_title='Transaction amount', title_x=0.35, yaxis_title='Pincodes')

                    st.plotly_chart(fig4)

    
    





def agg_u():
    agg_users_df = pd.read_sql('agg_users', engine)

    states = agg_users_df['States'].unique()
        
    row1 = st.columns(2)
    row2 = st.columns(2)
    row3 = st.columns(2)
    

    with row1[0]:
        selected_state = st.selectbox("Select a state", states)
    
    with row1[1]:
        sub_columns = st.columns(3)
        
        with sub_columns[0]:
            selected_year = st.selectbox("Select a year", agg_users_df["Years"].unique())
        
        with sub_columns[1]:
            selected_quater = st.selectbox("Select a quater", agg_users_df['Quater'].unique()) 
        
        with sub_columns[2]:
            AU_B = agg_users_df.query(' States == @selected_state and Years == @selected_year')
            selected_brand = st.selectbox("Select a brand", AU_B["Brands"].unique())

    with row2[0]:
        AU_Brand = agg_users_df.query(' States == @selected_state and Years == @selected_year and Quater == @selected_quater ')

        fig1 = px.bar(AU_Brand, y='Reg_user_count', 
                                x='Brands',
                                color='Quater',
                                barmode='stack',
                                title='Distribution of User Brand Count',
                                labels={'value': 'Transaction', 'variable': 'Type'})

        fig1.update_layout(xaxis_title='Brands', title_x=0.35, yaxis_title='Count', legend_title='Type')

        st.plotly_chart(fig1)


    with row2[1]:
        AU_Brand = agg_users_df.query(' States == @selected_state and Years == @selected_year and Brands == @selected_brand ')

        fig2 = px.bar(AU_Brand, y='Reg_percentage', 
                                x='Quater',
                                color='Quater',
                                barmode='stack',
                                title='Distribution of User Brand Percentage',
                                labels={'value': 'Transaction', 'variable': 'Type'})

        fig2.update_layout(xaxis_title=f'{selected_brand}', title_x=0.35, yaxis_title='Percentage', legend_title='Type')

        st.plotly_chart(fig2)

        
    with row3[0]:
        AUS = agg_users_df[agg_users_df["Years"]==selected_year]
        AUS_M = AUS.groupby('States')[['Reg_user_count', 'Reg_percentage']].sum()
        AUS_M.reset_index(inplace = True)

        fig6 = px.choropleth(
            AUS_M,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='Reg_user_count',
            color_continuous_scale='turbo',
            range_color = (AUS_M['Reg_user_count'].min(), AUS_M['Reg_user_count'].max()),
            title = 'Registered count'
            )

        fig6.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig6)

    with row3[1]:
        AUS = agg_users_df[agg_users_df["Years"]==selected_year]
        AUS_M = AUS.groupby('States')[['Reg_user_count', 'Reg_percentage']].sum()
        AUS_M.reset_index(inplace = True)
        stateAU = AUS_M[AUS_M['States'] == selected_state]

        fig7 = px.choropleth(
            stateAU,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='Reg_user_count',
            color_continuous_scale='turbo',
            range_color = (AUS_M['Reg_user_count'].min(), AUS_M['Reg_user_count'].max()),
            title = 'Registered count'
            )

        fig7.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig7)










def map_u():
    map_users_df = pd.read_sql('map_users', engine)

    states = map_users_df['States'].unique()
        
    row1 = st.columns(2)
    row2 = st.columns(2)
    row3 = st.columns(2)
    row4 = st.columns(3)
    row5 = st.columns(2)
    

    with row1[0]:
        selected_state = st.selectbox("Select a state", ['All states'] + list(states))
        
    
    with row1[1]:
        sub_columns = st.columns(2)
        
        with sub_columns[0]:
            pass
        
        with sub_columns[1]:
            coloum1 = map_users_df["Years"].unique()
            selected_year = st.selectbox("Select a year", coloum1)

    with row2[0]:
        MUS = map_users_df[map_users_df["Years"]==selected_year]

        MU_S_Map = MUS.groupby('States')[['Reg_users', 'App_opens']].sum()
        MU_S_Map.reset_index(inplace = True)

        if selected_state == 'All states':
            stateMU = MU_S_Map
        else:
            stateMU = MU_S_Map[MU_S_Map['States'] == selected_state]
                
        fig1 = px.choropleth(
            stateMU,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='Reg_users',
            color_continuous_scale='turbo',
            range_color = (MU_S_Map['Reg_users'].min(), MU_S_Map['Reg_users'].max()),
            title = 'Registered users'
            )

        fig1.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig1)

    with row2[1]:
        MUS = map_users_df[map_users_df["Years"]==selected_year]

        MU_S_Map = MUS.groupby('States')[['Reg_users', 'App_opens']].sum()
        MU_S_Map.reset_index(inplace = True)
        if selected_state == 'All states':
            stateMU = MU_S_Map
        else:
            stateMU = MU_S_Map[MU_S_Map['States'] == selected_state]
                

        fig2 = px.choropleth(
            stateMU,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='App_opens',
            color_continuous_scale='turbo',
            range_color = (MU_S_Map['App_opens'].min(), MU_S_Map['App_opens'].max()),
            title = 'Number of app open'
            )

        fig2.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig2)

    if selected_state == 'All states':
            pass

    else:
        with row3[0]:

                MU_D = map_users_df.query('States == @selected_state and Years == @selected_year')


                fig3 = px.bar(MU_D, y=MU_D['District_name'].apply(lambda x: x.replace("district", "")), 
                                x=['Reg_users'],
                                color='Quater',
                                barmode='stack', orientation='h',
                                title='Registered users by District',
                                labels={'value': 'Transaction', 'variable': 'Type'})

                fig3.update_layout(xaxis_title='Registered users', title_x=0.35, yaxis_title='Districts', legend_title='Type', height= 700)

                st.plotly_chart(fig3)
        
        with row3[1]:
            
                MU_D_M = map_users_df.query('States == @selected_state and Years == @selected_year')


                fig4 = px.bar(MU_D_M, y=MU_D_M['District_name'].apply(lambda x: x.replace("district", "")), 
                                x=['App_opens'],
                                color='Quater',
                                barmode='stack', orientation='h',
                                title='Number of app open by District',
                                labels={'value': 'Transaction', 'variable': 'Type'})

                fig4.update_layout(xaxis_title='Number of app open', title_x=0.35, yaxis_title='Districts', legend_title='Type', height= 700)

                st.plotly_chart(fig4)

        with row4[1]:
            selected_dic = st.selectbox("Select a district", sorted(MU_D_M['District_name'].unique()))

            MU_D_bar = MU_D_M.query('District_name == @selected_dic')
        
        with row5[0]:
            fig5 = px.bar(MU_D_bar, y='Reg_users', 
                                x='Quater',
                                color='Quater',
                                barmode='stack',
                                title='Registered users by District',
                                labels={'value': 'Transaction', 'variable': 'Type'})

            fig5.update_layout(xaxis_title='Quater', title_x=0.35, yaxis_title='Registered users', legend_title='Type')

            st.plotly_chart(fig5)

        with row5[1]:
            fig6 = px.bar(MU_D_bar, y='App_opens', 
                                x='Quater',
                                color='Quater',
                                barmode='stack',
                                title='Number of app open by District',
                                labels={'value': 'Transaction', 'variable': 'Type'})

            fig6.update_layout(xaxis_title='Quater', title_x=0.35, yaxis_title='Number of app open', legend_title='Type')

            st.plotly_chart(fig6)






def top_u():
    top_user_df = pd.read_sql('top_user', engine)

    states = top_user_df['States'].unique()

    row1 = st.columns(2)
    row2 = st.columns(2)
    row3 = st.columns(4)
    row4 = st.columns(2)
    
    

    with row1[0]:
        selected_state = st.selectbox("Select a state", ['All states'] + list(states))
        
    
    with row1[1]:
        sub_columns = st.columns(2)
        
        with sub_columns[0]:
            pass
        
        with sub_columns[1]:
            coloum1 = top_user_df["Years"].unique()
            selected_year = st.selectbox("Select a year", coloum1)

    with row2[0]:
        TUS = top_user_df[top_user_df["Years"]==selected_year]

        TU_S_Map = TUS.groupby('States')['Reg_users'].sum()
        TU_S_Map = TU_S_Map.to_frame().reset_index()

        fig1 = px.choropleth(
            TU_S_Map,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='Reg_users',
            color_continuous_scale='turbo',
            range_color = (TU_S_Map['Reg_users'].min(), TU_S_Map['Reg_users'].max()),
            title = 'Transacion count'
            )

        fig1.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig1)

    if selected_state == 'All states':
        pass

    else:

        with row2[1]:
            TUS = top_user_df[top_user_df["Years"]==selected_year]

            TU_S_Map = TUS.groupby('States')['Reg_users'].sum()
            TU_S_Map = TU_S_Map.to_frame().reset_index()
            
            stateTU = TU_S_Map[TU_S_Map['States'] == selected_state]
                    

            fig2 = px.choropleth(
                stateTU,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='States',
                color='Reg_users',
                color_continuous_scale='turbo',
                range_color = (TU_S_Map['Reg_users'].min(), TU_S_Map['Reg_users'].max()),
                title = 'Transacion amount'
                )

            fig2.update_geos(fitbounds="locations", visible=False)

            st.plotly_chart(fig2)

        

            with row3[1]:
                selected_quater = st.selectbox("Select a quater", top_user_df['Quater'].unique())

                
            with row4[0]:

                    TU_Pin = top_user_df.query('States == @selected_state and Years == @selected_year and Quater == @selected_quater').reset_index(drop=True)

                    st.write(TU_Pin[['Pincodes', 'Reg_users']])

                    fig3 = px.bar(TU_Pin, x ='Reg_users',
                                            y= 'Pincodes',
                                            orientation='h',
                                            title='Top 10 Transaction count'
                                            )
                   
                    fig3.update_layout(xaxis_title='Reg_users',title_x=0.35,  yaxis_title='Pincodes')

                    st.plotly_chart(fig3)
            
            with row4[1]:
                pass
    






#streamlit

st.set_page_config(
    page_title="Phonepe Pulse Data Visualization",
    page_icon=":books:",
    layout="wide",
    #initial_sidebar_state="collapsed",
    menu_items={
        'About': """Welcome to the Phonepe Pulse Data Visualization project!"""
    }
)


def styled_text(text, color="black", font_size=None, alignment="left", bold=False, background_color=None, bullet_points=False):
    style = ""
    if color:
        style += f"color: {color};"
    if font_size:
        style += f"font-size: {font_size}px;"
    if alignment:
        style += f"display: block; text-align: {alignment};"
    if bold:
        style += "font-weight: bold;"
    if background_color:
        style += f"background-color: {background_color};"

    if bullet_points:
        text = "<ul>" + "".join([f"<li>{line}</li>" for line in text.split("\n")]) + "</ul>"

    if style:
        text = f'<span style="{style}">{text}</span>'
    return text


def home_page():

    st.markdown(styled_text("Welcome to Phonepe Pulse Data Visualization", 
                            color="green", font_size="50", alignment="center", bold = True), unsafe_allow_html=True)






page = st.sidebar.radio(":blue[Choose your page]", ["Home page", "Transacions", "Users"])

if page == "Home page":
    home_page()


if page == "Transacions":

    st.markdown("Hi")

    choice1 = st.selectbox("", [
                        "1. Aggregated values of various payment categories",
                        "2. Total values at the State and District levels",
                        '3. Totals of top States / Districts /Pin Codes'
    ] )

    if choice1 == "1. Aggregated values of various payment categories":
        agg_t()

    if choice1 == "2. Total values at the State and District levels":
        map_t()

    if choice1 == "3. Totals of top States / Districts /Pin Codes":
        top_t()


if page == "Users":

    st.markdown("Hi")

    choice2 = st.selectbox("", [
                        "1. Aggregated values of various payment categories",
                        "2. Total values at the State and District levels",
                        '3. Totals of top States / Districts /Pin Codes'
    ] )

    if choice2 == "1. Aggregated values of various payment categories":
        agg_u()

    if choice2 == "2. Total values at the State and District levels":
        map_u()

    if choice2 == "3. Totals of top States / Districts /Pin Codes":
        top_u()
    