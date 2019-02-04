from _datetime import datetime
import logging

h = logging.FileHandler("log.txt", encoding="utf-8")
logger = logging.getLogger(__name__)
fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s :%(message)s")
h.setFormatter(fmt)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def append_c_to_n(syoriNo, filePath):
    """
    ConversionからHUEへファイル転送する。
    """
    strs = get_c_to_n_text()
    file_path = "\"" + filePath + "\""
    strs = strs.format(no=syoriNo, source= file_path)
    logger.info("c2n.txt [ConversionからHUEへファイルを転送する]: Ready to write.")
    return strs


def get_c_to_n_text():
    with open("template/c2n.txt", "r", encoding="utf-8") as f:
        sentence = f.read()
    return sentence


def append_n_to_c(syoriNo, syoriNoToUse, filePath):
    """
    HUEからConversionへファイル転送を行う。
    """
    strs = get_n_to_c_text()
    result_id_map = "resultfileIdMap[" + syoriNoToUse + "]"
    file_path = "\"" + filePath + "\""
    strs = strs.format(no=syoriNo, fileid=result_id_map,destination=file_path)
    logger.info("n2c.txt [HUEからConversionへファイル転送する]: Ready to write.")
    return strs


def get_n_to_c_text():
    with open("template/n2c.txt", "r",encoding="utf-8") as f:
        sentence = f.read()
    return sentence


def append_upload_hue(syoriNo, localFileName):
    """
    HUEへファイルをアップロードする。
    """
    strs = get_upload_hue_text()
    localFile = "if_filein_dir + \"\\\\\" + \"" + localFileName + "\""
    strs = strs.format(no=syoriNo, localpath=localFile)
    logger.info("uploadHue.txt [HUEへファイルをアップロードする。]: Ready to write.")
    return strs


def get_upload_hue_text():
    with open("template/uploadHue.txt", "r",encoding="utf-8") as f:
        sentence = f.read()
    return sentence


def append_download_hue(syoriNo,fileNo,localFileName):
    """
    HUEからファイルをダウンロードする。
    """
    strs = get_download_hue_text()
    file_no = "resultfileIdMap[" + fileNo + "]"
    local_file_name = "if_fileout_dir + \"\\\\\" + \"" + localFileName + "\""
    strs = strs.format(no=syoriNo, fileid=file_no, localpath=local_file_name)
    logger.info("downloadHue.txt [HUEからファイルをダウンロードする。]: Ready to write.")
    return strs


def get_download_hue_text():
    with open("template/downloadHue.txt", encoding="utf-8") as f:
        sentence = f.read()
    return sentence


def append_transform(syoriNo, transformcode, syoriNoList):
    """
    Converterで変換する。
    """
    strs = get_transform_text()
    transform_code = "\"" + transformcode + "\""
    inputfile_id_map = ""

    for i, syoriNoToUse in enumerate(syoriNoList):
        temp = "inputfileIdMap[\"" + str(i+1) + "\"] = fileid = " \
               + "resultfileIdMap[" + syoriNoToUse + "]"
        inputfile_id_map += temp + "\n    "
    strs = strs.format(no=syoriNo, transformcode=transform_code,
                       inputfileIdMap=inputfile_id_map)
    logger.info("transform.txt [Converterで変換する]: Ready to write.")
    return strs


def get_transform_text():
    with open("template/transform.txt",encoding="utf-8") as f:
        sentence = f.read()
    return sentence


def append_exec_conv_batch(syoriNo, batch, arg):
    """
    Conversionでバッチ処理を実行する。
    """
    strs = get_exec_conv_batch_text()
    batch_s = "\"" + batch + "\""
    arg_s = "\"" + arg + "\""

    strs = strs.format(no=syoriNo, batch=batch_s, arg=arg_s)
    logger.info("execConvBatch.txt [Conversionでバッチ処理を実行する] : Ready to write.")
    return strs


def get_exec_conv_batch_text():
    with open("template/execConvBatch.txt",encoding="utf-8") as f:
        sentence = f.read()
    return sentence


def append_exec_conv_batch_ifm(syoriNo, batch, arg):
    """
    Conversionでバッチ処理を実行する。IFM専用のメソッド。
    自動追記処理がこのメソッドの場合だと行われない。
    """
    strs = get_exec_conv_batch_ifm_text()
    batch_s = "\"" + batch + "\""
    arg_s = "\"" + arg + "\""

    strs = strs.format(no=syoriNo, batch=batch_s, arg=arg_s)
    logger.info("execConvBatch.txt [Conversionでバッチ処理を実行する] : Ready to write.")
    return strs


def get_exec_conv_batch_ifm_text():
    with open("template/execConvBatch.txt",encoding="utf-8") as f:
        sentence = f.read()
    return sentence


def append_file_up_conv(syoriNo, filePath):
    """
    Conversionへファイルアップロードを行う。
    """
    strs = get_file_up_conv_text()
    file_path = "\"" + filePath + "\""
    unoverride = "\"false\""
    localpath = "if_filein_dir + \"\\\\\" + \"" + filePath.replace("/", "") + "\""

    strs = strs.format(no=syoriNo, destination=file_path, unoverride=unoverride,localpath=localpath)
    logger.info("fileUpConv.txt [Conversionへファイルアップロードする]: Ready to write.")
    return strs


def get_file_up_conv_text():
    with open("template/fileUpConv.txt", encoding="utf-8") as f:
        sentence = f.read()
    return sentence


def append_file_down_conv_ifm(syoriNo, filePath):
    """
    IFMのログファイルをダウンロードする。
    この処理だけイレギュラーで、オーダー定義書通りの処理を行わない。
    これは、Conversionからダウンロードすると暗号化されたファイルになってしまうため、
    初めから　HUEへ転送　⇒　HUEからダウンロードの処理　へと変更される。
    """
    strs = get_file_down_conv_ifm_text()
    file_path_temp = filePath[:filePath.index('<')]
    jid_name = filePath[filePath.index('<')+1:filePath.index('に')]

    local_path = "if_filewk_dir + \"\\\\\" + \"" + file_path_temp.replace("/", "") + "\""

    filedId = "resultfileIdMap[10" + syoriNo + "]"
    strs = strs.format(no=syoriNo, localpath=local_path, file_path_front=file_path_temp, jid_file=jid_name,
                       fileid=filedId)
    logger.info("fileDownloadIFM.txt [IFM用の処理でファイルをダウンロードする]: Ready to write.")
    logger.info("ログファイルの取得のため処理を自動修正します。")
    return strs


def get_file_down_conv_ifm_text():
    with open("template/fileDownloadIFM.txt", encoding="utf-8") as f:
        sentence = f.read()
    return sentence


def append_file_down_conv(syoriNo, filePath):
    """
    Conversionからファイルをダウンロードする。
    このままConversionからダウンロードすると、暗号化されたファイルが取得されるため、
    自動追記として、HUEへ転送　⇒　HUEからダウンロードの処理　が加えられる。
    """
    strs = get_file_down_conv_text()
    file_path = "\"" + filePath + "\""
    local_path = "if_fileout_dir + \"\\\\\" + \"" + filePath.replace("/", "") + "\""
    local_path2 = "if_filewk_dir + \"\\\\\" + \"" + filePath.replace("/", "") + "\""

    filedId = "resultfileIdMap[10" + syoriNo + "]"
    strs = strs.format(no=syoriNo, source=file_path, localpath=local_path, fileid=filedId, localpath2=local_path2)
    logger.info("fileDownConv.txt [Conversionからファイルをダウンロードする]: Ready to write.")
    logger.info("自動追記します。")
    return strs


def get_file_down_conv_text():
    with open("template/fileDownConv.txt",encoding="utf-8") as f:
        sentence = f.read()
    return sentence


def exchange_file_name(filename):
    if ".csv" in filename:
        pos = filename.find(".")
        temp = filename[:pos]
        date_data = datetime.now().strftime("%Y_%m%d_%H%M")
        filename = temp + "_" + date_data + ".csv"
        return filename
    else:
        return filename