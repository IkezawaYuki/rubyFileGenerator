import os
import tkinter.messagebox
import logging
import xlrd

h = logging.FileHandler("log.txt")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def read_info(filepath):
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
            strings.append(strs)
            strs = ""


def read_info_row(row):
    syoriNo = str(row[7])
    processContentsCell = str(row[8])
    processExecCell = str(row[9])
    ifCode = str(row[10])
    syoriNoToUse = str(row[11])
    convFilePathCell = str(row[12])
    productName = str(row[13])
    batchName = str(row[14])
    argCell = str(row[15])

    print("read_info_row def = " + str(processContentsCell))

    processContents = processContentsCell[0:1]
    processExec = processExecCell[0:1]

    convFilePath = convFilePathCell.replace("%UPDOWN_ROOT%", "")

    arg = create_args(argCell)
    print("arg = " + arg)

    logger.info("syoriNo=" + syoriNo + ", processExec=" + processExec +
                ", ifCode=" + ifCode + ", syoriNoToUse=" + syoriNoToUse +
                ", convFilePath=" + convFilePath + ", productName=" +
                productName + ", batchName=" + batchName + ", arg=" + arg)

    strs = read_cell_info(syoriNo, processContents, processExec, ifCode,
                          syoriNoToUse, convFilePath
                          ,productName, batchName, arg)
    return strs

def create_args(argCell):
    arg = str(argCell).replace("\n", "")
    arg = arg.replace("\r\n", "")
    return arg


def read_cell_info(syoriNo, processContents, processExec, ifCode, syoriNoToUse, convFilePath
                       , productName, batchName, arg):
    if processContents == "9":
        logger.info("appendN2C")
        return appendC2N(syoriNo, syoriNoToUse, convFilePath)
    elif processContents == "1" and processExec == "N":
        logger.info("appendC2N")
        return appendC2N(syoriNo, convFilePath)
    elif processExec == "N":
        logger.info("dispatchNative")
        return dispatch_native(syoriNo, processContents, ifCode, syoriNoToUse)
    elif processExec == "C":
        logger.info("distapchConversion")
        print("dispatchConversion")

    return "Null"


def dispatch_native(syoriNo, processContents, ifCode, syoriNoToUse):
    if processContents == "1":
        logger.info("appendUploadHue")
        print(processContents)
    elif processContents == "2":
        print("appendDownloadHue")
    elif processContents == "5":
        print("processContents")


def dispatch_conv(syoriNo,processContents,syoriNoToUse, convFilePath,productName,batchName,arg):
    if processContents == "1":
        print(processContents)
    elif processContents == "2":
        print("appendDownloadHue")
    elif processContents == "6":
        print("processContents")



def appendC2N(syoriNo, filePath):
    strs = ""
    with open("template/c2n.txt", "r") as f:
        crlf = os.sep()
        strs = f.read()
        strs.format(no=syoriNo, source= crlf + filePath + crlf)
    return strs


def appendN2C(syoriNo, syoriNoToUse, filePath):
    strs = ""
    with open("template/n2c.txt", "r") as f:
        crlf = os.sep()
        strs = f.read()
        strs.format(no=syoriNo, fileid="resultfileIdMap[" + syoriNoToUse + "]",
                    destination=crlf + filePath + crlf)
    return strs


def append_upload_hue(syoriNo, localFileName):
    strs = ""
    with open("template/uploadHue.txt", "r") as f:
        crlf = os.sep()
        strs = f.read()
        localFile = "if_filein_dir + \"\\\\\" + \"" + localFileName + "\""
        strs.format(no=syoriNo, localpath=localFile)
    return strs


def append_download_hue(syoriNo,fileNo,localFileName):
    with open("template/downloadHue.txt") as f:
        strs = f.read()
        file_no = "resultfileIdMap" + fileNo + "]"
        local_file_name = "if_fileout_dir + \"\\\\\" + \"" + localFileName + "\""
    strs.format(no=syoriNo, fileid=file_no, localpath=local_file_name)
    return strs


def append_transform(syoriNo, transformcode, syoriNoList):
    with open("template/transform.txt") as f:
        strs = f.read()
        crlf = os.linesep()
        transform_code = "\"" + transformcode + "\""
    inputfile_id_map = ""

    for i, syoriNoToUse in enumerate(syoriNoList):
        temp = "    inputfileIdMap[\"" + str(i+1) + "\"] = " \
               + "resultfileIdMap[" + syoriNoToUse + "]" + crlf
        inputfile_id_map.append(temp)
    strs.format(no=syoriNoList, transformcode=transform_code, inputfileIdMap=inputfile_id_map)
    return strs









