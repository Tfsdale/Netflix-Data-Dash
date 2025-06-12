
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
titles_df = pd.read_csv("netflix_titles.csv")
listed_in_df = pd.read_csv("Netflix_listed_in.csv")
director_df = pd.read_csv("Netflix_director.csv")
description_df = pd.read_csv("Netflix_description.csv")
country_df = pd.read_csv("Netflix_country.csv")
cast_df = pd.read_csv("Netflix_Cast.csv")

# Merge all datasets
df = titles_df.merge(listed_in_df, on='show_id', how='left') \
              .merge(director_df, on='show_id', how='left') \
              .merge(description_df, on='show_id', how='left') \
              .merge(country_df, on='show_id', how='left') \
              .merge(cast_df, on='show_id', how='left')

st.title("🎬 Netflix Global Content Dashboard")

# Map
country_counts = df['country_1'].value_counts().reset_index()
country_counts.columns = ['country', 'count']
fig_map = px.choropleth(country_counts, locations='country', locationmode='country names',
                        color='count', title='Total Titles by Country', color_continuous_scale='Plasma')
st.plotly_chart(fig_map)

# Top genres
top_genres = df['listed_in_1'].value_counts().nlargest(10).sort_values(ascending=True)
fig_genre = go.Figure(go.Bar(x=top_genres.values, y=top_genres.index, orientation='h',
                             marker_color='indianred'))
fig_genre.update_layout(title='Top 10 Genres')
st.plotly_chart(fig_genre)

# Ratings
rating_counts = df['rating'].value_counts().sort_values(ascending=False)
fig_rating = go.Figure(go.Bar(x=rating_counts.index, y=rating_counts.values, marker_color='gray'))
fig_rating.update_layout(title='Ratings Breakdown')
st.plotly_chart(fig_rating)

# Type breakdown
type_counts = df['type'].value_counts()
fig_type = go.Figure(go.Bar(x=type_counts.index, y=type_counts.values,
                            marker_color=['firebrick', 'darkgray']))
fig_type.update_layout(title='Movies vs TV Show Distribution')
st.plotly_chart(fig_type)

# Yearly trends
year_type_counts = df.groupby(['release_year', 'type']).size().unstack().fillna(0)
fig_time = px.area(year_type_counts, x=year_type_counts.index,
                   y=['Movie', 'TV Show'], title='Titles Over Time',
                   labels={'value': 'Count', 'release_year': 'Year'},
                   color_discrete_sequence=['firebrick', 'gray'])
st.plotly_chart(fig_time)
