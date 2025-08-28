#!/usr/bin/env python3
"""
This file is part of the Live Code
See https://github.com/augustodamasceno/live-code/
"""
__author__ = "Augusto Damasceno"
__version__ = "1.0"
__copyright__ = "Copyright (c) 2025, Augusto Damasceno."
__license__ = "All rights reserved"


import datetime
from typing import Callable
from decimal import Decimal, getcontext


def decimal_pretty(value):
    value = Decimal(value)
    abs_value = abs(value)
    if abs_value >= Decimal('1e9'):
        return f"{value / Decimal('1e9'):.2f}bi"
    elif abs_value >= Decimal('1e6'):
        return f"{value / Decimal('1e6'):.2f}mi"
    elif abs_value >= Decimal('1e3'):
        return f"{value / Decimal('1e3'):.2f}k"
    else:
        return f"{value:.2f}"
    

class InvestmentSimulator:
    def __init__(self, 
                 tax: float, 
                 periods: int, 
                 deposit: Callable[[int], float]):
        self.tax = Decimal(str(tax))
        self.multiplier = (Decimal('1') + self.tax)
        self.periods = periods
        self.amount = [Decimal('0.0')] * (self.periods + 1)
        self.amount[0] = Decimal(str(deposit(0)))
        self.deposit = deposit
        self.simulated = False
        self.timestamp = 'invalid'

    def run(self):
        self.simulated = True
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S.%f")
        for i in range(1, self.periods + 1):
            self.amount[i] = (self.amount[i - 1] * self.multiplier
                             + Decimal(str(self.deposit(i))))

    def to_csv(self) -> str:
        data = "Iteration, Deposit, Amount\n"
        if not self.simulated:
            return data
        
        for i in range(self.periods + 1):
            data += f"{i}, {self.deposit(i):.2f}, {self.amount[i]:.2f}\n"
        return data
    
    def write_csv(self):
        with open(f'investment_simulation_metadata_{self.timestamp}.csv', 'w') as f:
            f.write(str(self))
        with open(f'investment_simulation_{self.timestamp}.csv', 'w') as f:
            f.write(self.to_csv())

    def __str__(self):
        if not self.simulated:
            return 'Not simulated.'
        
        return ("Investment Simulator\n"
              + f"Datetime: {self.timestamp}\n"
              + f"\tTax {Decimal('100.0')*self.tax:.4f}%\n"
              + f"\tTax in 12 Periods {(Decimal('12')**self.multiplier):.4f}%\n"
              + f"\tPeriods {self.periods}\n"
              + f"\tInitial Deposit {self.deposit(0):.2f}\n"
              + f"\tLast Deposit {self.deposit(self.periods+1):.2f}\n"
              + f"\tTotal Amount {decimal_pretty(self.amount[-1])}\n"
              )



if __name__ == "__main__":
    simulator = InvestmentSimulator(tax=0.012, 
                                    periods=12*30, 
                                    deposit=lambda x: 500+4*x)
    simulator.run()
    print(simulator)
    simulator.write_csv()