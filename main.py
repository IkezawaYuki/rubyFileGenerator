import os
import tkinter.filedialog
import tkinter.messagebox
import traceback
import pandas as pd
import xlrd
import openpyxl

import model.input_order_file as reading
import model.ruby_source_factory
import logging

h = logging.FileHandler("log.txt", encoding="utf-8")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def validate_file(file):
    if file is None or len(file) == 0:
        exit(0)

    logger.info("Start processing...")
    logger.info("Target path is " + file)
    confirm = tkinter.messagebox.askokcancel('Ruby source generator ver1.0',
                                            '以下のファイルのサンプルデータを作成します。\n\n' + file)

    if confirm is not True:
        logger.info("システムを終了します。")
        exit(0)

    if "インターフェースオーダー定義書" not in file:
        tkinter.messagebox.showerror("Ruby source generator ver1.0", "オーダー定義書ではありません。")
        exit(0)



def main():

    logger.info("hello")
    # ファイル選択ダイアログの表示
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("","*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo('Ruby source generator ver.1.0',
                                'インターフェースオーダー定義書のRubyを作成します。')
    # file = tkinter.filedialog.askopenfilename(filetypes=fTyp,initialdir=iDir)
    file = "インターフェースオーダー定義書(IF051).xls"

    validate_file(file)
    # オーダー定義書を読みこみ、Rubyを作成。

    str = reading.read_info(file)

    logger.info("読み込み時にエラー発生")
    logger.info(traceback.format_exc())

# ファイルにRubyを出力する

if __name__ == "__main__":
    main()
