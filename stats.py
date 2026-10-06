import numpy as np
from parameters import *

class Stats:
    def __init__(self):
        self.clients = {"came":0, "served":0, "lost":0}
        self.revenue = 0.0
        self.queue_lengths = []
        self.busy_time = 0.0

    def add_arrival(self):
        self.clients["came"] += 1

    def add_lost(self):
        self.clients["lost"] += 1

    def add_served(self, serving_time, price):
        self.clients["served"] += 1
        self.revenue += price
        self.busy_time += serving_time

    def record_queue(self, queue_length):
       self.queue_lengths.append(queue_length)


    def summary(self):
        ingredients_cost = self.revenue * FOOD_COST_RATE
        fixed_station_cost = STATION_COST * 14
        total_cost = fixed_station_cost + ingredients_cost
        return {
            "loss rate": self.clients["lost"]/self.clients["came"],
            "average queue length": np.mean(self.queue_lengths) if len(self.queue_lengths) > 0 else 0.0,
            "maximum queue length": np.max(self.queue_lengths) if len(self.queue_lengths) > 0 else 0.0,
            "utilisation": self.busy_time/840,    # навантаження на хвилину
            "revenue": self.revenue,
            "cost": total_cost,
            "profit": self.revenue - total_cost
        }
