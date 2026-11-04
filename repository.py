
from typing import Any, Protocol

import psycopg
from psycopg.rows import dict_row


DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/city_transport"


class RouteRepository(Protocol):
    def get_all(self) -> list[dict[str, Any]]: ...

    def get_by_id(self, route_id: int) -> dict[str, Any] | None: ...

    def create(self, data: dict[str, Any]) -> dict[str, Any]: ...

    def update(self, route_id: int, data: dict[str, Any]) -> dict[str, Any] | None: ...

    def delete(self, route_id: int) -> dict[str, Any] | None: ...


class PostgresRouteRepository:
    def __init__(self) -> None:
        self.database_url = DATABASE_URL

    def get_all(self) -> list[dict[str, Any]]:
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            return conn.execute(
                "SELECT * FROM transport_routes ORDER BY id"
            ).fetchall()

    def get_by_id(self, route_id: int) -> dict[str, Any] | None:
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            return conn.execute(
                "SELECT * FROM transport_routes WHERE id = %s",
                (route_id,),
            ).fetchone()

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            result = conn.execute(
                """
                INSERT INTO transport_routes
                (transport_type, route_number, introduction_date,
                 start_stop, end_stop, travel_time, note)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    data["transport_type"],
                    data["route_number"],
                    data["introduction_date"],
                    data["start_stop"],
                    data["end_stop"],
                    data["travel_time"],
                    data.get("note"),
                ),
            ).fetchone()

            if result is None:
                raise RuntimeError("Failed to create transport route")

            return result

    def update(
        self, route_id: int, data: dict[str, Any]
    ) -> dict[str, Any] | None:
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            return conn.execute(
                """
                UPDATE transport_routes
                SET transport_type = %s,
                    route_number = %s,
                    introduction_date = %s,
                    start_stop = %s,
                    end_stop = %s,
                    travel_time = %s,
                    note = %s
                WHERE id = %s
                RETURNING *
                """,
                (
                    data["transport_type"],
                    data["route_number"],
                    data["introduction_date"],
                    data["start_stop"],
                    data["end_stop"],
                    data["travel_time"],
                    data.get("note"),
                    route_id,
                ),
            ).fetchone()

    def delete(self, route_id: int) -> dict[str, Any] | None:
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            return conn.execute(
                """
                DELETE FROM transport_routes
                WHERE id = %s
                RETURNING id
                """,
                (route_id,),
            ).fetchone()
