import tkintermapview

companies: list = []
employees: list = []
routes: list = []

def _build_headers(self, provider_key, **kwargs):
    return {"User-Agent": 'My User Agent 1.0'}


def get_coordinates(address: str):
    from geocoder.osm import OsmQuery
    OsmQuery._build_headers = _build_headers
    data = tkintermapview.convert_address_to_coordinates(address)
    if data is None:
        return [0, 0]
    latitude = float(data[0])
    longitude = float(data[1])
    return [latitude, longitude]


class Company:
    def __init__(self, name: str, city: str, street: str):
        self.name = name
        self.city = city
        self.street = street
        self.coordinates = get_coordinates(f"{city}, {street}")
        self.marker = None
        self.clients = []


class Employee:
    def __init__(self, name: str, surname: str, city: str, street: str, company_name: str):
        self.name = name
        self.surname = surname
        self.city = city
        self.street = street
        self.company_name = company_name
        self.coordinates = get_coordinates(f"{city}, {street}")
        self.marker = None


class Route:
    def __init__(self, name: str, start_location: str, end_location: str, company_name: str):
        self.name = name
        self.start_location = start_location
        self.end_location = end_location
        self.company_name = company_name
