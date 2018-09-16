import logging

import model.output_ruby_file as out

h = logging.FileHandler("log.txt")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def appendC2N(syoriNo, filePath):
    with open("model/template/c2n.txt", "r") as f:
        strs = f.read()
    file_path = "\"" + filePath + "\""
    strs = strs.format(no=syoriNo, source= file_path)
    return strs


def appendN2C(syoriNo, syoriNoToUse, filePath):
    with open("model/template/n2c.txt", "r") as f:
        strs = f.read()
    result_id_map = "resultfileIdMap[" + syoriNoToUse + "]"
    file_path = "\"" + filePath + "\""
    strs = strs.format(no=syoriNo, fileid=result_id_map,destination=file_path)
    return strs


def append_upload_hue(syoriNo, localFileName):
    strs = ""
    with open("model/template/uploadHue.txt", "r") as f:
        strs = f.read()
    localFile = "if_filein_dir + \"\\\\\" + \"" + localFileName + "\""
    strs = strs.format(no=syoriNo, localpath=localFile)
    return strs


def append_download_hue(syoriNo,fileNo,localFileName):
    with open("model/template/downloadHue.txt") as f:
        strs = f.read()
    file_no = "resultfileIdMap" + fileNo + "]"
    local_file_name = "if_fileout_dir + \"\\\\\" + \"" + localFileName + "\""
    strs = strs.format(no=syoriNo, fileid=file_no, localpath=local_file_name)
    return strs


def append_transform(syoriNo, transformcode, syoriNoList):
    with open("model/template/transform.txt") as f:
        strs = f.read()
    transform_code = "\"" + transformcode + "\""
    inputfile_id_map = ""

    for i, syoriNoToUse in enumerate(syoriNoList):
        temp = "    inputfileIdMap[\"" + str(i+1) + "\"] = " \
               + "resultfileIdMap[" + syoriNoToUse + "]" + "\\"
        inputfile_id_map += temp + "\n"
    strs = strs.format(no=syoriNo, transformcode=transform_code,
                       inputfileIdMap=inputfile_id_map)
    return strs


def append_exec_conv_batch(syoriNo, batch, arg):
    with open("model/template/execConvBatch.txt") as f:
        strs = f.read()
    batch_s = "\"" + batch + "\""
    arg_s = "\"" + arg + "\""

    strs = strs.format(no=syoriNo, batch=batch_s, arg=arg_s)
    logger.info(strs)
    return strs


def append_file_up_conv(syoriNo, filePath):
    with open("model/template/fileUpConv.txt") as f:
        strs = f.read()
    file_path = "\"" + filePath + "\""
    unoverride = "\"false\""
    localpath = "if_filein_dir + \"\\\\\" + \"" + filePath.replace("/", "") +\
                "\""

    strs = strs.format(no=syoriNo, destination=file_path ,unoverride=unoverride,
                localpath=localpath)
    logger.info(strs)
    return strs

def append_file_down_conv(syoriNo, filePath):
    with open("model/template/fileDownConv.txt") as f:
        strs = f.read()
    file_path = "\"" + filePath + "\""
    local_path = "if_fileout_dir + \"\\\\\" + \"" +\
                 filePath.replace("/", "") + "\""
    strs = strs.format(no=syoriNo, source=file_path, localpath=local_path)
    logger.info(strs)
    return strs
