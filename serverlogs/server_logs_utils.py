from serverlogs.serverlogs_config import SERVER_NAMES, OUTPUT_TYPES, LOG_DIR
from ftplib import FTP, error_perm
from os import path


class ServerLogsValidator:
    """
    Class for validation and getting valid data from server logs form,
    needed for downloads and parsing server logs
    """
    def __init__(self, log_name: str, server_name: str, output_type: str, steam_id=None):
        self._log_name = log_name
        self._server_name = server_name
        self._output_type = output_type
        self._steam_id = steam_id

    def _valid_log_name(self) -> bool:
        return True if isinstance(self._log_name, str) and self._log_name.split('.')[-1] in ('log', 'txt') else False

    def _valid_server_name(self) -> bool:
        return True if self._server_name in SERVER_NAMES else False

    def _valid_output_type(self) -> bool:
        return True if self._output_type in OUTPUT_TYPES else False

    def _valid_steam_id(self) -> bool:
        return True if isinstance(self._steam_id, str) and self._steam_id.isdigit() and len(self._steam_id) == 17 \
            else False

    def validation(self) -> tuple:
        log_name_res = self._valid_log_name()
        server_name_res = self._valid_server_name()
        output_type_res = self._valid_output_type()
        steam_id_res = self._valid_steam_id()
        return log_name_res, server_name_res, output_type_res, steam_id_res

    def get_valid_data(self):
        return {
            'log_name': self._log_name if self._valid_log_name() else None,
            'server_name': self._server_name if self._valid_server_name() else None,
            'output_type': self._output_type if self._valid_output_type() else None,
            'steam_id': self._steam_id if self._valid_steam_id() else None,
        }


class LogsFindAndDownloader:
    """
    class for find and downloads log files from game server
    """

    def __init__(self, host: str, port: int, login: str, password: str):
        self._host = host
        self._port = int(port)
        self._login = login
        self._password = password

    def get_log_file_list(self, directory: str) -> list:
        """ return list log files or list with auth error if fail auth """
        with FTP() as ftp:
            ftp.connect(self._host, self._port)
            try:
                ftp.login(self._login, self._password)
            except error_perm:
                return ['530 Sorry, Authentication failed.']
            return ftp.nlst(directory)

    def download_log_file(self, directory: str, file_name: str):
        """ downloads file and save in downloads/logs directory and return True or False if give exception"""
        with FTP() as ftp:
            ftp.connect(self._host, self._port)
            try:
                ftp.login(self._login, self._password)
            except error_perm:
                return False
            ftp.cwd(directory)
            try:
                with open(f'{path.dirname(__file__)}/{LOG_DIR}/{file_name}', 'wb') as file:
                    ftp.retrbinary('RETR ' + file_name, file.write)
                    return True
            except FileNotFoundError:
                return False

