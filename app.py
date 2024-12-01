import streamlit as st
import pickle
import requests
import os


# Function to download similarity.pkl from Google Drive
def download_similarity_file():
    url = "https://drive.google.com/uc?id=1ki3ZByfEKMESN9z9UJIE8ZPl1_a02SnX&export=download"  # Replace with your modified Google Drive link
    response = requests.get(url, allow_redirects=True)

    # Save the file locally
    with open("similarity.pkl", "wb") as f:
        f.write(response.content)


# Check if similarity.pkl exists, if not, download it
if not os.path.exists("similarity.pkl"):
    st.write("Downloading similarity.pkl...")
    download_similarity_file()

# Load the movie list and similarity file after download
movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=97d5a607fcee6660300b0aa8ea11b164&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies_list.iloc[i[0]].movie_id

        recommended_movies.append(movies_list.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies_list['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    # Create columns explicitly using st.columns
    col1, col2, col3, col4, col5 = st.columns(5)

    if len(names) > 0:
        with col1:
            st.header(names[0])
            st.image(posters[0])

    if len(names) > 1:
        with col2:
            st.header(names[1])
            st.image(posters[1])

    if len(names) > 2:
        with col3:
            st.header(names[2])
            st.image(posters[2])

    if len(names) > 3:
        with col4:
            st.header(names[3])
            st.image(posters[3])

    if len(names) > 4:
        with col5:
            st.header(names[4])
            st.image(posters[4])
