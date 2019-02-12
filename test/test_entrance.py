import pytest
import model.input_order_file as input
import controller.control as control
import model.ruby_source_factory as factory
import freezegun
from unittest.mock import MagicMock

from datetime import datetime


class TestCellInfoReading(object):
    """
    引数を正しくRubyのソースコードに変換できているかどうかのテスト。
    """

    @freezegun.freeze_time('2018/12/26')
    def test_test(self):
        x = "this"
        assert 'h' in x

    @freezegun.freeze_time('2018/12/26')
    def test_adjust_args_format_1(self):
        args = "前月末日"
        result = input.adjust_args_format(args)
        assert(result == "2018/11/30")

    @freezegun.freeze_time('2018/12/26')
    def test_adjust_args_format_2(self):
        args = "当月末"
        result = input.adjust_args_format(args)
        assert(result == "2018/12/31")

    @freezegun.freeze_time('2018/12/26')
    def test_create_args(self):
        args = "-u conversion-cjk-db -c interface_api_ms932/******************* -a 508200101" \
               "-p IF16410099 -f  IF16410099.csv -cnt e /IF16410099.cnt"
        result = input.create_args(args)

        expected = "-u conversion-cjk-db -c interface_api_ms932/interface_api_ms932 -a 508200101" \
                   "-p IF16410099 -f IF16410099.csv -cnt e /IF16410099.cnt"

        assert(result == expected)


class TestCreateFilePath(object):
    """名前から出力ファイル名を想定通りに生成できるかのテスト。"""

    def test_get_output_filepath(self):
        file_path = "test/test/インターフェースオーダー定義書(IF001).xlsx"
        result = control.get_output_filepath(file_path)
        expect = "IF001"
        assert result == expect

    @freezegun.freeze_time('2018/12/26 12:34:56')
    def test_get_output_filepath(self):
        file_path = "test/test/インターフェースオーダー定義書.xlsx"
        result = control.get_output_filepath(file_path)
        expect = "1226-1234"
        assert result == expect


