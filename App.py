import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Database Manager", layout="wide")

# Sidebar: Upload data
st.sidebar.header("Data Source")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
#developer contact
st.sidebar.subheader("Developer")
st.sidebar.text("This is developed by Mr Suraj Kumar jha.He developed this using Data science library of python like pandas,matplotlib,streamlit and seaborn.This is very helpful and ploblem solving.")
st.sidebar.header("Developer Contact\nEmail: zhasuraj31@gmail.com")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state["data"] = df
else:
    st.info("Please upload a CSV file to get started.")
    st.stop()

df = st.session_state["data"]

# Sidebar: Filter Data
st.sidebar.header("Filters")
filters = {}
for column in df.select_dtypes(include=["object", "category"]).columns:
    options = st.sidebar.multiselect(f"Filter by {column}", df[column].unique())
    if options:
        filters[column] = options

# Apply Filters
filtered_df = df.copy()
for col, vals in filters.items():
    filtered_df = filtered_df[filtered_df[col].isin(vals)]

# Main Page
st.title("📊 Database Visualization & Management Tool")

st.subheader("1. Data Table")
st.dataframe(filtered_df)

# Summary
st.subheader("2. Summary Statistics")
st.write(filtered_df.describe(include='all'))

# Charts
st.subheader("3. Chart Visualization")

chart_type = st.selectbox("Choose chart type", ["Bar Chart", "Line Chart", "Scatter Plot"])
x_col = st.selectbox("X-axis", df.columns)
y_col = st.selectbox("Y-axis", df.select_dtypes(include=['number']).columns)

if chart_type == "Bar Chart":
    fig, ax = plt.subplots()
    filtered_df.groupby(x_col)[y_col].mean().plot(kind='bar', ax=ax)
    st.pyplot(fig)
elif chart_type == "Line Chart":
    fig, ax = plt.subplots()
    filtered_df.groupby(x_col)[y_col].mean().plot(kind='line', ax=ax)
    st.pyplot(fig)
elif chart_type == "Scatter Plot":
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_df, x=x_col, y=y_col, ax=ax)
    st.pyplot(fig)

# Data Entry Form
st.subheader("4. Add New Entry")
with st.form("data_entry_form", clear_on_submit=True):
    new_data = {}
    for col in df.columns:
        dtype = df[col].dtype
        if dtype == 'object' or dtype.name == 'category':
            val = st.text_input(f"{col}", "")
        elif dtype in ['int64', 'float64']:
            val = st.number_input(f"{col}", value=0.0)
        else:
            val = st.text_input(f"{col}", "")
        new_data[col] = val

    submitted = st.form_submit_button("Submit")
    if submitted:
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df, new_row], ignore_index=True)
        st.success("New entry added!")
        st.session_state["data"] = df
