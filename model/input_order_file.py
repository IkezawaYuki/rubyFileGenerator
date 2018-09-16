
import logging
import xlrd

import model.ruby_source_factory as factory
import model.output_ruby_file as out

h = logging.FileHandler("log.txt")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def execute(filepath):
    """エクセルの情報を取得します。Ruby作成に必要のないsheetは無視します。"""
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
            strs = read_info_row(row)
            if strs is None:
                continue
            strings.append(strs)
        out.execute_output(strings)


def create_args(argCell):
    arg = str(argCell).replace("\n", " ")
    arg = arg.replace("\r\n", " ")
    return arg


def adjust_number_format(syoriNo):
    if len(syoriNo) > 0:
        number = float(syoriNo)
        number = int(number)
        return str(number)
    return ""

def read_info_row(row):
    syoriNo = str(row[7].value)
    processContentsCell = str(row[8].value)
    processExecCell = str(row[9].value)
    ifCode = str(row[10].value)
    syoriNoToUse = str(row[11].value)
    convFilePathCell = str(row[12].value)
    productName = str(row[13].value)
    batchName = str(row[14].value)
    argCell = str(row[15].value)


    processContents = processContentsCell[0:1]
    processExec = processExecCell[0:1]
    convFilePath = convFilePathCell.replace("%UPDOWN_ROOT%", "")

    arg = create_args(argCell)

    syoriNo = adjust_number_format(syoriNo)
    syoriNoToUse = adjust_number_format(syoriNoToUse)

    logger.info("syoriNo=" + syoriNo + ", processExec=" + processExec +
                ", ifCode=" + ifCode + ", syoriNoToUse=" + syoriNoToUse +
                ", convFilePath=" + convFilePath + ", productName=" +
                productName + ", batchName=" + batchName + ", arg=" + arg)

    strs = read_cell_info(syoriNo, processContents, processExec, ifCode,
                          syoriNoToUse, convFilePath
                          , productName, batchName, arg)
    return strs


def read_cell_info(syoriNo, processContents, processExec, ifCode, syoriNoToUse, convFilePath
                       , productName, batchName, arg):
    if processContents == "9":
        logger.info("appendN2C")
        return factory.appendN2C(syoriNo, syoriNoToUse, convFilePath)
    elif processContents == "1" and processExec == "N":
        logger.info("appendC2N")
        return factory.appendC2N(syoriNo, convFilePath)
    elif processExec == "N":
        logger.info("dispatchNative")
        return dispatch_native(syoriNo, processContents, ifCode, syoriNoToUse)
    elif processExec == "C":
        logger.info("distapchConversion")
        return dispatch_conv(syoriNo, processContents, syoriNoToUse,
                             convFilePath, productName, batchName, arg)
    return "Null"


def dispatch_native(syoriNo, processContents, ifCode, syoriNoToUse):
    if processContents == "1":
        logger.info("appendUploadHue")
        return factory.append_upload_hue(syoriNo, "ローカルファイルパス")
    elif processContents == "2":
        return factory.append_download_hue(syoriNo,syoriNoToUse,"ローカルファイルパス")
    elif processContents == "5":
        syoriNoList = syoriNoToUse.split(",")
        return factory.append_transform(syoriNo, ifCode, syoriNoList)


def dispatch_conv(syoriNo,processContents,syoriNoToUse, convFilePath,productName,batchName,arg):
    if processContents == "1":
        return factory.append_file_up_conv(syoriNo, convFilePath)
    elif processContents == "2":
        return factory.append_file_down_conv(syoriNo, convFilePath)
    elif processContents == "6":
        return factory.append_exec_conv_batch(syoriNo, batchName, arg)





