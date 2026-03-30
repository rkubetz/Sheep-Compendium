from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep
from typing import List

app = FastAPI()


@app.get(path="/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    # Get the sheep from the database
    sheep = db.get_sheep(id)

    # If the sheep doesn't exist (is None), raise a 404 error!
    if sheep is None:
        raise HTTPException(status_code=404, detail="Sheep not found")

    return sheep

@app.post("/sheep/", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    # Check if the sheep ID already exists to avoid duplicates
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID already exists")

    # Add the new sheep to the database
    db.data[sheep.id] = sheep
    return sheep # Return the newly added sheep data

@app.get("/sheep/", response_model=list[Sheep])
def read_all_sheep():
    # Returns all sheep as a list
    return list(db.data.values())

@app.put("/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, sheep_data: Sheep):
    # Check if the sheep exists before updating
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep not found")

    # Update the dictionary
    db.data[id] = sheep_data
    return db.data[id]


@app.delete("/sheep/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sheep(id: int):
    # Check if the sheep exists before deleting
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep not found")

    # Delete from the dictionary
    del db.data[id]
    # No return needed for 204 No Content