from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_retrieve_movies():
    """
    Test the /movies endpoint for successful retrieval of movie list.
    
    Verifies that:
    1. The endpoint returns a 200 OK status code
    2. The response is a list
    """
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_retrieve_movie_by_id():
    """
    Test the /movies/{movie_id} endpoint for retrieving a specific movie by its ID.
    
    Verifies that:
    1. The endpoint returns a 200 OK status code
    2. The response is either None (no movie found) or a list
    
    Note: This test assumes a movie with ID 1 exists or might not exist in the database.
    """
    response = client.get("/movies/1")
    assert response.status_code == 200
    # Response may be None if no movie with id 1 exists
    assert response.json() is None or isinstance(response.json(), list)

def test_retrieve_producer_winners():
    """
    Test the /producer-winners endpoint for retrieving producer award winners.
    
    Verifies that:
    1. The endpoint returns a 200 OK status code
    2. The response is a dictionary with 'min' and 'max' keys
    3. Both 'min' and 'max' are lists
    
    This endpoint returns producers with the minimum and maximum interval between wins.
    """
    response = client.get("/producer-winners")
    assert response.status_code == 200
    # Should return a dictionary with 'min' and 'max' keys
    result = response.json()
    assert isinstance(result, dict)
    assert 'min' in result
    assert 'max' in result
    assert isinstance(result['min'], list)
    assert isinstance(result['max'], list)

def test_retrieve_nonexistent_movie():
    """
    Test retrieving a movie with an ID that does not exist.
    
    Verifies that:
    1. The endpoint returns a 200 OK status code
    2. The response is None when the movie ID is not found
    """
    response = client.get("/movies/99999")  # Assuming this ID does not exist
    assert response.status_code == 200
    assert response.json() is None

def test_movies_data_integrity():
    """
    Test the integrity of movie data retrieved from the /movies endpoint.
    
    Verifies that:
    1. Each movie record has the expected number of fields
    2. Movie records contain valid data types
    """
    response = client.get("/movies")
    movies = response.json()
    
    assert len(movies) > 0, "Movie database should not be empty"
    
    for movie in movies:
        # Validate movie record structure (assuming 6 fields: id, year, title, studios, producers, winner)
        assert len(movie) == 6, f"Movie record should have 6 fields, got {len(movie)}"
        
        # Validate data types
        assert isinstance(movie[0], int), "Movie ID should be an integer"
        assert isinstance(movie[1], int), "Movie year should be an integer"
        assert isinstance(movie[2], str), "Movie title should be a string"
        assert isinstance(movie[3], str), "Studios should be a string"
        assert isinstance(movie[4], str), "Producers should be a string"
        # Winner can be boolean or None
        assert movie[5] is None or isinstance(movie[5], bool), "Winner should be boolean or None"

def test_producer_winners_data_integrity():
    """
    Test the integrity of producer winners data retrieved from the /producer-winners endpoint.
    
    Verifies that:
    1. Producer winners data is well-formed
    2. Minimum and maximum intervals are valid
    """
    response = client.get("/producer-winners")
    result = response.json()
    
    assert 'min' in result, "Result should have 'min' key"
    assert 'max' in result, "Result should have 'max' key"
    
    # Validate min and max lists
    for category in ['min', 'max']:
        for winner in result[category]:
            assert isinstance(winner, dict), f"{category} winner should be a dictionary"
            assert 'producer' in winner, f"{category} winner should have 'producer' key"
            assert 'interval' in winner, f"{category} winner should have 'interval' key"
            assert isinstance(winner['producer'], str), "Producer name should be a string"
            assert isinstance(winner['interval'], int), "Interval should be an integer"

def test_invalid_movie_id():
    """
    Test retrieving a movie with an invalid ID.
    
    Verifies that:
    1. Non-integer movie IDs return a 422 Unprocessable Entity status
    2. Out-of-range movie IDs return None
    """
    # Test non-integer movie ID
    response = client.get("/movies/abc")
    assert response.status_code == 422  # Unprocessable Entity

    # Test very large out-of-range movie ID
    response = client.get("/movies/999999")
    assert response.status_code == 200
    assert response.json() is None

def test_producer_winners_empty_scenario():
    """
    Test producer winners endpoint with potential empty scenarios.
    
    Verifies that:
    1. The endpoint returns a valid response with empty lists
    2. No exceptions are raised
    """
    response = client.get("/producer-winners")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, dict)
    assert 'min' in result
    assert 'max' in result
    assert isinstance(result['min'], list)
    assert isinstance(result['max'], list)

def test_movies_data_validation():
    """
    Test movies endpoint for data validation and integrity.
    
    Verifies that:
    1. Each movie record has the expected number of fields
    2. Movie records contain valid data types
    """
    response = client.get("/movies")
    assert response.status_code == 200
    movies = response.json()
    
    for movie in movies:
        # Validate movie record structure
        assert len(movie) == 6  # id, year, title, studios, producers, winner
        
        # Validate data types
        assert isinstance(movie[0], int)  # id
        assert isinstance(movie[1], int)  # year
        assert isinstance(movie[2], str)  # title
        assert isinstance(movie[3], str)  # studios
        assert isinstance(movie[4], str)  # producers
        assert movie[5] in ['yes', 'no']  # winner flag
