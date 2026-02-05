#To-Do
#Add Event Costs breakdown - average rates for each cost center? average per person? 
#addd pdf link
#add - big initiatives/updates this year 
#Members per chapter on the dues table? 
#Chapter account balances Jan 2023 - Jan 2026 - average $ + % growth per year 
#one chapter slide to control ALL tables referring to chapters at once, section break titled "Chapter View" 
#bother adding 2022 or no? If not, increase the slider minimum.
#mobile-friendly aspect ratio
#green page, green widgets, more arty overall
#Where our members are based, heat map or something, highlight growth 


import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="PNWSU 2026", page_icon="📊")
st.title("PNWSU 2026 Report")

st.image("data/Greyscale_Logo.png")

st.write(
    """
    This is the PNWSU Treasurer's Dashboard for the 2026 Annual Conference - To help members dynamically view and visualize important staff union financial data.
    """
)
st.write(
    """
    Este es un reporte para los miembros de PNWSU quien estan interesado en el salud financial de sus sindicato. Se ofrece datos dynamicos para consideracion mas profunda. 
    """
)

if st.button("Table", width="stretch"):
    st.markdown(st.table({'Year':['Income', 'Expenses'], '2025':[479040.73, 302795.81],'2024':[376153.56, 61651.26],'2023':[352818.17, 157027.20]}))  




st.write(
    """
    PNWSU 2024-2026 Total Income and Expenses
    """
)

st.table({'Year':['Income', 'Expenses'], '2025':[479040.73, 302795.81],'2024':[376153.56, 61651.26],'2023':[352818.17, 157027.20]})  


def load_data2():
    df2 = pd.read_csv('data/pnwsu_dues.csv')
    return df2


df2 = load_data2()

dues = st.multiselect(
    "Dues Income",
    df2.Chapter.unique(),
    ['BSSU',
'CWA9009',
'KIWA',
'LA Labor Fed',
'NVLF',
'PROTEC17',
'SEIU121RN',
'SEIU2015',
'SEIU221',
'SEIU925',
'UDWA',
'UFCW21',
'UFCW3000',
'UFCW367',
'Working WA-FWC'
],
)


# Show a slider widget with the years using `st.slider`.
years2 = st.slider("Year", 2023, 2025, (2024, 2025),key="dues")

# Filter the dataframe based on the widget input and reshape it.
df_filtered2 = df2[(df2["Chapter"].isin(dues)) & (df2["Year"].between(years2[0], years2[1]))]
df_reshaped2 = df_filtered2.pivot_table(
    index="Year", columns="Chapter", values="Total", aggfunc="sum", fill_value=0
)
df_reshaped2 = df_reshaped2.sort_values(by="Year", ascending=False)


# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped2,
    use_container_width=True,
    column_config={"Year": st.column_config.TextColumn("Year")},
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv('data/pnwsu_gf_exp.csv')
    return df


df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
expenses = st.multiselect(
    "Expense Types",
    df.Expense.unique(),
    ['Taxi',
'Arbitration',
'Subsciption Service',
'Travelperk',
'Venmo',
'Parking',
'Food',
'Office Supplies',
'Database',
'Transaction Fees',
'Court Reporting',
'Accounting Services',
'Hotel',
'Labor Notes',
'Misc',
'Printing'
],
)

# Show a slider widget with the years using `st.slider`.
years = st.slider("Year", 2022, 2025, (2024, 2025),key="exp")

# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["Expense"].isin(expenses)) & (df["Year"].between(years[0], years[1]))]
df_reshaped = df_filtered.pivot_table(
    index="Year", columns="Expense", values="Total", aggfunc="sum", fill_value=0
)
df_reshaped = df_reshaped.sort_values(by="Year", ascending=False)


# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"Year": st.column_config.TextColumn("Year")},
)

# Display the data as an Altair chart using `st.altair_chart`.
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="Year", var_name="Expense", value_name="Total"
)
chart = (
    alt.Chart(df_chart)
    .mark_bar(size=50)
    .encode(
        x='Year:N',
        y='Total:Q',
        color="Expense:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)
