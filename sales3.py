import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Sales Dashboard", layout="wide")
#st.title("Sales Dashboard")



with st.sidebar:
    selected=option_menu(menu_title="Navigation panel", options=["Sales","Orders"], icons=["house", "book"], menu_icon='cast', default_index=0)

if selected=="Sales":
    st.title("Sales Dashboard")
    df=pd.read_excel("Order Details.xlsx")
    df['Order_Date']= pd.to_datetime( df['Order_Date']).dt.strftime("%Y-%m-%d")
    
    df1=df.groupby(["Category","Sub-Category"], as_index=False).sum()
    category=st.sidebar.multiselect(label="Category", options=df1["Category"].unique(), default=df1["Category"].unique())
    selection=df1.query("Category==@category")
    kpi1,kpi2,kpi3=st.columns(3)
    kpi1.metric(label="Quantity", value=int(selection["Quantity"].sum()))
    kpi2.metric(label="Profit", value=int(selection["Profit"].sum()))
    kpi3.metric(label="Sales", value=int(selection["Amount"].sum()))

    df2=df.groupby(["Order_Date","Country", "Code"], as_index=False).sum()
    st.plotly_chart(px.choropleth(df2, locations="Code", color="Profit", hover_name="Country", animation_frame="Order_Date"))

    
    st.plotly_chart(px.bar(selection, x="Sub-Category", y="Profit", color="Category"))

if selected=="Orders":
    st.title("Orders Dashboard")
    df=pd.read_excel("List of Orders.xlsx")
    df['Order Date']= pd.to_datetime( df['Order Date']).dt.strftime("%Y-%m-%d")
    
    df2=df.groupby(["Order Date", "Category","Sub-Category"], as_index=False).sum()
    #st.write(df2)
    category=st.selectbox("Select A Product Category", pd.unique(df2["Category"]))
    df3=df2[df2["Category"]==category]
    st.plotly_chart(px.scatter(df3, x="Order Date", y="Amount", color="Sub-Category", size="Quantity"))
    df4=df.groupby(["Category", "Sub-Category"], as_index=False).sum()
    st.plotly_chart(px.bar(df4, x="Category", y="Amount", color="Sub-Category"))
   