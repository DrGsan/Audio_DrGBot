from pycbrf import ExchangeRates


def currency(name):
    exchangerate = str(ExchangeRates()[name].value).replace(".", ",")[:-2]
    return exchangerate
