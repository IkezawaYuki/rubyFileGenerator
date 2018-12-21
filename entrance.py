import os
import tkinter.filedialog
import tkinter.messagebox
import traceback
import logging
import sys

import controller.control as co

h = logging.FileHandler("log.txt", encoding="utf-8")
logger = logging.getLogger(__name__)
fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s :%(message)s")
h.setFormatter(fmt)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def validate_file(file):
    if file is None or len(file) == 0:
        logger.info("中断")
        sys.exit(0)

    logger.info("指定したファイルのパスは " + file)
    confirm = tkinter.messagebox.askokcancel('entrance',
                                            '以下のオーダー定義書のRubyファイルを作成します。\n\n' + file)

    if confirm is not True:
        logger.info("キャンセル")
        sys.exit(0)

    if "インターフェースオーダー定義書" not in file:
        tkinter.messagebox.showerror("entrance",
                                     "オーダー定義書ではありません。")
        logger.info("「オーダー定義書」の文言がない")
        sys.exit(0)


def main():
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("","*")]
    iDir = os.path.abspath(os.path.dirname(__file__))

    file = tkinter.filedialog.askopenfilename(filetypes=fTyp,initialdir=iDir)
    # file = "/Users/ikezaway/PycharmProjects/rubyFileGenerator/インターフェースオーダー定義書(IF051).xls"
    validate_file(file)

    try:
        co.execute(file)
    except co.ReadingException:
        logger.error("Error is occured in reading!")
        logger.error(traceback.format_exc())
        tkinter.messagebox.showerror("entrance",
                                     "オーダー定義書の読み込み時にエラーが発生しました。処理を中断します。")
        sys.exit(1)
    except co.WritingException:
        logger.error("Error is occurred in writing!")
        logger.error(traceback.format_exc())
        tkinter.messagebox.showerror("entrance",
                                     "Rubyファイル・batファイル書き込み時にエラーが"
                                     "発生しました。処理を中断します。")
        sys.exit(1)

    tkinter.messagebox.showinfo("entrance",
                                "処理が完了しました。\n/source、/bat以下を確認してください")


if __name__ == "__main__":
    logger.info("ファイル選択ダイアログを起動します。")
    main()
