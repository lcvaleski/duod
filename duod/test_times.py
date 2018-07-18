import os
from datetime import datetime
import unittest

from util_funcs import market_closed

class TestTimeFunctions(unittest.TestCase):

    def test_market_closed(self):
        # test some known open and closed time windows
        closed_time_1 = datetime.strptime("12/06/18 14:05", "%d/%m/%y %H:%M")
        open_time_1 = datetime.strptime("12/06/18 14:35", "%d/%m/%y %H:%M")
        closed_time_2 = datetime.strptime("12/06/18 23:05", "%d/%m/%y %H:%M")
        open_time_2 = datetime.strptime("12/06/18 18:00", "%d/%m/%y %H:%M")
        closed_weekend = datetime.strptime("17/06/18 18:00", "%d/%m/%y %H:%M")

        self.assertFalse(market_closed(closed_time_1))

        self.assertTrue(market_closed(open_time_1))

        self.assertFalse(market_closed(closed_time_2))

        self.assertTrue(market_closed(open_time_2))

        self.assertFalse(market_closed(closed_weekend))

if __name__ == '__main__':
    unittest.main()
