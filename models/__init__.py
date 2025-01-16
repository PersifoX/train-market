from abc import ABC, abstractmethod
from configparser import ConfigParser


class Seat:
    # Useless thing
    is_available = True


# ---------------------------------------------------------------------------


class Carriage(ABC):
    def __init__(self, seats, price):
        self.seats = [Seat() for _ in range(seats)]
        self.price = price

    @abstractmethod
    def get_details(self):
        pass

    def set_price(self, new_price):
        self.price = new_price

    def set_seats(self, new_seats):
        self.seats = new_seats


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
        raw = open("Stations.conf", "r")

        for rawline in raw:
            rawline = rawline.split(" ")
            self.stations[rawline[0]] = " ".join(rawline[1:])

        raw.close()

    def load_carriages(self, number):
        config = ConfigParser(f"Train{number}.ini")

        carriages = {
            "seat": [],
        }

        for carriage_type in config["CountCarriages"]:
            count = int(config["CountSeatCarriages"][carriage_type])

            for _ in range(count):
                if carriage_type == "SeatCarriage":
                    seats = int(config["CountSeatCarriages"]["SeatCarriage"])
                    price = int(config["PriceCarriages"]["SeatCarriage"])
                    carriages["seat"].append(SeatCarriage(seats, price))
                elif carriage_type == "EconomCarriage":
                    seats = int(config["CountSeatCarriages"]["EconomCarriage"])
                    price = int(config["PriceCarriages"]["EconomCarriage"])
                    carriages.append(EconomCarriage(seats, price))
                elif carriage_type == "CoupeCarriage":
                    seats = int(config["CountSeatCarriages"]["CoupeCarriage"])
                    price = int(config["PriceCarriages"]["CoupeCarriage"])
                    carriages.append(CoupeCarriage(seats, price))
                elif carriage_type == "FirstClassCarriage":
                    seats = int(config["CountSeatCarriages"]["FirstClassCarriage"])
                    price = int(config["PriceCarriages"]["FirstClassCarriage"])
                    carriages.append(FirstClassCarriage(seats, price))

    def load_train(self, number):
        self.parser = ConfigParser("Route.ini")

        return Train(
            number,
            self.load_carriages(number),
        )

    def load_routes(self):
        for key, value in self.parser["Shedule"]:
            self.routes[int(key)] = Route(value, self.load_train(int(key)))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_stations(self):
        return self.stations

    def get_route(self, route_id):
        return self.routes[route_id]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def buy_ticket(self, route_id, carriage_id, seat_id):
        self.trains.get(route_id).carriages.get(carriage_id)[seat_id].is_avaible = False
