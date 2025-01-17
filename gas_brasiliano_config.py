# COORDENADAS PARA EXTRAÇÃO DE DADOS USANDO OCR

def corte_gas_brasiliano():
    corte = {

    'cnpj': (650, 1880, 1500, 1960), #  NECTA
    'cnpj_ajustado': (650, 1760, 1500, 1830), # GAS BRSILIANO
    'cnpj_necta': (650, 1770, 1500, 1850),    

    'valor_total': (3320, 2100, 3950, 2300), # NECTA
    'valor_total_ajustado':(3320, 1980, 3950, 2180),

    'volume_total': (3350, 4050, 3930, 4100), # NECTA
    'volume_total_ajustado2': (2000, 2890, 2385, 3200),# GAS BRASILIANO
    'volume_necta': (3400, 4200, 3900, 4400),

    'data_emissao': (3280, 1040, 4000, 1100),# NECTA
    'data_emissao2': (3280, 815, 4000, 870), # GAS BRASILIANO
    'emissao_necta': (2720, 750, 3200, 850),

    'data_inicio': (545, 3020, 850, 3200), # NECTA
    'data_inicio_ajustado': (545, 2900, 850, 3070), # GAS BRSILIANO
    'data_inicio_ajustado2': (530, 3020, 850, 3200),

    'data_fim': (245, 3020, 650, 3200), # NECTA
    'data_fim_ajustado': (245, 2900, 650, 3070), # GAS BRSILIANO
    'data_fim_ajustado2': (300, 4650, 1700, 4750),

    'numero_fatura': (3280, 950, 4000, 1050), # NECTA
    'numero_fatura_ajustado': (3280, 740, 4000, 815), # GAS BRSILIANO
    'numero_necta': (2720, 680, 3200, 780), # GAS BRSILIANO


    'valor_icms': (1305, 3390, 1700, 3460), # NECTA
    'valor_icms_ajustado': (1000, 3420, 1480, 3480), # GAS BRSILIANO

    'correcao_pcs': (2700, 4050, 3000, 4100),# NECTA
    'correcao_pcs_ajustado': (2500, 4000, 3000, 4370), # GAS BRSILIANO
    'correcao_pcs_ajustado2': (2500, 4000, 3000, 4370) # GAS BRSILIANO


    }
    return corte
caminho_excel = r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\00 Faturas Lidas\GAS BRASILIANO.xlsx'

'''while True
    for Player(get_moeda):
        if player(moeda >= 3):
            brilhar(dourado)
        else:
            brilhar(branco)'''


