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
    """ruby_source_factory.pyが値を返すかのテスト"""

    def test_append_c_to_n(self):

        sentence = """
    # ==================================================================================================
    # ConversionからHUEへファイル転送する。
    #   source    : Conversion のダウンロード元パスを指定。/nfsroot/interface/client 以下のパスを指定。
    # ==================================================================================================
    syori_no = {no}
    source = {source}
    responsCode, resbStatus, resultbatchIdMap[syori_no], resultfileIdMap[syori_no] = transfer_c2n(access_token, client_id, userid, server, source)
    responsCode, resbStatus = get_status_hue_continuously(access_token, client_id, userid, resultbatchIdMap[syori_no], 10)
"""

        factory.get_c_to_n_text = MagicMock(return_value=sentence)
        sentence = factory.append_c_to_n("3", "/IF55500031")

        expect = """
    # ==================================================================================================
    # ConversionからHUEへファイル転送する。
    #   source    : Conversion のダウンロード元パスを指定。/nfsroot/interface/client 以下のパスを指定。
    # ==================================================================================================
    syori_no = 3
    source = "/IF55500031"
    responsCode, resbStatus, resultbatchIdMap[syori_no], resultfileIdMap[syori_no] = transfer_c2n(access_token, client_id, userid, server, source)
    responsCode, resbStatus = get_status_hue_continuously(access_token, client_id, userid, resultbatchIdMap[syori_no], 10)
"""
        assert sentence == expect

