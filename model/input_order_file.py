
import logging
from _datetime import datetime

import model.ruby_source_factory as factory


h = logging.FileHandler("log.txt")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def adjust_args_format(arg):
    arg_list = arg.split(" ")
    for i, temp in enumerate(arg_list):
        if "システム日付" in temp:
            day = datetime.now().strftime("%Y/%m/%d")
            arg_list[i] = day
        elif "***" in temp:
            print(temp)
            slash = temp.index("/")
            user_code = temp[0:slash]
            arg_list[i] = user_code + "/" + user_code
    return " ".join(arg_list)


def create_args(argCell):
    arg = str(argCell).replace("\n", " ")
    arg = arg.replace("\r\n", " ")
    arg = adjust_args_format(arg)
    return arg


def adjust_number_format(syoriNo):
    if len(syoriNo) > 0:
        number = float(syoriNo)
        number = int(number)
        return str(number)
    return ""


def read_info(row):
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

    if "," not in syoriNoToUse:
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
        logger.info("appendN2C start...")
        return factory.append_n_to_c(syoriNo, syoriNoToUse, convFilePath)
    elif processContents == "1" and processExec == "N":
        logger.info("appendC2N start...")
        return factory.append_c_to_n(syoriNo, convFilePath)
    elif processExec == "N":
        return dispatch_native(syoriNo, processContents, ifCode, syoriNoToUse)
    elif processExec == "C":
        return dispatch_conv(syoriNo, processContents, syoriNoToUse,
                             convFilePath, productName, batchName, arg)
    return "Null"


def dispatch_native(syoriNo, processContents, ifCode, syoriNoToUse):
    if processContents == "1":
        logger.info("append_upload_hue start...")
        return factory.append_upload_hue(syoriNo, "ローカルファイルパス")
    elif processContents == "2":
        logger.info("append_download_hue start...")
        return factory.append_download_hue(syoriNo,syoriNoToUse,"ローカルファイルパス")
    elif processContents == "5":
        logger.info("append_transform start...")
        syoriNoList = syoriNoToUse.split(",")
        return factory.append_transform(syoriNo, ifCode, syoriNoList)


def dispatch_conv(syoriNo,processContents,syoriNoToUse, convFilePath,productName,batchName,arg):
    if processContents == "1":
        logger.info("append_file_up_conv start...")
        return factory.append_file_up_conv(syoriNo, convFilePath)
    elif processContents == "2":
        logger.info("append_file_down_conv start...")
        return factory.append_file_down_conv(syoriNo, convFilePath)
    elif processContents == "6":
        logger.info("append_exec_conv_batch start...")
        return factory.append_exec_conv_batch(syoriNo, batchName, arg)





