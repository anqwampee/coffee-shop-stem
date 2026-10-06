import numpy as np
from stats import Stats
from order import Order
from parameters import *

class Cafe:
    def __init__(self):
        self.current_time = 7.5
        self.queue = []
        self.current_order = None
        self.remaining_time = 0.0
        self.stats = Stats()

    def arrive(self):
        k = np.random.poisson(get_lambda(self.current_time))
        for _ in range(k):
            order = Order()
            self.stats.add_arrival()
            if self.current_order is None:
                self.current_order = order
                self.remaining_time = order.total_time
            elif len(self.queue) < QUEUE_LIMIT:
                self.queue.append(order)
            else:
                self.stats.add_lost()

    def serve(self):
        budget = STEP
        while (0 < budget and self.current_order is not None):
            if self.remaining_time <= budget:
                self.stats.add_served(self.current_order.total_time, self.current_order.price)
                budget -= self.remaining_time
                if self.queue:
                    self.current_order = self.queue.pop(0)
                    self.remaining_time = self.current_order.total_time
                else:
                    self.current_order = None
                    self.remaining_time = 0
            else:
                self.remaining_time -= budget
                budget = 0



