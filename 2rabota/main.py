from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

class MovieBase(BaseModel):
    name: str
    description: str
    popularity: int

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

MOVIES_DB: List[Movie] = [
    Movie(id=1, name="Classic", description="A classic movie with a timeless story.", popularity=12),
    Movie(id=2, name="Fortuna", description="A thrilling adventure about a quest for fortune.", popularity=4),
    Movie(id=3, name="Epic", description="An epic tale of heroes and villains.", popularity=8),
    Movie(id=4, name="Mystery", description="A mysterious story that keeps you guessing until the end.", popularity=6),
    Movie(id=5, name="Romance", description="A heartwarming love story that will make you believe in love again.", popularity=10),
]

app = FastAPI()

@app.get("/")
def dead_root():
    return {}

@app.get("/movies/", response_model=List[Movie])
def read_movies():
    return MOVIES_DB

@app.get("/movies/{id}", response_model=Movie)
def read_movie(id: int):
    for movie in MOVIES_DB:
        if movie.id == id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

@app.post("/movies/", response_model=Movie)
async def create_movie(movie: MovieCreate):
    new_id = max(m.id for m in MOVIES_DB) + 1 if MOVIES_DB else 1
    new_movie = Movie(id=new_id, **movie.dict())
    MOVIES_DB.append(new_movie)
    return new_movie

@app.put("/movies/{movie_id}", response_model=Movie)
async def update_movie(movie_id: int, updated_movie: MovieCreate):
    for movie in MOVIES_DB:
        if movie.id == movie_id:
            movie.name = updated_movie.name
            movie.description = updated_movie.description
            movie.popularity = updated_movie.popularity
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

@app.delete("/movies/{movie_id}")
async def delete_movie(movie_id: int):
    global MOVIES_DB
    MOVIES_DB = [movie for movie in MOVIES_DB if movie.id != movie_id]
    return {"message": "Movie deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8002)