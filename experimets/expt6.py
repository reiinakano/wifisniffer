stock_prices_yesterday = [7,6,7]

def get_max_profit(stock_prices_yesterday):
    lowest_price = None
    highest_profit = None

    for price in stock_prices_yesterday:
        if lowest_price is None:
            lowest_price = price
        else:
            profit = price - lowest_price
            if profit > highest_profit:
                highest_profit = profit
            if lowest_price > price:
                lowest_price = price

    return highest_profit

print get_max_profit(stock_prices_yesterday)

