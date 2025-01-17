from PIL import Image
import pytesseract
import re
import os
import pandas as pd
import numpy as np
from gas_brasiliano_config import corte_gas_brasiliano, caminho_excel
from gas_brasiliano_funcoes import pdf_ocr, pdf_to_image, dados_excel, adicionar_dados_excel, verificar_download, mover_faturas_lidas

#in/out 3100, 1300, 3800, 1450
#X-Y X-Y
dist = 'Gás Brasiliano'
usuario_conectado = 'samuel.santos'
# Configure o caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = fr'C:\Users\{usuario_conectado}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def extrator_cnpj(imagem, cordenadas):#
        try:
                cnpj = imagem.crop(corte[cordenadas])
                #cnpj.show()
                cnpj = pdf_ocr(cnpj)
                cnpj = cnpj.replace (',','').replace('/','').replace('-','').replace('.', '')
                cnpj = re.findall(r'(\d+)',cnpj)
                cnpj = ''.join(cnpj)
                cnpj = cnpj

                return cnpj
        except:
                return False

def extrator_valor_total(imagem, coordenadas): #
        try:        
                valor_total = imagem.crop(corte[coordenadas])
                #valor_total.show()
                valor_total = pdf_ocr(valor_total)
                if '§' in valor_total:
                    valor_total = valor_total.replace('§', '5')
                valor_total = re.findall(r'(\d{1,3}[\,\.]?\d{1,3}\.?\s?\,?\d{1,2})',valor_total)
                valor_total  = valor_total[0].strip()
                valor_total = re.sub(r'(\d+)(\,)(\d+\,\d+)',r'\1.\3',valor_total)
                valor_total = valor_total.replace(' ', '') 
                #volume_total = round(float(volume_total),4)
                #valor_total = valor_total.replace('.','').replace(",",".")
                return valor_total
        except:
                return False
    
def extrator_volume_total(imagem, coordenadas):#     #QUANTIDADE
    try:        
        volume_total = imagem.crop(corte[coordenadas])
        #volume_total.show()
        volume_total = pdf_ocr(volume_total) 
        volume_total = re.findall(r'\s?(\d+[\.?A-a\,?]\d+\,?\.?\d+)\s?', volume_total)
        volume_total = volume_total[0].strip()
        volume_total = volume_total.replace(' ', '')  # Remove espaços em branco
        volume_total = volume_total.replace('.', '').replace(",", ".")
        volume_total = round(float(volume_total), 5)
        volume_total = str(volume_total)
        
        return volume_total
    
    except:
        return False
    
def extrator_data_emissao(imagem, coordenadas):#
        try:
                data_emissao = imagem.crop(corte[coordenadas])
                #data_emissao.show()
                data_emissao = pdf_ocr(data_emissao)
                data_emissao = re.findall(r'\d{2}/\d{2}/\d{4}',data_emissao)               
                data_emissao  = data_emissao[0].strip()                   

                return data_emissao.split()
        except:
                return False
                
def extrator_data_inicio(imagem, coordenadas):  #?  
        try:
                data_inicio = imagem.crop(corte[coordenadas])
                #data_inicio.show()
                data_inicio = pdf_ocr(data_inicio)
                data_inicio = re.findall(r'\s(\d+\/\d+\/\d{2,4})',data_inicio)
                data_inicio  = data_inicio[0].strip()
                #data_inicio = data_inicio_mes(data_inicio)

                return data_inicio
        except:
                return False

def extrator_data_fim(imagem, coordenadas): #?

        try:
                data_fim = imagem.crop(corte[coordenadas])
                #data_fim.show()
                data_fim = pdf_ocr(data_fim)
                data_fim = re.findall(r'\s(\d+\/\d+\/\d{2,4})',data_fim)
                data_fim = data_fim[0].strip()
                return data_fim
        except:
                return False
        
def extrator_numero_fatura(imagem, coordenadas): #
        
        try:
                numero_fatura = imagem.crop(corte[coordenadas])
                #numero_fatura.show()
                numero_fatura = pdf_ocr(numero_fatura)
                numero_fatura = re.findall(r'\s?(\d+\.?\d+\.?\d+)',numero_fatura)
                numero_fatura  = numero_fatura[0].strip()
                
                return numero_fatura
        except:
                        
                return False

def extrator_valor_icms(imagem, coordenadas):#
        
        try:
                valor_icms = imagem.crop(corte[coordenadas])
                #valor_icms.show()
                valor_icms = pdf_ocr(valor_icms)
                valor_icms = re.findall(r'\d+\,?\.?\s?\d+\.?\d+\.?\,?\s?\,?\d+\,?\d+', valor_icms)
                if valor_icms:  # Verifica se a lista não está vazia
                    valor_icms = valor_icms[0].strip()
                    if valor_icms.startswith('0'):
                        valor_icms = False
                else:
                        valor_icms = False
                        
                return valor_icms
        except Exception as e:
                print(f"Erro: {e}")
                return False

def extrator_correcao_pcs(imagem, coordenadas): #
        
        try:
                correcao_pcs = imagem.crop(corte[coordenadas])
                #correcao_pcs.show()
                correcao_pcs = pdf_ocr(correcao_pcs)
                correcao_pcs = re.findall(r'\s?(\d+\,?\d+\.?\d+\.?\d+)',correcao_pcs)
                correcao_pcs = ''.join(correcao_pcs)
                if correcao_pcs ==  '':
                      raise Exception
                
                return correcao_pcs
        except Exception as erro:
                print(erro)
                return False
        
