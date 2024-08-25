# Movie Assistant

The **Movie Assistant** is an intelligent movie recommendation and information retrieval tool designed to enhance user interaction by leveraging the capabilities of a Large Language Model (LLM). This project is part of the LLM Zoomcamp and demonstrates the use of Retrieval-Augmented Generation (RAG) to provide detailed and contextually relevant movie-related information.

## Key Features

### Extensive Movie Database
The application utilizes a comprehensive dataset sourced from [Kaggle](https://www.kaggle.com/datasets/rajugc/imdb-movies-dataset-based-on-genre/data), which includes detailed information for each movie, such as:

- **Movie Name**: The title of the movie.
- **Year**: The release year of the movie.
- **Certificate**: The age rating of the movie (e.g., PG-13, R).
- **Runtime**: The duration of the movie in minutes.
- **Genre**: The genre(s) of the movie (e.g., Action, Drama, Comedy).
- **Rating**: The IMDb or similar platform rating.
- **Description**: A brief synopsis of the movie.
- **Director**: The name of the movie's director.
- **Star**: The lead actor or actress in the movie.
- **Votes**: The number of votes or reviews the movie has received.
- **Gross**: The box office earnings of the movie in USD.

### Intelligent Movie Assistant
The application leverages RAG to provide users with accurate and context-sensitive responses to queries related to movies. Whether a user is looking for a movie recommendation based on a particular genre, seeking information about a director’s filmography, or wanting to know the box office success of a movie, the assistant can retrieve and generate responses based on the available data.

### Seamless Integration of Retrieval and Generation
The RAG framework combines retrieval-based methods with generative models, ensuring that the responses are both factually accurate and fluently presented. The retrieval component accesses the structured movie data, while the generative model crafts user-friendly responses.

### Enhanced User Experience
With the ability to understand and respond to complex queries, the Movie Assistant RAG Application offers a more personalized and engaging user experience. It not only fetches specific information but can also provide insightful recommendations and comparisons between movies.

---

*Note: The movie dataset used in this project was taken from Kaggle and can be accessed [here](https://www.kaggle.com/datasets/rajugc/imdb-movies-dataset-based-on-genre/data).*