import logging
import xlrd
import model.input_order_file as infile
import model.output_ruby_file as outfile

h = logging.FileHandler("log.txt")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


class ReadingException(Exception):
    pass


class WritingException(Exception):
    pass


def get_output_filepath(filepath):
    c = str(filepath).rindex("/")
    outputpath = str(filepath)[0:c + 1]
    target_start = str(filepath).index("(")
    target_end = str(filepath).index(")")
    target_name = str(filepath)[target_start+1:target_end]
    return outputpath + target_name


def execute(filepath):
    strings = []
    output_target_path = get_output_filepath(filepath)
    file = xlrd.open_workbook(filepath)

    for page in range(file.nsheets):
        sheet = file.sheet_by_index(page)
        if sheet.name == "更新履歴" or sheet.name == "表紙" or sheet.name == "環境変数一覧":
            continue

        logger.info("target sheet name is " + str(sheet.name))

        for row_index in range(sheet.nrows):
            row = sheet.row(row_index)
            if row_index < 5:
                continue
            logger.info("target row is" + str(row))
            try:
                strs = infile.read_info(row)
            except IOError:
                raise ReadingException("error is " + str(row))
            if strs is None:
                continue
            strings.append(strs)
        try:
            outfile.execute_output(output_target_path, page, strings)
        except IOError:
            raise WritingException("error is " + str(sheet.name))