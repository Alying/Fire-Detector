import configparser
import itertools
import os

class DSConfig:
    instance = None
    config = {}

    @staticmethod
    def getInstance():
        if DSConfig.instance is None:
            instance = DSConfig()

        return instance

    def __init__(self):
        client_id = os.environ.get('DS_CLIENT_ID', None)
        if client_id is not None:
            self.config["DS_CLIENT_ID"] = client_id
            self.config["DS_AUTH_SERVER"] = os.environ.get("DS_AUTH_SERVER")
            self.config["DS_IMPERSONATED_USER_GUID"] = os.environ.get("DS_IMPERSONATED_USER_GUID")
            self.config["DS_TARGET_ACCOUNT_ID"] = os.environ.get("DS_TARGET_ACCOUNT_ID")
            self.config["DS_SIGNER_1_EMAIL"] = os.environ.get("DS_SIGNER_1_EMAIL")
            self.config["DS_SIGNER_1_NAME"] = os.environ.get("DS_SIGNER_1_NAME")
            self.config["DS_CC_1_EMAIL"] = os.environ.get("DS_CC_1_EMAIL")
            self.config["DS_CC_1_NAME"] = os.environ.get("DS_CC_1_NAME")
            self.config["DS_PRIVATE_KEY"] = os.environ.get("DS_PRIVATE_KEY")
        else:
            ini_file = 'ds_config.ini'
            if os.path.isfile(ini_file):
                config_parser = configparser.ConfigParser()
                with open(ini_file) as fp:
                    # Enable ini file to not have explicit global section
                    config_parser.read_file(itertools.chain(['[global]'], fp), source=ini_file)
                self.config = config_parser['global']
            else:
                raise Exception(f"Missing config file |{ini_file}| and environment variables are not set.")

    def _auth_server(self):
        return self.config['DS_AUTH_SERVER']

    @staticmethod
    def auth_server():
        return DSConfig.getInstance()._auth_server()

    def _client_id(self):
        return self.config['DS_CLIENT_ID']

    @staticmethod
    def client_id():
        return DSConfig.getInstance()._client_id()

    def _impersonated_user_guid(self):
        return self.config["DS_IMPERSONATED_USER_GUID"]

    @staticmethod
    def impersonated_user_guid():
        return DSConfig.getInstance()._impersonated_user_guid()

    def _target_account_id(self):
        return self.config["DS_TARGET_ACCOUNT_ID"]

    @staticmethod
    def target_account_id():
        return DSConfig.getInstance()._target_account_id()

    def _signer_email(self):
        return self.config["DS_SIGNER_1_EMAIL"]

    @staticmethod
    def signer_email():
        return DSConfig.getInstance()._signer_email()

    def _signer_name(self):
        return self.config["DS_SIGNER_1_NAME"]

    @staticmethod
    def signer_name():
        return DSConfig.getInstance()._signer_name()

    def _cc_email(self):
        return self.config["DS_CC_1_EMAIL"]

    @staticmethod
    def cc_email():
        return DSConfig.getInstance()._cc_email()

    def _cc_name(self):
        return self.config["DS_CC_1_NAME"]

    @staticmethod
    def cc_name():
        return DSConfig.getInstance()._cc_name();

    def _private_key(self):
        return self.config["DS_PRIVATE_KEY"]

    @staticmethod
    def private_key():
        return DSConfig.getInstance()._private_key()

    @staticmethod
    def aud():
        auth_server = DSConfig.getInstance()._auth_server()

        if 'https://' in auth_server:
            aud = auth_server[8:]
        else: # assuming http://blah
            aud = auth_server[7:]

        return aud

    @staticmethod
    def api():
        return "restapi/v2"

    @staticmethod
    def permission_scopes():
        return "signature impersonation"

    @staticmethod
    def jwt_scope():
        return "signature"
