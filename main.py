import re
from datetime import date
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from repository import PostgresRouteRepository, RouteRepository

app = FastAPI(title="City Transport API")

repository: RouteRepository = PostgresRouteRepository()


class TransportRoute(BaseModel):
    transport_type: str
    route_number: str = Field(pattern=r"^[0-9]{1,3}[А-Яа-яA-Za-z]?$")
    introduction_date: date
    start_stop: str
    end_stop: str
    travel_time: int = Field(gt=0, le=300)
    note: str | None = None


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "City Transport API is running"}


@app.get("/routes")
def get_routes() -> list[dict[str, Any]]:
    return repository.get_all()


@app.get("/routes/{route_id}")
def get_route(route_id: int) -> dict[str, Any]:
    route = repository.get_by_id(route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@app.post("/routes")
def create_route(route: TransportRoute) -> dict[str, Any]:
    if not re.fullmatch(r"[0-9]{1,3}[А-Яа-яA-Za-z]?", route.route_number):
        raise HTTPException(status_code=400, detail="Invalid route number")

    return repository.create(route.model_dump())


@app.put("/routes/{route_id}")
def update_route(route_id: int, route: TransportRoute) -> dict[str, Any]:
    updated = repository.update(route_id, route.model_dump())
    if updated is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return updated


@app.delete("/routes/{route_id}")
def delete_route(route_id: int) -> dict[str, int]:
    deleted = repository.delete(route_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return {"deleted_id": deleted["id"]}