class TestRubyFactory(object):
    """ruby_source_factory.pyが期待している値を返すかのテスト。"""

    C_TO_N_TEXT = """
    syori_no = {no}
    source = {source}
    responsCode, resbStatus, resultbatchIdMap[syori_no], resultfileIdMap[syori_no] = transfer_c2n(access_token, client_id, userid, server, source)
    responsCode, resbStatus = get_status_hue_continuously(access_token, client_id, userid, resultbatchIdMap[syori_no], 10)
"""
    DOWNLOAD_HUE_TEXT = """
    syori_no = {no}
    fileid = {fileid}
    localpath = {localpath}
    download_hue(access_token, client_id, userid, fileid, localpath)
"""
    EXEC_CONV_BATCH_TEXT = """
    syori_no = {no}
    batch = {batch}
    args = {arg}
    responsCode, resbStatus = execute_conversion_batch(access_token, client_id, product,batch ,args )
    responsCode, resbStatus, result = get_status_conversion_batch_continuously(access_token, client_id, product, batch, args, 10)
"""
    FILE_DOWN_CONV_TEXT = """
    syori_no = {no}
    source = {source}
    localpath = {localpath}
    responsCode, resbApiStatus = download_conversion(access_token, client_id, source, server, localpath)

    syori_no = 10{no}
    source = {source}
    responsCode, resbStatus, resultbatchIdMap[syori_no], resultfileIdMap[syori_no] = transfer_c2n(access_token, client_id, userid, server, source)
    responsCode, resbStatus = get_status_hue_continuously(access_token, client_id, userid, resultbatchIdMap[syori_no], 10)

    syori_no = 20{no}
    fileid = {fileid}
    localpath = {localpath2}
    download_hue(access_token, client_id, userid, fileid, localpath)
"""
    FILE_DOWNLOAD_IFM_TEXT = """
    syori_no = 10{no}
    jid = get_ifmjid(if_filewk_dir + "\\" + "{jid_file}")
    source = "{file_path_front}" + jid
    responsCode, resbStatus, resultbatchIdMap[syori_no], resultfileIdMap[syori_no] = transfer_c2n(access_token, client_id, userid, server, source)
    responsCode, resbStatus = get_status_hue_continuously(access_token, client_id, userid, resultbatchIdMap[syori_no], 10)

    syori_no = 20{no}
    fileid = {fileid}
    localpath = {localpath} + jid
    download_hue(access_token, client_id, userid, fileid, localpath)
"""
    FILE_UP_CONV_TEXT = """
    syori_no = {no}
    destination = {destination}
    unoverride = {unoverride}
    localpath = {localpath}
    responsCode, resbApiStatus = upload_conversion(access_token, client_id, destination, unoverride, server, localpath)
"""
    N_TO_C_TEXT = """
    syori_no = {no}
    fileid = {fileid}
    destination = {destination}
    responsCode, resbStatus, resultbatchIdMap[syori_no] = transfer_n2c(access_token, client_id, userid, fileid, server, destination)
    responsCode, resbStatus = get_status_hue_continuously(access_token, client_id, userid, resultbatchIdMap[syori_no], 10)
"""
    UPLOAD_HUE_TEXT = """
    syori_no = {no}
    localpath = {localpath}
    responsCode, resbStatus, resultbatchIdMap[syori_no], resultfileIdMap[syori_no] = upload_hue(access_token, client_id, userid, localpath)
    responsCode, resbStatus = get_status_hue_continuously(access_token, client_id, userid, resultbatchIdMap[syori_no], 10)
"""

    def test_append_c_to_n(self):

        factory.get_c_to_n_text = MagicMock(return_value=self.C_TO_N_TEXT)
        sentence = factory.append_c_to_n("3", "IF55500031")

        expect = """
    syori_no = 3
    source = "IF55500031"
    responsCode, resbStatus, resultbatchIdMap[syori_no], resultfileIdMap[syori_no] = transfer_c2n(access_token, client_id, userid, server, source)
    responsCode, resbStatus = get_status_hue_continuously(access_token, client_id, userid, resultbatchIdMap[syori_no], 10)
"""
        assert sentence == expect

    def test_append_download_hue(self):

        factory.get_download_hue_text = MagicMock(return_value=self.DOWNLOAD_HUE_TEXT)
        sentence = factory.append_download_hue("4", "3", "IF55500031")
        expect = """
    syori_no = 4
    fileid = resultfileIdMap[3]
    localpath = if_fileout_dir + "\\\\" + "IF55500031"
    download_hue(access_token, client_id, userid, fileid, localpath)
"""
        assert sentence == expect
    #
    # def test_append_exec_conv_batch(self):
    #     factory.get_exec_conv_batch_text = MagicMock(return_value=self.EXEC_CONV_BATCH_TEXT)
    #     sentence = factory.append_exec_conv_batch()
    #


    def test_append_file_down_conv(self):
        factory.get_file_down_conv_text = MagicMock(return_value= self.FILE_DOWN_CONV_TEXT)
        sentence = factory.append_file_down_conv("10", "IF55500099")
        expect = """
    syori_no = 10
    source = "IF55500099"
    localpath = if_fileout_dir + "\\\\" + "IF55500099"
    responsCode, resbApiStatus = download_conversion(access_token, client_id, source, server, localpath)

    syori_no = 1010
    source = "IF55500099"
    responsCode, resbStatus, resultbatchIdMap[syori_no], resultfileIdMap[syori_no] = transfer_c2n(access_token, client_id, userid, server, source)
    responsCode, resbStatus = get_status_hue_continuously(access_token, client_id, userid, resultbatchIdMap[syori_no], 10)

    syori_no = 2010
    fileid = resultfileIdMap[1010]
    localpath = if_filewk_dir + "\\\\" + "IF55500099"
    download_hue(access_token, client_id, userid, fileid, localpath)
"""
        assert sentence == expect


    # def test_append_file_download_IFM(self):
    #     factory.get_file_down_conv_ifm_text = MagicMock(return_value=self.FILE_DOWNLOAD_IFM_TEXT)
    #
    #
    # def test_append_file_up_conv(self):
    #     factory.get_file_up_conv_text = MagicMock(return_value=self.FILE_UP_CONV_TEXT)
    #
    #
    # def test_append_n_to_c(self):
    #     factory.get_n_to_c_text = MagicMock(return_value=self.N_TO_C_TEXT)
    #





