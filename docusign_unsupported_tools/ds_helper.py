import os
import tempfile
from pprint import pprint

APP_PATH = os.path.dirname(os.path.abspath(__file__))

from ds_config import DSConfig


class DSHelper:
    def __init__(self):
        pass

    @classmethod
    def read_content(cls, path):
        with open(os.path.join(APP_PATH, "data", path), "rb") as binary_file:
            data = binary_file.read()
        return data

    @classmethod
    def print_pretty_json(cls, obj):
        pprint(obj)

    @classmethod
    def ensureDirExistance(cls, param):
        pass

    @classmethod
    def writeByteArrayToFile(cls, filePath, docBytes):
        pass

    @classmethod
    def create_private_key_temp_file(cls, file_suffix):
        """
        create temp file and write into private key string in

        :param file_suffix:
        :return:
        """
        tmp_file = tempfile.NamedTemporaryFile(mode='w+b', suffix=file_suffix)
        f = open(tmp_file.name, "w+")
        f.write(DSConfig.private_key())
        f.close()
        return tmp_file
