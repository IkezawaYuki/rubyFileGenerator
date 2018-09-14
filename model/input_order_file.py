import openpyxl
import tkinter.messagebox
import logging
import pandas as pd
import xlrd

h = logging.FileHandler("log.txt")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def read_info(filepath):
    """エクセルの情報を取得します。Ruby作成に必要のないsheetは無視します。"""
    file = xlrd.open_workbook(filepath)
    for i in range(file.nsheets):
        sheet = file.sheet_by_index(i)
        print(sheet.name)
        if sheet.name == "更新履歴" or sheet.name == "表紙" or sheet.name == "環境変数一覧":
            continue
        for row_index in range(sheet.nrows):
            row = sheet.row(row_index)
            logger.info(row)
            for colum, cell in enumerate(row):
                dispatch_cell_info(colum, cell.value)



def dispatch_cell_info(colum, value):
    logger.info("colum is " + str(colum))
    if colum == 8:
        print("target!")
    print(value)



    return str

def save_info():

    pass






