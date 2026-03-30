from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep
from typing import List

app = FastAPI()

@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    return db.get_sheep(id)

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