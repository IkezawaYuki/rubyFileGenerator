
import logging
from _datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import model.ruby_source_factory as factory


h = logging.FileHandler("log.txt", encoding="utf-8")
logger = logging.getLogger(__name__)
fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s :%(message)s")
h.setFormatter(fmt)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def adjust_args_format(arg):
    arg_list = arg.split(" ")
    for i, temp in enumerate(arg_list):
        if "システム日付" in temp:
            today = datetime.now().strftime("%Y/%m/%d")
            arg_list[i] = today
        elif "当月末" in temp:
            today = datetime.today()
            last_day = (today + relativedelta(months=1)
                        ).replace(day=1) - timedelta(days=1)
            last_day = datetime.strftime(last_day, '%Y/%m/%d')
            arg_list[i] = last_day
        elif "前月末" in temp:
            today = datetime.today()
            last_day_last_month = today.replace(day=1) - timedelta(days=1)
            last_day_last_month = datetime.strftime(last_day_last_month, '%Y/%m/%d')
            arg_list[i] = last_day_last_month
        elif "***" in temp:
            slash = temp.index("/")
            user_code = temp[0:slash]
            arg_list[i] = user_code + "/" + user_code
        elif temp.isdecimal():
            arg_list[i] = str(int(temp))
    return " ".join(arg_list)


def create_args(argCell):
    """
    >>> arg = ["r", "ikezawa/******","<システム日付>", "n", "<当月末日>", "r", "<前月末日>"]
    >>> create_args(arg)
    4
    :param argCell:
    :return:
    """
    arg = str(argCell).replace("  ", " ")
    arg = arg.replace("\n", " ")
    arg = arg.replace("\r\n", " ")
    arg = adjust_args_format(arg)
    return arg


if __name__ == "__main__":
    import doctest
    doctest.testmod()


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

    if "," not in syoriNoToUse and syoriNoToUse != "-":
        syoriNoToUse = adjust_number_format(syoriNoToUse)

    logger.info("syoriNo=" + syoriNo + ", processExec=" + processExec +
                ", ifCode=" + ifCode + ", syoriNoToUse=" + syoriNoToUse +
                ", convFilePath=" + convFilePath + ", productName=" +
                productName + ", batchName=" + batchName + ", arg=" + arg)

    strs = read_cell_info(syoriNo, processContents, processExec, ifCode,
                          syoriNoToUse, convFilePath, productName, batchName,
                          arg)
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
    logger.error("Rubyへの書き込みがスキップされた処理があります。")
    return


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
    logger.error("Rubyへの書き込みがスキップされた処理があります。")
    return


def dispatch_conv(syoriNo,processContents,syoriNoToUse, convFilePath,productName,batchName,arg):
    if processContents == "1":
        logger.info("append_file_up_conv start...")
        return factory.append_file_up_conv(syoriNo, convFilePath)
    elif processContents == "2":
        logger.info("append_file_down_conv start...")
        if 'テキスト>' in convFilePath:
            logger.info("append file_down_conv_ifm start...")
            return factory.append_file_down_conv_ifm(syoriNo, convFilePath)
        else:
            logger.info("append file_down_conv start...")
            return factory.append_file_down_conv(syoriNo, convFilePath)
    elif processContents == "3" or processContents == "6":
        logger.info("append_exec_conv_batch start...")
        return factory.append_exec_conv_batch(syoriNo, batchName, arg)
    logger.error("Rubyへの書き込みがスキップされた処理があります。")
    return

