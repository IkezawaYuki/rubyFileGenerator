import openpyxl
import tkinter.messagebox
import logging


h = logging.FileHandler("log.txt")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def read_info(df):


    print(df)

    targat_sheet = "インターフェースオーダー定義書"








