from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import OHLCV

class TradingStrategy(Strategy):
    def __init__(self):
        # Assuming SPY as a representative for the S&P 500
        self.ticker = "SPY"
        # Placeholder for previous day's close price to calculate day-to-day changes
        self.previous_close = None

    @property
    def assets(self):
        # List of assets this strategy will operate on
        return [self.ticker]

    @property
    def interval(self):
        # Use daily data for each trading decision
        return "1day"

    def run(self, data):
        # Dictionary to store the target allocation for each asset
        allocation_dict = {}

        # Fetch the OHLCV data for SPY
        ohlcv_data = data["ohlcv"]
        
        # Check if there's enough data for comparison
        if len(ohlcv_data) < 2:
            log("Not enough data for comparison.")
            return TargetAllocation(allocation_dict)

        # Retrieve the current and previous day's close prices
        current_close = ohlcv_data[-1][self.ticker]["close"]
        if self.previous_close is None:
            self.previous_close = ohlcv_data[-2][self.ticker]["close"]

        # Calculate the percentage change from the previous close to the current close
        percent_change = (current_close - self.previous_close) / self.previous_close * 100

        # If stock drops by at least 5%, buy $1 worth of SPY
        if percent_change <= -5:
            allocation_dict[self.ticker] = 1  # Buy signal, value to represent $1 worth can be adjusted as per implementation specifics
            log(f"Buying $1 worth of {self.ticker} due to a drop of {percent_change}%.")
        
        # If stock increases by at least 10%, sell $1 worth of SPY
        elif percent_change >= 10:
            allocation_dict[self.ticker] = -1  # Sell signal, value to represent $1 worth can be adjusted as per implementation specifics
            log(f"Selling $1 worth of {self.ticker} due to an increase of {percent_change}%.")

        # Update the previous close for the next day's calculation
        self.previous_close = current_close

        # Return the target allocation as a TargetAllocation object
        return TargetAllocation(allocation_dict)