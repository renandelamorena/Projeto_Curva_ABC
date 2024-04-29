import pyautogui as pag
import pyperclip as pcl

import datetime
from dateutil.relativedelta import relativedelta

from func_geral import p_i, p_f

def colar_data_1_ano_atras():

    data_atual = datetime.now()

    data_um_ano_atras = data_atual - relativedelta(years=1)

    dia_1_ano_atras = data_um_ano_atras.day
    mes_1_ano_atras = data_um_ano_atras.month
    ano_1_ano_atras = data_um_ano_atras.year

    if dia_1_ano_atras < 10:
        dia_1_ano_atras = '0' + str(dia_1_ano_atras)

    if mes_1_ano_atras < 10:
        mes_1_ano_atras = '0' + str(mes_1_ano_atras)

    p_i(0.5)
    pcl.copy(dia_1_ano_atras)
    pag.hotkey('ctrl', 'v')
    pcl.copy(mes_1_ano_atras)
    pag.hotkey('ctrl', 'v')
    pcl.copy(ano_1_ano_atras)
    pag.hotkey('ctrl', 'v')
    p_f()

def colar_data_3_meses_atras():

    data_atual = datetime.now()

    data_tres_meses_atras = data_atual - relativedelta(months=3)

    dia_3_meses_atras = data_tres_meses_atras.day
    mes_3_meses_atras = data_tres_meses_atras.month
    ano_3_meses_atras = data_tres_meses_atras.year

    if dia_3_meses_atras < 10:
        dia_3_meses_atras = '0' + str(dia_3_meses_atras)

    if mes_3_meses_atras < 10:
        mes_3_meses_atras = '0' + str(mes_3_meses_atras)

    p_i(0.5)
    pcl.copy(dia_3_meses_atras)
    pag.hotkey('ctrl', 'v')
    pcl.copy(mes_3_meses_atras)
    pag.hotkey('ctrl', 'v')
    pcl.copy(ano_3_meses_atras)
    pag.hotkey('ctrl', 'v')
    p_f()