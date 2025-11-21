from typing import Any


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.is_alive = is_alive
        self.row = row
        self.column = column


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        if start[1] != end[1]:

            step = 1 if end[1] - start[1] >= 0 else - 1
            self.decks = [Deck(start[0], x)
                          for x in range(start[1], end[1] + step, step)]

        elif start[0] != end[0]:
            step = 1 if end[0] - start[0] >= 0 else - 1
            self.decks = [Deck(y, end[1])
                          for y in range(start[0], end[0] + step, step)]

        else:
            self.decks = [Deck(start[0], start[1])]

        self.coord = self.get_coord()

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None:
            return "Miss!"

        if deck.is_alive is False:
            return "Miss!"

        deck.is_alive = False

        if self.is_ship_alive():
            return "Hit!"
        else:
            self.is_drowned = True
            return "Sunk!"

    def is_ship_alive(self) -> bool:
        return any([deck.is_alive for deck in self.decks])

    def get_coord(self) -> list[tuple[int, int]]:
        return [(deck.row, deck.column) for deck in self.decks]

    def __len__(self) -> int:
        return len(self.coord)

    def __repr__(self) -> str:
        return f"{self.coord}"

    def __contains__(self, item: Any) -> bool:
        return item in self.coord


class Battleship:
    def __init__(self, ships: list[tuple, tuple]) -> None:
        self.field = [["~" for _ in range(10)] for _ in range(10)]

        self.ships = self.create_ships(ships)
        if not self._validate_field():
            raise ValueError("Your ships is not correct for the game")

        self.draw_ships()

    def create_ships(self, ships: list[tuple, tuple]) -> list[Ship]:

        return [Ship(*ship) for ship in ships]

    def _validate_field(self) -> bool:
        length_ships = [len(ship) for ship in self.ships]
        length_ships.sort()

        if length_ships == [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            return True

        return False

    def draw_ship_on_field(self, ship: Ship) -> None:
        ship_coords = ship.get_coord()

        for coord in ship_coords:
            self.field[coord[0]][coord[1]] = u"\u25A1"

    def draw_ships(self) -> None:
        for ship in self.ships:
            self.draw_ship_on_field(ship)

    def fire(self, location: tuple[int, int]) -> str:
        for ship in self.ships:
            if location in ship:
                return ship.fire(location[0], location[1])

        return "Miss!"
