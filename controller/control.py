import datetime
import re
import logging
import xlrd
import tkinter.filedialog
import tkinter.messagebox
from _datetime import datetime

import model.input_order_file as infile
import model.output_ruby_file as outfile

h = logging.FileHandler("log.txt", encoding="utf-8")
logger = logging.getLogger(__name__)
fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s :%(message)s")
h.setFormatter(fmt)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


class ReadingException(Exception):
    pass


class WritingException(Exception):
    pass


def get_output_filepath(filepath):

    c = str(filepath).rindex("/")
    outputpath = str(filepath)[c + 1:]
    target_start = str(outputpath).find("(")
    target_end = str(outputpath).find(")")
    if target_start == -1 or target_end == -1:
        target_name = datetime.now().strftime("%m%d-%H%M")
        return target_name

    target_name = str(outputpath)[target_start+1:target_end]
    alnumReg = re.compile(r'^[a-zA-Z0-9_-]+$')

    if alnumReg.match(target_name) is None:
        target_name = datetime.now().strftime("%m%d-%H%M")
        return target_name
    return target_name


if __name__ == "__main__":
    import doctest
    doctest.testmod()


def execute(filepath):
    strings = []
    output_target_path = get_output_filepath(filepath)
    file = xlrd.open_workbook(filepath)
    bat_files = []

    for page in range(file.nsheets):
        sheet = file.sheet_by_index(page)
        if sheet.name == "更新履歴" or sheet.name == "表紙" or sheet.name == "環境変数一覧":
            continue

        logger.info("これから読み込むシート名は " + str(sheet.name))

        for row_index in range(sheet.nrows):
            row = sheet.row(row_index)
            if row_index < 5:
                continue

            try:
                strs = infile.read_info(row)
            except IOError:
                raise ReadingException()

            if strs is None:
                continue
            strings.append(strs)
        try:
            if len(strings) > 0:
                bat_file = outfile.execute_output(output_target_path, page-1, strings)
                bat_files.append(bat_file)
            strings.clear()
            logger.info(str(sheet.name) + ": このシートの情報をファイルへ書き込むことができました。")
        except IOError:
            raise WritingException()