def main(file, pdf_file):
    imagem = pdf_to_image(pdf_file)

    cnpj = extrator_cnpj(imagem, 'cnpj')
    if cnpj == False or len(cnpj) < 14:
        cnpj = extrator_cnpj(imagem, 'cnpj_ajustado')
        if cnpj == False or len(cnpj) < 14:
            cnpj = extrator_cnpj(imagem, 'cnpj_necta') # CRIAR OCR
    
    valor_total = extrator_valor_total(imagem, 'valor_total')
    if valor_total == False:
        valor_total = extrator_valor_total(imagem, 'valor_total_ajustado')
        if valor_total == False:
           valor_total = extrator_valor_total(imagem, 'valor_total_ajustado1')
           if valor_total == False:
                 valor_total = extrator_valor_total(imagem, 'valor_total_ajustado2')
                 if valor_total == False:
                         valor_total = '---' 

    volume_total = extrator_volume_total(imagem, 'volume_total')
    if volume_total == False:
        volume_total = extrator_volume_total(imagem, 'volume_total_ajustado')
        if volume_total == False:
            volume_total = extrator_volume_total(imagem, 'volume_necta')
            if volume_total == False:
                   volume_total = extrator_volume_total(imagem, 'volume_total_ajustado3')
                   if volume_total == False:
                          volume_total = '---'

    data_emissao = extrator_data_emissao(imagem, 'data_emissao')
    if data_emissao == False:
        data_emissao = extrator_data_emissao(imagem, 'data_emissao2')
        if data_emissao == False:
            data_emissao = extrator_data_emissao(imagem, 'data_emissao3')
            if data_emissao == False:
                  data_emissao = extrator_data_emissao(imagem, 'emissao_necta')
    
    data_inicio = extrator_data_inicio(imagem, 'data_inicio')
    if data_inicio == False:
        data_inicio = extrator_data_inicio(imagem, 'data_inicio_ajustado')               
        if data_inicio == False:
            data_inicio = extrator_data_inicio(imagem, 'data_inicio_ajustado2')
            if data_inicio == False:
                data_inicio = extrator_data_inicio(imagem, 'data_inicio_ajustado3')
                if data_inicio == False:
                    data_inicio = extrator_data_inicio(imagem, 'data_inicio_ajustado4')
                         
    data_fim = extrator_data_fim(imagem, 'data_fim')
    if data_fim == False:
        data_fim = extrator_data_fim(imagem, 'data_fim_ajustado')
        if data_fim == False:
            data_fim = extrator_data_fim(imagem, 'data_fim_ajustado2')
            if data_fim == False:
                  data_fim = extrator_data_fim(imagem, 'data_fim_ajustado3')
                  if data_fim == False: 
                         data_fim = extrator_data_fim(imagem, 'data_fim_ajustado3')
                         if data_fim == False:
                                data_fim = extrator_data_fim(imagem, 'data_fim_ajustado4')

    numero_fatura = extrator_numero_fatura(imagem, 'numero_fatura')
    if numero_fatura == False:
        numero_fatura = extrator_numero_fatura(imagem, 'numero_fatura_ajustado')
        if numero_fatura == False:
            numero_fatura = extrator_numero_fatura(imagem, 'numero_necta')
            if numero_fatura == False:
                numero_fatura = extrator_numero_fatura(imagem, 'numero_fatura_ajustado3')
        
    valor_icms = extrator_valor_icms(imagem, 'valor_icms')
    if valor_icms == False:
        valor_icms = extrator_valor_icms(imagem, 'valor_icms_ajustado')
        if valor_icms == False:
            valor_icms = extrator_valor_icms(imagem, 'valor_icms_ajustado2')
            if valor_icms == False:
                valor_icms = extrator_valor_icms(imagem, 'valor_icms_ajustado3')    
    
    correcao_pcs = extrator_correcao_pcs(imagem, 'correcao_pcs')
    if correcao_pcs == False:
        correcao_pcs = extrator_correcao_pcs(imagem, 'correcao_pcs_ajustado')
        if correcao_pcs == False:
            correcao_pcs = extrator_correcao_pcs(imagem, 'correcao_pcs_ajustado2')   
        
    if not cnpj or not valor_total or not volume_total or not data_emissao or not data_inicio or not data_fim or not numero_fatura or not valor_icms or not correcao_pcs:
        print('Fatura não movida devido a dados incompletos.')
    else: 
        
        verificar = verificar_download(cnpj, data_inicio, data_fim, caminho_excel)
        if verificar:
                
                data_frame = dados_excel(cnpj, valor_total, volume_total, data_emissao, data_inicio, data_fim, numero_fatura, valor_icms, correcao_pcs, dist, arquivo)
                adicionar_dados_excel(caminho_excel, data_frame)
                mover_faturas_lidas(pdf_file, diretorio_destino)

        else:
                print('Dados já inseridos!')

# Exemplo de uso
corte = corte_gas_brasiliano()
file_path = r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Brasiliano\Faturas'
diretorio_destino = r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Brasiliano\Lidos'

for arquivo in os.listdir(file_path):
        if arquivo.endswith('.pdf') or arquivo.endswith('.PDF'):
                arquivo_full = rf'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Brasiliano\Faturas\{arquivo}' 
        main(arquivo, arquivo_full)