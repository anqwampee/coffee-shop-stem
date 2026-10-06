import numpy as np
from parameters import P_GEOM, DRINKS, PRICES, TIMES, PROBS

class Order:
    def __init__(self):
        self.total_time = 0.0
        self.price = 0.0
        self.items = []

        self.generate()

    def generate(self):
        drink_num = np.random.geometric(P_GEOM)
        drink_types = np.random.choice(len(DRINKS), drink_num, p=PROBS)
        for d in drink_types:
            self.total_time += TIMES[d]
            self.price += PRICES[d]
            self.items.append(DRINKS[d])

    def __str__(self):
        return f"Замовлення(час: {self.total_time}, ціна: {self.price})"

