import numpy as np
from parameters import *
from cafe import *

class Statistics:
    def __init__(self):
        self.clients = {"came":0, "served":0, "lost":0}
        self.revenue = 0.0
        self.queue_lengths = []
        self.busy_time = 0.0

    def add_arrival(self):
        self.clients["came"] += 1

    def add_lost(self):
        self.clients["lost"] += 1

    def add_served(self, price, serving_time):
        self.clients["served"] += 1
        self.revenue += price
        self.busy_time += serving_time

    def record_queue(self, queue_length):
       self.queue_lengths.append(queue_length)


    def summary(self):
        return {
            "loss rate": self.clients["lost"]/self.clients["came"],
            "average queue length": np.mean(self.queue_lengths) if len(self.queue_lengths) > 0 else 0.0,
            "maximum queue length": np.max(self.queue_lengths) if len(self.queue_lengths) > 0 else 0.0,
            "utilisation": self.busy_time/840,    # навантаження на хвилину
            "revenue": self.revenue,
            "cost": STATION_COST * 14,
            "profit": self.revenue - STATION_COST * 14
        }
