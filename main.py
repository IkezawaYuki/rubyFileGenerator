import os
import tkinter.filedialog
import tkinter.messagebox
import traceback
import pandas as pd
import xlrd
import openpyxl

import model.input_order_file as reading
import model.output_ruby_source
import logging


h = logging.FileHandler("log.txt")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)

logger.info("hello")
# ファイル選択ダイアログの表示
root = tkinter.Tk()
root.withdraw()
fTyp = [("","*")]
iDir = os.path.abspath(os.path.dirname(__file__))
tkinter.messagebox.showinfo('Ruby source generator ver.1.0','選択した変換定義書のサンプルを作成します。')
file = tkinter.filedialog.askopenfilename(filetypes=fTyp,initialdir=iDir)
#file = "インターフェースオーダー定義書(IF051).xls"

logger.info("Start processing...")
logger.info("Target path is " + file)
confirm = tkinter.messagebox.askokcancel('Sample file generator ver1.0',
                                             '以下のファイルのサンプルデータを作成します。\n\n' + file)
if confirm is False:
    logger.info("システムを終了します。")
    exit(0)

#　オーダー定義書を読みこみ、Rubyを作成。
try:
    str = reading.read_info(file)
except:
    logger.info("読み込み時にエラー発生")
    logger.info(traceback.format_exc())

#　ファイルにRubyを出力する


