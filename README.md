# MovieSearch

MovieSearch is a Django-based web application that allows users to explore movies through a trending page, a search functionality, detailed movie information pages, and the ability to save their favorite movies.

## Features
- **Trending Page**: Displays the most popular movies currently trending.
- **Search Page**: Allows users to search for movies by title.
- **Details Page**: Provides detailed information about a selected movie, including cast, plot, and ratings.
- **Pagination**: Search results are paginated to improve user experience by displaying a limited number of results per page. Users can navigate through pages to view additional movies.
- **Favorites**: Users can add movies to their favorites. Favorite movies are stored for each user, allowing them to easily view and manage their collection of favorite films.

## Setup Instructions

### Prerequisites
1. Python (>=3.7)
2. Django (>=3.2)
3. OMDB API Key (You can obtain one from [OMDB API](http://www.omdbapi.com/apikey.aspx))

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/moviesearch.git
   cd moviesearch
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows, use `venv\\Scripts\\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations to set up the database:
   ```bash
   python manage.py migrate
   ``` 

5. Add your OMDB API key to `settings.py`:
   Inside `moviesearch/settings.py`, add the following line:
   ```python
   OMDB_API_KEY = "your_api_key"
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Open the app in your browser:
   Visit `http://127.0.0.1:8000/`.



## License
This project is licensed under the MIT License.

---
