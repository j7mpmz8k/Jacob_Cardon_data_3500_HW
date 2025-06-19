def import_stock(file_name):
    with open(file_name) as stock_file:
        lines = stock_file.read().split()# converts to a list
        prices = [round(float(line),2) for line in lines]# sets each price value to a float rounded to two decimal places
    return prices

prices = import_stock('/home/crostini/Github/Jacob_Cardon_data_3500_HW/HW/hw5/AAPL.txt')



def calculate_ema(data, period):
    """
    Calculates the Exponential Moving Average (EMA) for a given list of data.

    Args:
        data (list of float): A list of numerical data (e.g., closing prices).
        period (int): The period for the EMA calculation.

    Returns:
        list of float: A list containing the EMA values. Returns an empty list
                       if the data is insufficient for the period.
    """
    if len(data) < period:
        return []

    ema_values = []
    # The multiplier for smoothing.
    multiplier = 2 / (period + 1)
    
    # The first EMA is a simple moving average of the first 'period' prices.
    sma = sum(data[:period]) / period
    ema_values.append(sma)

    # Calculate the subsequent EMA values
    for i in range(period, len(data)):
        current_price = data[i]
        previous_ema = ema_values[-1]
        current_ema = (current_price - previous_ema) * multiplier + previous_ema
        ema_values.append(current_ema)
        
    return ema_values

def calculate_macd(close_prices, day, short_period=12, long_period=26, signal_period=9):
    """
    Calculates the MACD line, Signal line, and Histogram.

    Args:
        close_prices (list of float): A list of closing prices.
        short_period (int): The period for the short-term EMA (default 12).
        long_period (int): The period for the long-term EMA (default 26).
        signal_period (int): The period for the Signal line EMA (default 9).

    Returns:
        tuple: A tuple containing three lists (macd_line, signal_line, histogram).
               Returns ([], [], []) if the data is insufficient.
    """
    if len(close_prices) < long_period:
        print("Not enough data to calculate MACD.")
        return [], [], []

    # Calculate the 12-period and 26-period EMAs
    ema_short = calculate_ema(close_prices, short_period)
    ema_long = calculate_ema(close_prices, long_period)

    # The MACD calculation can only start where both EMAs are available.
    # The longer EMA starts later, so we align our MACD calculation to its start.
    alignment_offset = long_period - short_period
    
    # Calculate the MACD line
    macd_line = []
    for i in range(len(ema_long)):
        # Align the short EMA with the long EMA
        macd_value = ema_short[i + alignment_offset] - ema_long[i]
        macd_line.append(macd_value)

    # Calculate the Signal line (9-period EMA of the MACD line)
    signal_line = calculate_ema(macd_line, signal_period)

    # Calculate the Histogram
    # The histogram can only be calculated where the signal line is available.
    histogram_offset = signal_period - 1
    histogram = []
    for i in range(len(signal_line)):
      # Align the MACD line with the Signal line
      histogram_value = macd_line[i + histogram_offset] - signal_line[i]
      histogram.append(round(histogram_value,4))

    # To ensure all lists are the same length for easy plotting,
    # we trim the beginning of the macd_line and signal_line.
    final_macd_line = macd_line[histogram_offset:]

    start_day = len(prices) - len(histogram)
    index_of_histogram = day-start_day
    if day >= start_day:
        return histogram[index_of_histogram]
    else:
        return None


###########################################################################################





def MacdStrategey(ticker, prices):
    N_days = 200# executes strategy over Nth number of days
    
    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0

    print('-'*44)#creates a line for formatting
    print(f'{ticker} Macd Strategy Over Period of: {N_days}')

    #calculates buy/sell conditions and individual trade profits
    for day, price in enumerate(prices):# keeps track of index position of each day and price value
        if calculate_macd(prices, day) is None:# ensures at least "N_days" have past till "N_days" average calculates
            pass
        else:

            #ensures today's price is at least 2% less than last "N_days" moving avg
            #AND not to double up on stock inventory
            if calculate_macd(prices, day) < 0 and buy != 0:#sell conditions
                trade_profits = round(price - buy,2)#initiates purchase of stock
                total_profit += trade_profits#adds to total profits
                if day == len(prices)-1:# checks if day is most recent day
                    print(f'Today you should sell at:\t$ {price}')
                    print(f'trade profits:\t$ {trade_profits}')
                if first_buy == 0:
                    first_buy = buy# keeps track of price of first purchase for return on investment
                buy = 0# resets stock inventory to zero

            #ensures today's price is at least 2% greater than last "N_days" moving avg
            # AND not to double up on stock inventory
            elif calculate_macd(prices, day) > 0 and buy == 0:#buy conditions
                if day == len(prices)-1:# checks if day is most recent day
                    print(f'Today you should buy at:\t\t$ {price}')
                buy = price# updates stock inventory to current purchase

    #calculates ROI % 
    try:
        final_profit_percentage = f'{round((total_profit/first_buy)*100,2)}%'
    except ZeroDivisionError:
        final_profit_percentage = "0.00%"
    total_profit = round(total_profit,2)

    #prints final totals of profits and returns of a year of trade history         
    print(f'total profits:\t$ {total_profit}')
    print(f'first buy:\t$ {first_buy}')
    print(f'percent return:\t  {final_profit_percentage}')
    return total_profit, final_profit_percentage

MacdStrategey("AAPL", prices)