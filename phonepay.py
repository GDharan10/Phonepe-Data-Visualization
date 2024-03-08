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

agg_trans_df.query(' State == "Tamil Nadu" and Year == "2023" and Quater == 1 and Transacion_type == "Merchant payments" ')

fig = px.pie(agg_trans_df, names='Transacion_type', values='Transacion_count')


def agg_t():
    row1 = st.columns(3)
    row2 = st.columns(2)

    with row1[1]:
        fig3 = px.sunburst(agg_trans_df, path=['Transacion_type', 'Year'], values='Transacion_count')
        st.plotly_chart(fig3)
    
    with row1[2]:
        pass

    
    with row2[0]:
        fig1 = px.scatter(agg_trans_df, x='State', y='Transacion_count',color='Transacion_type',animation_frame="Year", range_y=[0, 1800000000])
        st.plotly_chart(fig1)
    
    with row2[1]:
        fig2 = px.bar(agg_trans_df, x='State', y='Transacion_amount',color='Transacion_type',animation_frame="Year", range_y=[0, 1800000000])
        st.plotly_chart(fig2)
        
def map_t():
    fig1 = px.scatter(map_trans_df, x='State', y='transaction_count',color='district_name',animation_frame="Year", range_y=[0, 1800000000])
    st.plotly_chart(fig1)
    fig2 = px.bar(map_trans_df, x='State', y='transaction_amount',color='district_name',animation_frame="Year", range_y=[0, 1800000000])
    st.plotly_chart(fig2)
    fig3 = px.sunburst(map_trans_df, path=['transacion_type', 'Year'], values='Transacion_count')
    st.plotly_chart(fig3)


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

    choice = st.selectbox("", [
                        "1. Aggregated values of various payment categories",
                        "2. Total values at the State and District levels",
                        '3. Totals of top States / Districts /Pin Codes'
    ] )

    if choice == "1. Aggregated values of various payment categories":
        agg_t()

    if choice == "2. Total values at the State and District levels":
        map_t()

    if choice == "3. Totals of top States / Districts /Pin Codes":
        pass


if page == "Users":

    st.markdown("Hi")

    choice = st.selectbox("", [
                        "1. Aggregated values of various payment categories",
                        "2. Total values at the State and District levels",
                        '3. Totals of top States / Districts /Pin Codes'
    ] )

    if choice == "1. Aggregated values of various payment categories":
        pass

    if choice == "2. Total values at the State and District levels":
        pass

    if choice == "3. Totals of top States / Districts /Pin Codes":
        pass
