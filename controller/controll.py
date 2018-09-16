import logging
import xlrd
import model.input_order_file as infile
import model.output_ruby_file as outfile

h = logging.FileHandler("log.txt")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def execute(filepath):
    """"""
    strings = []
    file = xlrd.open_workbook(filepath)
    for i in range(file.nsheets):
        sheet = file.sheet_by_index(i)
        if sheet.name == "更新履歴" or sheet.name == "表紙" or sheet.name == "環境変数一覧":
            continue

        logger.info("target sheet name is " + str(sheet.name))
        for row_index in range(sheet.nrows):
            row = sheet.row(row_index)
            if row_index < 5:
                continue
            logger.info("target row is" + str(row))
            strs = infile.read_info(row)
            if strs is None:
                continue
            strings.append(strs)
        outfile.execute_output(strings)
