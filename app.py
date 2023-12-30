import streamlit as st
import pickle
import requests

st.set_page_config(
    page_title="Movie Recommendation",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

header_image_url = "Movie-img.png"  
width = 200  
aspect_ratio = 200 / 600

# Create two columns for side-by-side layout (col1 and col2)
col1, col2 = st.columns([2, 4])

# Column 1: Display the header image
with col1:
    st.image(header_image_url, width=width, use_column_width=True)

# Column 2: Movie Recommendation System
with col2:
    # Function to fetch the movie poster using TMDb API
    def fetch_poster(movie_id):
        api_key = 'c7ec19ffdd3279641fb606d19ceb9bb1'
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            movie_details = response.json()
            
            # Extract the poster_path from the movie_details
            poster_path = movie_details['poster_path']
            
            # Construct the full poster URL
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            
            return poster_url
        except requests.exceptions.RequestException as e:
            print(f"Error fetching poster for movie_id {movie_id}: {e}")
            return None

    # Load the model and movie data
    movies = pickle.load(open("movies_list.pkl", 'rb'))
    similarity = pickle.load(open("similarity.pkl", 'rb'))
    movies_list = movies['original_title'].values

    # Streamlit app header
    # Centered header using HTML and CSS
    st.markdown("""
        <div style="text-align:center;">
            <h1>Movie Recommendation System</h1>
        </div>
    """, unsafe_allow_html=True)

    # Center-align the "Select a movie" label using HTML and CSS
    st.markdown("""
        <div style="text-align:center;">
            <h6>Elevate Your Movie Experience with Personalized Picks! </h6>
        </div>
    """, unsafe_allow_html=True)

    # Create a dropdown to select a movie
    selected_movie = st.selectbox("", movies_list, key="movie_dropdown")

    # Center-align the dropdown using HTML and CSS
    st.markdown("""
        <style>
            div[data-baseweb="select"] {
                text-align: center !important;
                width: 300px;
                margin: 0 auto;
            }
        </style>
    """, unsafe_allow_html=True)

    # Function to recommend movies based on similarity
    def recommend(movie):
        index = movies[movies['original_title'] == movie].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
        recommend_movie = []
        recommend_poster = []
        for i in distance[1:9]:
            movies_id = movies.iloc[i[0]].id
            recommend_movie.append(movies.iloc[i[0]].original_title)
            recommend_poster.append(fetch_poster(movies_id))
        return recommend_movie, recommend_poster

    # Center-align the "Recommend" button using HTML and CSS
    st.markdown("""
        <style>
            .stButton button {
                margin: 0 auto;
                display: block;
            }
        </style>
    """, unsafe_allow_html=True)

    # Button to trigger movie recommendations
    if st.button("Recommend"):
        movie_name, movie_poster = recommend(selected_movie)

        for url in movie_poster:
            print(f"Poster URL: {url}")

# Recommendation Section (occupying 100% width)
with st.columns([1])[0] as col3:
    if "movie_name" in locals() and "movie_poster" in locals():
        # Calculate the number of columns based on the number of recommendations
        num_columns = len(movie_name)

        # Create columns for recommended movies and posters
        columns = st.columns(num_columns)

        for i in range(num_columns):
            with columns[i]:
                st.markdown(
                    f"""
                    <div class="movie-name" style="height: 50px; overflow: auto;">
                        {movie_name[i]}
                    </div>
                    <style>
                        .movie-name {{
                            font-size: 18px;
                            color: white;
                            margin-bottom: 10px;
                        }}
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                if movie_poster[i]:
                    # Display movie poster with styling and hover effect
                    st.markdown(
                        f"""
                        <div class="movie-card">
                            <img class="movie-poster" src="{movie_poster[i]}" alt="{movie_name[i]}">
                        </div>
                        <style>
                            .movie-card {{
                                position: relative;
                                overflow: hidden;
                                border-radius: 10px;
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                transition: transform 0.3s;
                            }}
                            .movie-poster {{
                                width: 100%;
                                height: auto;
                            }}
                            .movie-card:hover {{
                                transform: scale(1.1);
                            }}
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.text("No Poster Available")
