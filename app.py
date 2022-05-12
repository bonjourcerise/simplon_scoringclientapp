# import
import streamlit as st
import pandas as pd
import time
import pickle
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
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

# main function to define webpage
def main(): 
    # header with image and title
    st.image("img/img_bank.gif")
    st.title("AI Credit Bank 💰")

    # welcome info
    st.info("Welcome here !  Fill the fields and hop, you can predict if your customer will have payment difficulties on a credit. You will also find statistics in the dashboard.")

    # create boxes to enter data and make prediction 
    gender = st.selectbox("Gender", ("F", "M"))
    age = st.number_input("Age", min_value=18, max_value=99, step=1)
    family_status = st.selectbox("Family Status", ("Married", "Single / not married", "Separated", "Widow", "Civil marriage"))
    child = st.number_input("Children", step=1)
    income = st.number_input("Annual income", step=1)
    credit= st.number_input("Credit amount", step=1)
    type_contract=st.selectbox("Contract type",("Cash loans", "Revolving loans"))
    education = st.selectbox("Education", ("Secondary / secondary special", "Higher education", "Incomplete higher", "Lower secondary", "Academic degree"))
    metier = st.selectbox("Occupation", ("Laborers", "Core staff", "Sales staff","Managers","Drivers","Accountants","High skill tech staff",
    "Medecine staff","Cooking staff","Security Staff","Cleaning staff","Private service staff","Secretaries","Waiters/barmen staff","Low-skill Laborers","Realty agents","HR staff","IT staff"))
    
    # predict button
    if st.button("Submit & Predict"):

        with st.spinner('Tic tac, please wait'):
            time.sleep(10)
    
        # store inputs into dataframe
        X = pd.DataFrame([[gender, age, family_status,child,income,type_contract,credit,education,metier]], 
        columns = ["CODE_GENDER", "DAYS_BIRTH", "NAME_FAMILY_STATUS","CNT_CHILDREN", "AMT_INCOME_TOTAL","NAME_CONTRACT_TYPE", "AMT_CREDIT", "NAME_EDUCATION_TYPE", "OCCUPATION_TYPE"])
        # get pred
        prediction = model_app.predict(X)

        # output pred
        st.text(f"Score : {prediction}")
        st.success('Th credit will be {}'.format(prediction_status(prediction)))


if __name__=='__main__': 
    main()