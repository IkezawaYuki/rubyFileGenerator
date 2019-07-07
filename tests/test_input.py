import unittest
import freezegun

import controller.control as c
import model.ruby_source_factory as factory

class TestInput(unittest.TestCase):

    def test_create_localpath2(self):
        with freezegun.freeze_time('2015-10-21 12:34:56'):
            filePath = "/IF52300099.csv"
            test_path = local_path2 = "if_filewk_dir + \"\\\\\" + \"" +\
                     filePath.replace("/", "") + "\""
            actual = factory.create_localpath2(test_path)
            self.assertEqual("if_filewk_dir + \"\\\\\" + \"IF52300099_20151021_123456.csv\"", actual)