import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.title("Hello, Streamlit!")
st.header("Welcome to Streamlit")
st.subheader("This is a subheader")
st.text("This is some text.")
st.markdown("This is **Markdown** text.")
st.caption("This is a caption.")
st.code("print('Hello, Streamlit!')", language="python")
st.divider()
st.image('static/photo.png', caption='Streamlit Image' , width = 900)
st.divider()
st.header('Dataframe Section')
df = pd.DataFrame({
    'Column 1': [1, 2, 3, 4],
    'Column 2': ['A', 'B', 'C', 'D']
})
st.dataframe(df)
st.divider()
st.table(df)
st.divider()
st.subheader('Metrics')
st.metric(label="Temperature", value="25 °C", delta="1.2 °C")
st.metric(label="Humidity", value="60 %", delta="-5 %")
st.divider()
st.subheader('Plotting')
charts_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(charts_data)
st.bar_chart(charts_data)
st.area_chart(charts_data)
st.divider()
st.header('Forms')
form_values = {
    'name': '',
    'age': 0,
    'gender': '',
    'dob': None,
    'city': '',
    'range' : (0, 100),
    'marks': 0,
}
with st.form(key='my_form'):
    name = st.text_input(label='Enter your name')
    age = st.number_input(label='Enter your age', min_value=0, max_value=120, value=0)
    gender = st.selectbox(label='Select your gender', options=['Male', 'Female', 'Other'])
    dob = st.date_input(label='Enter your date of birth')
    city = st.text_input(label='Enter your city')
    range = st.slider(label='Select a range', min_value=0, max_value=100, value=(0, 100))
    marks = st.number_input(label='Enter your marks', min_value=0, max_value=100, value=0)

    submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        if not all(form_values.values()):
            st.error("Please fill in all the fields.")
        else:
            st.success("Form submitted successfully!")
            st.write(f"Name: {name}")
            st.write(f"Age: {age}")
            st.write(f"Gender: {gender}")
            st.write(f"Date of Birth: {dob}")
            st.write(f"City: {city}")
            st.write(f"Range: {range}")
            st.write(f"Marks: {marks}")
def show_message():
    st.session_state.message = (
        "Form Submitted Successfully"
    )

with st.form("student_form"):

    name = st.text_input("Enter Name")

    age = st.number_input(
        "Enter Age",
        min_value=1,
        max_value=100
    )

    submit = st.form_submit_button(
        "Submit",
        on_click=show_message
    )

if "message" in st.session_state:
    st.success(st.session_state.message)

    st.write("Name:", name)
    st.write("Age:", age)

st.divider()

import streamlit as st

st.set_page_config(layout="wide")

st.title("ML Dashboard")

# Sidebar
st.sidebar.header("Navigation")

# Columns
col1, col2 = st.columns(2)

with col1:
    st.metric("Accuracy", "95%")

with col2:
    st.metric("F1 Score", "93%")

# Tabs
tab1, tab2 = st.tabs(["Charts", "Data"])

with tab1:
    st.write("Charts Here")

with tab2:
    st.write("Dataset Here")
st.divider()
@st.fragment()
def toggle_and_text():
    
    cols = st.columns(2)

    show_text = cols[0].toggle(
        "Show Text",
        key="toggle_text"
    )

    if show_text:
        cols[1].write(
            "This is some text that can be toggled on and off."
        )
@st.fragment()
def toggle_and_chart():
    cols = st.columns(2)
    cols[0].toggle("Show Chart", key="toggle_chart")
    if st.session_state.toggle_chart:
        data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c']
        )
        cols[1].line_chart(data)
toggle_and_text()
toggle_and_chart()