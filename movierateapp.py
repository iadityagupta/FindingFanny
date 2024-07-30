import streamlit as st
import pickle
import pandas as pd

# Load movie list and similarity matrix
try:
    movies = pickle.load(open("movies_list.pkl", 'rb'))
    similarity = pickle.load(open("similarity.pkl", 'rb'))
    movies_list = movies['title'].values
except FileNotFoundError as e:
    st.error("Required files not found. Please ensure 'movies_list.pkl' and 'similarity.pkl' are in the correct location.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the data: {e}")
    st.stop()

st.header("Movie Recommender System")

selectvalue = st.selectbox("Select a movie from the dropdown", movies_list)

# Drop unnecessary columns for indexing
new_data = movies.drop(columns=['overview', 'genre'])

def recommend(movie):
    try:
        # Get the index of the movie in new_data
        index = new_data[new_data['title'] == movie].index[0]
        
        # Debugging: print the index and shape of similarity matrix
        st.write(f"Movie index: {index}")
        st.write(f"Similarity matrix shape: {similarity.shape}")

        # Ensure the index is within the bounds of the similarity matrix
        if index >= similarity.shape[0]:
            raise IndexError(f"Index {index} is out of bounds for the similarity matrix with shape {similarity.shape}.")

        # Get the similarity distances
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        # Collect the recommended movie titles
        recommend_movie = [new_data.iloc[i[0]].title for i in distances[1:6]]
        
        return recommend_movie
    except IndexError as e:
        st.error(f"Movie '{movie}' not found in the database.")
        return []
    except KeyError as e:
        st.error(f"Error accessing similarity data for '{movie}'.")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return []

if st.button("Show Recommendations"):
    movie_names = recommend(selectvalue)
    if movie_names:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(movie_names[0])
        with col2:
            st.text(movie_names[1])
        with col3:
            st.text(movie_names[2])
        with col4:
            st.text(movie_names[3])
        with col5:
            st.text(movie_names[4])
    else:
        st.write("No recommendations found.")
