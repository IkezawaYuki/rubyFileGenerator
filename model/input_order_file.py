import openpyxl
import tkinter.messagebox
import logging
import pandas as pd

h = logging.FileHandler("log.txt")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def read_info(filepath):
    """エクセルの情報を取得します。Ruby作成に必要のないsheetは無視します。"""
    file = pd.ExcelFile(filepath)
    df_list = []
    for sheet in file.sheet_names:
        if sheet == "表紙" or sheet == "更新履歴" or sheet == "環境変数一覧":
            continue
        df_list.append((sheet, file.parse(sheet)))
    read_sheet_info(df_list)



def read_sheet_info(df_list):
    for sheetName, sheetdf in df_list:
        print(sheetName,sheetdf)
        for index, row in sheetdf.iterrows():
            print(row)


def test(df_list):
    pass






