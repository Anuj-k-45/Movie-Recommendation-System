import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f4b94585378e4eea6c9cfb2549a3d608"
    response = requests.get(url)
    data = response.json()  # Fix: added parentheses
    if "poster_path" in data:
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"  # Fix: single quotes inside f-string
    else:
        return "https://via.placeholder.com/500"  # Placeholder if no poster is found


def recommend(movie):
    movie_index = movies_df[movies_df["title"] == movie].index[0]
    distances = similarity[movie_index]
    
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []

    for i in movie_indices:
        movie_id = movies_df.iloc[i[0]].movie_id  # Fix: get the correct movie_id from DataFrame
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies.append(movies_df.iloc[i[0]].title)
    
    return recommended_movies, recommended_movies_poster

# Load the data
movies_df = pickle.load(open("movies.pkl", "rb"))  # Ensure it's a DataFrame with a column 'id'
movies_list = movies_df["title"].values
similarity = pickle.load(open("similarity.pkl", "rb"))

# Streamlit UI
st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies_list,
)

if st.button("Recommend"):
    recommendations, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write(recommendations[0])
        st.image(posters[0])

    with col2:
        st.write(recommendations[1])
        st.image(posters[1])

    with col3:
        st.write(recommendations[2])
        st.image(posters[2])

    with col4:
        st.write(recommendations[3])
        st.image(posters[3])

    with col5:
        st.write(recommendations[4])
        st.image([posters[4]])