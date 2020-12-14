from serverlogs.serverlogs_config import SERVER_NAMES, OUTPUT_TYPES


class ServerLogsValidator:

    def __init__(self, log_name, server_name, output_type, steam_id=None):
        self._steam_id = steam_id
        self._log_name = log_name
        self._server_name = server_name
        self._output_type = output_type

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
