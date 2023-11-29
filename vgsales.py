from urllib.error import URLError
import streamlit as st
import numpy as np, pandas as pd
import altair as alt

@st.cache_data
def get_data():
    path_ = "dataset/vgsales.csv"
    df = pd.read_csv(path_)
    #drop NA on year and publisher
    df.dropna(inplace=True)
    # cleaning year column
    df.Year = df.Year.astype('str')
    df.Year = df.Year.str.replace('.0','')
    return df

try:
    df = get_data()
    st.title("""video games sales analysis""")


    st.dataframe(df.head(3))
    # st.write(df.columns)
    # total sales metrics
    global_sales = np.round(np.sum(df.Global_Sales),2)
    eu_sales =  np.round(np.sum(df.EU_Sales),2)
    na_sales =  np.round(np.sum(df.NA_Sales),2)
    jp_sales =  np.round(np.sum(df.JP_Sales),2)
    other_sales =  np.round(np.sum(df.Other_Sales),2)

    # create a series of column
    col1, col2, col3, = st.columns(3)
    col4, col5 = st.columns(2)

    # card
    col1.metric("Global Sales Total",global_sales,"USD")
    col2.metric("Global Sales Total",na_sales,"USD")
    col3.metric("Global Sales Total",eu_sales,"USD")
    col4.metric("Global Sales Total",jp_sales,"USD")
    col5.metric("Global Sales Total",other_sales,"USD")

    # filters (platforms)
    st.write(" # select a platform and Genre")
    col6, col7 = st.columns(2)
    platforms = df.Platform.unique()
    selected_platform = col6.multiselect(
        "platforms",platforms,[platforms[0],platforms[1]])
    

    # fliter (genre)
    genre = df.Genre.unique()
    selected_genre = col7.multiselect(
        "Genre", genre,[genre[0], genre[1]]
    )


    filtered_data = df[df["Platform"].isin(selected_platform) &
                       df["Genre"].isin(selected_genre)] 

    # table
    if not selected_platform or selected_genre:
        st.error("please select both filters from")
    else:
        st.write("""Filtered result obtained""")
        st.table(filtered_data.head())

    # table end

    # plots
    # bar chart
    st.write("# Top platform chart")
    bar0 = df.groupby(['Platform'])['Global_Sales'].sum().nlargest(n=10).sort_values(ascending=False)
    st.bar_chart(bar0, color="#d4af37",)

    st.write(" # Bar chart from filtered result")
    st.write(""" ## Global Sales per Platform """)
    bar1 = df.groupby(['Platform'])['Global_Sales'].sum().sort_values(ascending=True)
    st.bar_chart(bar1, color="#d4af37", width=20, height=400)

        
       
    # line chart
    st.write(""" ## Global sales over Time """)
    chart = (
             alt.Chart(filtered_data)
            .mark_area()
            .encode(
               x="Year",
               y=alt.Y("Global_Sales", stack=None),
            )
        )
    st.altair_chart(chart, use_container_width=True)
    
# area chart
    st.write(""" ## Global sales over Time """)
    chart = (
             alt.Chart(filtered_data)
            .mark_area(opacity=0.3)
            .encode(
               x="Year",
               y=alt.Y("Global_Sales", stack=None),
            )
        )
    st.altair_chart(chart, use_container_width=True)
    
    # countries = st.multiselect(
    #     "Choose countries", list(df.index), ["China", "United States of America"]
    # )
    # if not countries:
    #     st.error("Please select at least one country.")
    # else:
    #     data = df.loc[countries]
    #     data /= 1000000.0
    #     st.write("### Gross Agricultural Production ($B)", data.sort_index())

    #     data = data.T.reset_index()
    #     data = pd.melt(data, id_vars=["index"]).rename(
    #         columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
    #     )
    #     chart = (
    #         alt.Chart(data)
    #         .mark_area(opacity=0.3)
    #         .encode(
    #             x="year:T",
    #             y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
    #             color="Region:N",
    #         )
    #     )
    #     st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )

