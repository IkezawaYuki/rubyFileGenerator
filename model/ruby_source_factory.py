import logging

h = logging.FileHandler("log.txt",encoding="utf-8")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def append_c_to_n(syoriNo, filePath):
    """
    ConversionからHUEへファイル転送する。
    """
    with open("template/c2n.txt", "r",encoding="utf-8") as f:
        strs = f.read()
    file_path = "\"" + filePath + "\""
    strs = strs.format(no=syoriNo, source= file_path)
    return strs


def append_n_to_c(syoriNo, syoriNoToUse, filePath):
    """
    HUEからConversionへファイル転送を行う。
    """
    with open("template/n2c.txt", "r",encoding="utf-8") as f:
        strs = f.read()
    result_id_map = "resultfileIdMap[" + syoriNoToUse + "]"
    file_path = "\"" + filePath + "\""
    strs = strs.format(no=syoriNo, fileid=result_id_map,destination=file_path)
    return strs


def append_upload_hue(syoriNo, localFileName):
    """
    HUEへファイルをアップロードする。
    """
    with open("template/uploadHue.txt", "r",encoding="utf-8") as f:
        strs = f.read()
    localFile = "if_filein_dir + \"\\\\\" + \"" + localFileName + "\""
    strs = strs.format(no=syoriNo, localpath=localFile)
    return strs


def append_download_hue(syoriNo,fileNo,localFileName):
    """
    HUEからファイルをダウンロードする。
    """
    with open("template/downloadHue.txt",encoding="utf-8") as f:
        strs = f.read()
    file_no = "resultfileIdMap" + fileNo + "]"
    local_file_name = "if_fileout_dir + \"\\\\\" + \"" + localFileName + "\""
    strs = strs.format(no=syoriNo, fileid=file_no, localpath=local_file_name)
    return strs


def append_transform(syoriNo, transformcode, syoriNoList):
    """
    Converterで変換する。
    """
    with open("template/transform.txt",encoding="utf-8") as f:
        strs = f.read()
    transform_code = "\"" + transformcode + "\""
    inputfile_id_map = ""

    for i, syoriNoToUse in enumerate(syoriNoList):
        temp = "inputfileIdMap[" + str(i+1) + "] = " \
               + "resultfileIdMap[\"" + syoriNoToUse + "\"]"
        inputfile_id_map += temp + "\n    "
    strs = strs.format(no=syoriNo, transformcode=transform_code,
                       inputfileIdMap=inputfile_id_map)
    return strs


def append_exec_conv_batch(syoriNo, batch, arg):
    """
    Conversionでバッチ処理を実行する。
    """
    with open("template/execConvBatch.txt",encoding="utf-8") as f:
        strs = f.read()
    batch_s = "\"" + batch + "\""
    arg_s = "\"" + arg + "\""

    strs = strs.format(no=syoriNo, batch=batch_s, arg=arg_s)
    logger.info(strs)
    return strs


def append_file_up_conv(syoriNo, filePath):
    """
    Conversionへファイルアップロードを行う。
    """
    with open("template/fileUpConv.txt",encoding="utf-8") as f:
        strs = f.read()
    file_path = "\"" + filePath + "\""
    unoverride = "\"false\""
    localpath = "if_filein_dir + \"\\\\\" + \"" + filePath.replace("/", "") +\
                "\""

    strs = strs.format(no=syoriNo, destination=file_path, unoverride=unoverride,
                       localpath=localpath)
    logger.info(strs)
    return strs


def append_file_down_conv(syoriNo, filePath):
    """
    Conversionからファイルをダウンロードする。
    """
    with open("template/fileDownConv.txt",encoding="utf-8") as f:
        strs = f.read()
    file_path = "\"" + filePath + "\""
    local_path = "if_fileout_dir + \"\\\\\" + \"" +\
                 filePath.replace("/", "") + "\""
    local_path2 = "if_filewk_dir + \"\\\\\" + \"" +\
                 filePath.replace("/", "") + "\""
    filedId = "resultfileIdMap[\"" + syoriNo + "\"]"
    strs = strs.format(no=syoriNo, source=file_path, localpath=local_path,
                       fileid=filedId, localpath2=local_path2)
    logger.info(strs)
    return strs
