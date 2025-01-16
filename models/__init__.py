from abc import ABC, abstractmethod
from configparser import ConfigParser


class Seat:
    # Useless thing
    is_available = True


# ---------------------------------------------------------------------------


class Carriage(ABC):
    def __init__(self, seats, price):
        self.seats = seats
        self.price = price


class SeatCarriage(Carriage):
    def __init__(self, seats=60, price=500):
        super().__init__(seats, price)

    def __repr__(self):
        return f"Сидячий вагон: {self.seats} мест, цена: {self.price} руб."


class EconomCarriage(Carriage):
    def __init__(self, seats=30, price=1000):
        super().__init__(seats, price)

    def __repr__(self):
        return f"Эконом вагон: {self.seats} мест, цена: {self.price} руб."


class CoupeCarriage(Carriage):
    def __init__(self, seats=20, price=2000):
        super().__init__(seats, price)

    def __repr__(self):
        return f"Купейный вагон: {self.seats} мест, цена: {self.price} руб."


class FirstClassCarriage(Carriage):
    def __init__(self, seats=10, price=5000):
        super().__init__(seats, price)

    def __repr__(self):
        return f"СВ: {self.seats} мест, цена: {self.price} руб."


# ---------------------------------------------------------------------------


class Train:
    number: int
    carriages: dict[int, Carriage]

    def seats(self):
        return sum([carriage.seats for carriage in self.carriages.values()])

    def __init__(self, number, carriages):
        self.number = number
        self.carriages: carriages

    def __repr__(self):
        pretty = "\n".join([str(carriage) for carriage in self.carriages])
        return f"Номер поезда: {self.number}\n{pretty}"


# ---------------------------------------------------------------------------


class Route:
    timing: str
    train: Train

    def __init__(self, timing, train):
        self.timing = timing
        self.train = train

    def __repr__(self):
        return f"Время отправления: {self.timing}\т{self.train}"


# ---------------------------------------------------------------------------


class TicketOffice:
    def __init__(self):
        self.stations: dict[int, str] = {}
        self.routes: dict[int, Route] = {}
        self.trains: dict[str, Train] = {}
        self.schedule: dict[int, dict[int, int]] = {}

        self.parser: ConfigParser | None = None

        self.load()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def load(self):
        self.load_stations()
        self.load_routes()

    def load_stations(self):
        raw = open("Stations.conf", "r", encoding="utf-8")

        for rawline in raw:
            rawline = rawline.split(" ")
            self.stations[rawline[0]] = " ".join(rawline[1:])

        raw.close()

    def load_carriages(self, number):
        self.parser = ConfigParser()
        self.parser.read(f"Train{number}.ini", encoding="utf-8")

        carriages = {
            "seat": [],
            "econom": [],
            "coupe": [],
            "first": [],
        }

        for carriage_type in self.parser["CountCarriages"]:
            count = int(self.parser["CountSeatCarriages"][carriage_type])

            for _ in range(count):
                if carriage_type == "SeatCarriage":
                    seats = int(self.parser["CountSeatCarriages"]["SeatCarriage"])
                    price = int(self.parser["PriceCarriages"]["SeatCarriage"])
                    carriages["seat"].append(SeatCarriage(seats, price))
                elif carriage_type == "EconomCarriage":
                    seats = int(self.parser["CountSeatCarriages"]["EconomCarriage"])
                    price = int(self.parser["PriceCarriages"]["EconomCarriage"])
                    carriages["econom"].append(EconomCarriage(seats, price))
                elif carriage_type == "CoupeCarriage":
                    seats = int(self.parser["CountSeatCarriages"]["CoupeCarriage"])
                    price = int(self.parser["PriceCarriages"]["CoupeCarriage"])
                    carriages["coupe"].append(CoupeCarriage(seats, price))
                elif carriage_type == "FirstClassCarriage":
                    seats = int(self.parser["CountSeatCarriages"]["FirstClassCarriage"])
                    price = int(self.parser["PriceCarriages"]["FirstClassCarriage"])
                    carriages["first"].append(FirstClassCarriage(seats, price))

    def load_train(self, number):
        self.parser = ConfigParser()
        self.parser.read("Route.ini", encoding="utf-8")

        return Train(
            number,
            self.load_carriages(number),
        )

    def load_routes(self):
        self.parser = ConfigParser()
        self.parser.read("Route.ini", encoding="utf-8")

        for key in self.parser["Shedule"]:
            self.routes[int(key)] = Route(
                self.parser["Shedule"][key], self.load_train(int(key))
            )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_stations(self):
        return self.stations

    def get_route(self, route_id):
        return self.routes[route_id]

    def get_routers(self):
        return self.routes

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def buy_ticket(self, route_id, carriage_type):
        self.trains.get(route_id).carriages[carriage_type][0].seats -= 1
