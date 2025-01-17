from babel.numbers import format_currency

def converter_moeda(data):
    return format_currency(data, "BRL", locale="pt_BR")