companies: list = []
employees: list = []
routes: list = []


class Company:
    def __init__(self, name: str, city: str, street: str):
        self.name = name
        self.city = city
        self.street = street
        self.clients = []


class Employee:
    def __init__(self, name: str, surname: str, city: str, street: str, company_name: str):
        self.name = name
        self.surname = surname
        self.city = city
        self.street = street
        self.company_name = company_name


class Route:
    def __init__(self, name: str, start_location: str, end_location: str, company_name: str):
        self.name = name
        self.start_location = start_location
        self.end_location = end_location
        self.company_name = company_name
