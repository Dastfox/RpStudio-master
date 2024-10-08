# main.py

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import json
import os
from uuid import uuid4

app = FastAPI()

# Data storage (in-memory for simplicity)
scenarios = {}
images = {}


# Models
class Scenario(BaseModel):
    id: str
    content: dict


class ScenarioCreate(BaseModel):
    content: dict


class Image(BaseModel):
    id: str
    filename: str
    url: str


# Utility functions
def save_file(file_content, filename, directory):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    return file_path


# Scenarios CRUD
@app.post("/scenarios", response_model=Scenario)
async def create_scenario(scenario: ScenarioCreate):
    scenario_id = str(uuid4())
    new_scenario = Scenario(id=scenario_id, content=scenario.content)
    scenarios[scenario_id] = new_scenario

    # Save to file
    save_file(json.dumps(scenario.content).encode(), f"{scenario_id}.json", "scenarios")

    return new_scenario


@app.get("/scenarios", response_model=List[Scenario])
async def read_scenarios():
    return list(scenarios.values())


@app.get("/scenarios/{scenario_id}", response_model=Scenario)
async def read_scenario(scenario_id: str):
    if scenario_id not in scenarios:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenarios[scenario_id]


@app.put("/scenarios/{scenario_id}", response_model=Scenario)
async def update_scenario(scenario_id: str, scenario: ScenarioCreate):
    if scenario_id not in scenarios:
        raise HTTPException(status_code=404, detail="Scenario not found")
    updated_scenario = Scenario(id=scenario_id, content=scenario.content)
    scenarios[scenario_id] = updated_scenario

    # Update file
    save_file(json.dumps(scenario.content).encode(), f"{scenario_id}.json", "scenarios")

    return updated_scenario


@app.delete("/scenarios/{scenario_id}")
async def delete_scenario(scenario_id: str):
    if scenario_id not in scenarios:
        raise HTTPException(status_code=404, detail="Scenario not found")
    del scenarios[scenario_id]

    # Remove file
    os.remove(os.path.join("scenarios", f"{scenario_id}.json"))

    return {"message": "Scenario deleted successfully"}


# Images CRUD
@app.post("/images", response_model=Image)
async def create_image(file: UploadFile = File(...)):
    image_id = str(uuid4())
    filename = f"{image_id}.png"
    file_path = save_file(await file.read(), filename, "images")

    image_url = f"/images/{image_id}"
    new_image = Image(id=image_id, filename=filename, url=image_url)
    images[image_id] = new_image

    return new_image


@app.get("/images", response_model=List[Image])
async def read_images():
    return list(images.values())


@app.get("/images/{image_id}", response_model=Image)
async def read_image(image_id: str):
    if image_id not in images:
        raise HTTPException(status_code=404, detail="Image not found")
    return images[image_id]


@app.delete("/images/{image_id}")
async def delete_image(image_id: str):
    if image_id not in images:
        raise HTTPException(status_code=404, detail="Image not found")
    image = images[image_id]
    del images[image_id]

    # Remove file
    os.remove(os.path.join("images", image.filename))

    return {"message": "Image deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)