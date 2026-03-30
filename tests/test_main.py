# Import TestClient to simulate API requests
from fastapi.testclient import TestClient

# Import the FastAPI app instance from the controller module
from main import app

# Create a TestClient instance for the FastAPI app
client = TestClient(app)

# Define a test function for reading a specific sheep
def test_read_sheep():
    # Send a GET request to the endpoint "/sheep/1"
    response = client.get("/sheep/1")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response JSON matches the expected data
    assert response.json() == {
        # Expected JSON structure
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

# Define a test function for adding a new sheep
def test_add_sheep():
    # TODO: Prepare the new sheep data in a directory format.
    sheep_data_name = {
        "id": 99,
        "name": "Suffolk",
        "breed": "Merino",
        "sex": "ram"
    }

    # TODO: Send a POST request to the endpoint "/sheep" with the new sheep data.
    #  Arguments should be your endpoint and a new sheep data.
    response = client.post("/sheep", json=sheep_data_name)

    # TODO: Assert that the response status code is 201 (Created).
    assert response.status_code == 201

    # TODO: Assert that thr response JSON matches the new sheep data.
    assert response.json() == sheep_data_name

    # TODO: Verify that the sheep was actually added to the database by retrieving the new sheep by ID.
    #  Include an assert statement to see if the new sheep data can be retrieved.
    added_sheep_id = response.json()["id"]
    verify_response = client.get(f"/sheep/{added_sheep_id}")

    assert verify_response.status_code == 200
    assert verify_response.json() == sheep_data_name

def test_read_all_sheep():
    response = client.get("/sheep/")
    assert response.status_code == 200

    # We know the fake DB starts with 6 sheep
    assert len(response.json()) >= 6

    # Verify the structure of the first item
    first_sheep = response.json()[0]
    assert "id" in first_sheep
    assert "name" in first_sheep

