import streamlit as st
import pandas as pd
import numpy as np
from bike.predictor import ModelResolver
from bike.utils import load_object

model_resolver = ModelResolver()
transformer_path = model_resolver.get_latest_transformer_path()
model_path = model_resolver.get_latest_model_path()

transformer = load_object(file_path=transformer_path)
model = load_object(file_path=model_path)

season_dict = {'Spring':1, 'Summer':2, 'Fall':3, 'Winter':4}
weather_dict = {'Clear':1, 'Misty+Cloudy':2, 'Light Snow/Rain':3, 'Heavy Snow/Rain':4}
workingday_dict = {'weekend/holiday':0, 'Working day':1}
holiday_dict = {'Yes':1, 'No':0}


st.set_page_config(
    page_title="Bike Share Demand Prediction",
    page_icon="https://cdn-icons-png.flaticon.com/512/2119/2119039.png" ,
    layout="wide")

st.title('Bike Share Demand Prediction')

col1, col2 = st.columns([1, 1])

with col1:
    st.image('https://console.kr-asia.com/wp-content/uploads/2018/07/hellobike.jpg')
    st.markdown("<h1 style='font-size: 25px;'>Problem Statement:</h1>", unsafe_allow_html=True)
    st.write('Bike sharing systems are a new generation of traditional bike rentals where the whole process \
             from membership, rental and return back has become automatic. Through these systems, users are able \
             to easily rent a bike from a particular position and return back at another position.\
             Currently, there are about over 500 bike-sharing programs around the world which is composed of over\
             500 thousand bicycles. Today, there exists great interest in these systems due to their important role in\
             traffic, environmental and health issues. Apart from interesting real-world applications of bike sharing\
              systems, the characteristics of data being generated by these systems make them attractive for the research.')

with col2:
    col3, col4 = st.columns([1,1])
    with col3:
        weather = st.selectbox('Select the weather',
            ('Clear', 'Misty+Cloudy', 'Light Snow/Rain', 'Heavy Snow/Rain'))

        workingday = st.radio("Select the type of day",
            ('weekend/holiday','Working day'))

    with col4:
        season = st.selectbox('Select the season',
            ('Spring', 'Summer', 'Fall', 'Winter'))

        holiday = st.radio("Is the day is holiday",
            ('Yes','No'))
        
    hour = st.slider("Select the time of the day", 0, 23, 8)
    month = st.slider("Select the Month", 1,12,1)
    
    humidity = st.slider('Enter the humidity value', 0.0, 1.0,0.01 )

    temperature = st.slider('Enter the temperature value', 0.0, 1.0,0.01 )

    df = pd.DataFrame({'season':[season_dict[season]], 
                    'mnth':[month],
                    'hr':[hour],
                    'holiday':[holiday_dict[holiday]],
                    'workingday':[workingday_dict[workingday]],
                    'weathersit':[weather_dict[weather]],
                    'temp':[temperature],
                    'hum':[humidity]
                    })

    if st.button('Submit'):
        df.to_csv('input_data.csv', index=False)
        input_arr = transformer.transform(df)
        y_pred = model.predict(input_arr)
        y_pred_rounded = [round(pred, 2) for pred in y_pred]
        st.success(f'Demand for the day:  {y_pred_rounded[0]}')