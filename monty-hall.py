from dataclasses import dataclass, field
from random import choice as choose_random_from, randrange
from itertools import count


@dataclass
class Door:
    number: int = field(default_factory=count(1).__next__, init=False)
    prize: str


class ResultsTracker:
    switch_cars = 0
    switch_total = 0
    stay_cars = 0
    stay_total = 0

    def record_and_display(self, final_choice, has_switched_door):
        self.record(final_choice, has_switched_door)
        self.display()

    def record(self, final_choice, has_switched_door):
        if has_switched_door:
            self.switch_cars += 1 if final_choice.prize == "car" else 0
            self.switch_total += 1
        else:
            self.stay_cars += 1 if final_choice.prize == "car" else 0
            self.stay_total += 1

    def display(self):
        if self.switch_total > 0 and self.stay_total > 0:
            print(
                "When switching: "
                + format(self.switch_cars / self.switch_total, "8.6f")
                + "   When not switching: "
                + format(self.stay_cars / self.stay_total, "8.6f"),
                end="\r",
            )


def play_gameshow(number_of_goats, repeat):
    prizes = ["car"] + ["goat"] * number_of_goats
    switching = True
    results = ResultsTracker()

    for _ in range(repeat):
        doors = [Door(prize) for prize in prizes]
        initial_choice = choose_random_from(doors).number

        removal_candidates = [
            door for door in doors if door.number != initial_choice and door.prize == "goat"
        ]

        while len(doors) > 2:
            doors.remove(removal_candidates.pop(randrange(0, len(removal_candidates))))

        final_choice = next(
            door for door in doors
            if switching and door.number != initial_choice
            or not switching and door.number == initial_choice
        )
        results.record_and_display(final_choice, switching)

        switching = not switching

    print("")


print("")
play_gameshow(number_of_goats=2, repeat=1000000)
print("")


# Sample chances of winning a car if one car and two goats are available, for 1,000,000 runs:
# When switching: 0.666890   When not switching: 0.333286

# If it helps understanding
# Sample chances of winning a car if one car and nine goats are available, for 1,000,000 runs:
# When switching: 0.899160   When not switching: 0.100090
