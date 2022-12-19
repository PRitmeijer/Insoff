def transform_pricedata(pricedata):
    return 'low' if pricedata == 'L' else 'high' if pricedata == 'H' else 'vwap'