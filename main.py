import os
import tkinter.filedialog
import tkinter.messagebox
import traceback
import logging

import controller.controll as co

h = logging.FileHandler("log.txt", encoding="utf-8")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def validate_file(file):
    if file is None or len(file) == 0:
        exit(0)

    logger.info("Start processing...")
    logger.info("Target path is " + file)
    confirm = tkinter.messagebox.askokcancel('Ruby作成ツール ver.Python',
                                            '以下のファイルのサンプルデータを作成します。\n\n' + file)

    if confirm is not True:
        logger.info("キャンセル")
        exit(0)

    if "インターフェースオーダー定義書" not in file:
        tkinter.messagebox.showerror("Ruby作成ツール ver.Python",
                                     "オーダー定義書ではありません。")
        logger.info("「オーダー定義書」の文言がない")
        exit(0)


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
        logger.info(traceback.format_exc())
        print("Error is occured in reading!")
        print(traceback.format_exc())
        exit(0)
    except co.WritingException:
        logger.info(traceback.format_exc())
        print("Error is occurred in writing!")
        print(traceback.format_exc())
        exit(0)

    tkinter.messagebox.showinfo("Ruby作成ツール ver.Python", "処理が完了しました。\n/source、/bat以下を確認してください")


if __name__ == "__main__":
    main()
