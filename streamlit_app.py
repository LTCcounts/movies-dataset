import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Overhead", page_icon="📊")
st.title("Overhead Costs")
st.write(
    """
    This app visualizes data from [The Movie Database (TMDB)](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
    It shows which movie genre performed best at the box office over the years. Just 
    click on the widgets below to explore!
    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    #df = pd.read_csv(r'C:\Users\StashaL\Dropbox\PC\Desktop\pnwsu_overhead.csv')
    df = pd.read_csv('data/pnwsu_overhead1.csv')
    return df


df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
#all instances of 'genres' should be changed to 'expenses'
expenses = st.multiselect(
    "Expense",
    df.Expense.unique(),
    ['BLUEHOST.COM',
'GOOGLE WORKSPACE',
'ELECTIONRUNNER.COM',
'SHOPIFY',
'UNIONIMPACT HTTPSUNIONIMP WA',
'SURVEYMONKEY',
'ZOOM',
'JOTFORM INC',
'MICROSOFT 365',
'Ullico Insurance',
'Online Store (T-Shirts)',
'Printing',
'TravelPerk Fees'
],
)

# Show a slider widget with the years using `st.slider`.
years = st.slider("Years", 2022, 2025, (2024, 2025))

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
    .mark_line()
    .encode(
        x=alt.X("Year:N", title="Year"),
        y=alt.Y("Total:Q", title="Total ($)"),
        color="Expense:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)
