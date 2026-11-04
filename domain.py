from dataclasses import dataclass
from datetime import date


@dataclass
class TransportRoute:
    id: int
    transport_type: str
    route_number: str
    introduction_date: date
    start_stop: str
    end_stop: str
    travel_time: int
    note: str | None = None


@dataclass
class Stop:
    id: int
    name: str
    address: str


@dataclass
class RouteStop:
    id: int
    route_id: int
    stop_id: int
    stop_order: int
