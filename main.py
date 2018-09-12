import os
import tkinter.filedialog
import tkinter.messagebox


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
#file = tkinter.filedialog.askopenfilename(filetypes=fTyp,initialdir=iDir)

logger.info("hello")
print("hello")

with open("model/template/footer.txt", "r") as f:
    print(f.read())


#　オーダー定義書を読み込む
reading.read_info()

#　ファイルにRubyを書き込む


