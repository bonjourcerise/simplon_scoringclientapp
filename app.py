# import
import streamlit as st
import pandas as pd
import time
import pickle
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# config
st.set_page_config(page_title="Ai Credit Bank App", page_icon=":dollar:")

# load machine learning model
with open('model.pkl' , 'rb') as f:
    model_app = pickle.load(f)

# function pred status
def prediction_status(score):
    if score == 1:
        pred = 'rejected'
    else:
        pred = 'approved'
    return pred

# main page

#load data
uploaded_data = open("data/data_test.csv", "r")
df = pd.read_csv(uploaded_data)

# header with image and title
st.image("img/img_bank.gif")
st.title("AI Credit Bank 💰")

# welcome info
st.info("Welcome here !  Fill the fields in Genius App and hop, you can predict if your customer will have payment difficulties on a credit. You will also find statistics in the dashboard.")

#metrics
st.subheader("Statistics")
kpi_income = df['AMT_INCOME_TOTAL'].mean()
kpi_income = int(kpi_income)
kpi_client= len(df.index)
kpi_married = df['NAME_FAMILY_STATUS'].value_counts().Married
col1, col2, col3 = st.columns(3)
col1.metric(label="Outcome annual mean ($) 💵", value=kpi_income)
col2.metric(label="Clients number 🧑", value=kpi_client)
col3.metric(label="Married count 💍", value=kpi_married)

# config plotly colors
px.defaults.color_continuous_scale = px.colors.sequential.Purp

# viz 1
st.subheader("Education")
df_fig1 = df['NAME_EDUCATION_TYPE'].value_counts()
fig = px.bar(df_fig1, y="NAME_EDUCATION_TYPE", color="NAME_EDUCATION_TYPE", labels={"NAME_EDUCATION_TYPE": "Number of clients","index": "Education type"})
fig.update_layout(barmode="stack", xaxis={"categoryorder": "total descending"})
st.plotly_chart(fig)

# viz 2
st.subheader("Family Status")
df_fig2 = df["NAME_FAMILY_STATUS"].value_counts()
fig = px.bar(df_fig2, x="NAME_FAMILY_STATUS",color="NAME_FAMILY_STATUS", labels={"NAME_FAMILY_STATUS": "Number of clients","index": "Family Status"})
fig.update_layout(barmode="stack", xaxis={"categoryorder": "total descending"})
st.plotly_chart(fig)

# viz 3
st.subheader("Gender")
st.markdown("Men : 66% - Women : 34%")
df_fig3 = df["CODE_GENDER"].value_counts()
fig = px.pie(df_fig3, values='CODE_GENDER', color_discrete_sequence=px.colors.sequential.Purp)
st.plotly_chart(fig)

#sidebar
st.sidebar.title("Genius App")
# create boxes to enter data and make prediction 
gender = st.sidebar.selectbox("Gender", ("F", "M"))
age = st.sidebar.number_input("Age", min_value=18, max_value=99, step=1)
family_status = st.sidebar.selectbox("Family Status", ("Married", "Single / not married", "Separated", "Widow", "Civil marriage"))
child = st.sidebar.number_input("Children", step=1)
income = st.sidebar.number_input("Annual income", step=1)
credit= st.sidebar.number_input("Credit amount", step=1)
type_contract=st.sidebar.selectbox("Contract type",("Cash loans", "Revolving loans"))
education = st.sidebar.selectbox("Education", ("Secondary / secondary special", "Higher education", "Incomplete higher", "Lower secondary", "Academic degree"))
metier = st.sidebar.selectbox("Occupation", ("Laborers", "Core staff", "Sales staff","Managers","Drivers","Accountants","High skill tech staff",
"Medecine staff","Cooking staff","Security Staff","Cleaning staff","Private service staff","Secretaries","Waiters/barmen staff","Low-skill Laborers","Realty agents","HR staff","IT staff"))
    
# predict button
if st.sidebar.button("Submit & Predict"):

    with st.spinner('Tic tac, please wait'):
        time.sleep(10)
    
        # store inputs into dataframe
        X = pd.DataFrame([[gender, age, family_status,child,income,type_contract,credit,education,metier]], 
        columns = ["CODE_GENDER", "DAYS_BIRTH", "NAME_FAMILY_STATUS","CNT_CHILDREN", "AMT_INCOME_TOTAL","NAME_CONTRACT_TYPE", "AMT_CREDIT", "NAME_EDUCATION_TYPE", "OCCUPATION_TYPE"])
        # get pred
        prediction = model_app.predict(X)

        # output pred
        if  prediction_status(prediction) == 'rejected':
            st.sidebar.text(f"Score : {prediction}")
            st.sidebar.error('The credit will be {}'.format(prediction_status(prediction)))
        else:
            st.sidebar.text(f"Score : {prediction}")
            st.sidebar.success('The credit will be {}'.format(prediction_status(prediction)))