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
            for cell in row:
                # 全ての情報がセル単位で取り出すことに成功中
                print(cell.value)
            print(row[8])



def read_sheet_info(file, target):
    for sheet in target:
        input_sheet_df = file.parse(sheet)



    return str

def test(df_list):
    pass






