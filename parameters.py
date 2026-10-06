import numpy as np
import pandas as pd

STEP = 10                                  # хв
N_STEPS = int((21.5 - 7.5) * 60 // STEP)           # 84 кроки
QUEUE_LIMIT = 4                                      # ліміт черги
P_GEOM = 0.6                               # параметр геометричного розподілу
STATION_COST =  200                      # грн/год
FOOD_COST_RATE = 0.35

PERIODS = [(7.5, 10, 8), (10, 13, 3), (13, 16, 5), (16, 19, 7), (19, 21.5, 2)]
# (початок, кінець, λ за крок)

DRINKS = ["Еспресо", "Американо", "Капучино", "Лате", "Чай"]
PRICES = [60, 70, 85, 90, 80]
TIMES  = [0.5, 3, 4, 4, 3]
PROBS  = [0.20, 0.20, 0.25, 0.20, 0.15]

def get_lambda(hour):
    for period in PERIODS:
        if hour >= period[0] and hour < period[1]:
            return period[2]
    return 0


