def calcular_juros_compostos(referencia, inicial, mensal, taxa, meses):
    total_acumulado = 0
    total_investido = 0
    total_juros = 0

    for i in range(meses):
        if i == 0:
            total_investido = inicial
            total_juros = total_investido * taxa
            total_acumulado = total_investido + total_juros
        else:
            total_juros = total_acumulado * taxa
            total_investido = total_investido + mensal
            total_acumulado = total_acumulado + mensal + total_juros
    juros_totais = total_acumulado - total_investido

    return {
        "referencia": str(referencia).upper(),
        "montante_total":round(float(total_acumulado),2),
        "investidos": round(float(total_investido),2),
        "juros_totais": round(float(juros_totais),2),
        "taxa_juros":taxa,
        "meses":meses
    }