from datetime import datetime, timedelta
from io import open
from os import path
from re import search
from collections import defaultdict
from typing import TextIO

import serverlogs.parsing_patterns as pattern
from serverlogs.serverlogs_config import LOG_DIR


class Player(object):
    """Class to create Player Data"""
    def __init__(self):
        """Initiate Player"""
        self._steam_id = None
        self._game_id = None
        self._name = None
        self._connection_history = []
        self._owning_account = None
        self._last_spawn = None
        self._dino = []
        self._player_history = defaultdict(list)

    def steam_connect(self, time: datetime, steam_id: int):
        """Получение запроса на подключение Steam P2P"""
        self._steam_id = steam_id
        self._connection_history.append(f'МСК-{time}| Попытка подключения')
        self._player_history[time].append(f'МСК-{time}| Попытка подключения {steam_id}\n')

    def set_game_id(self, game_id: int):
        """Присвоение внутриигрового ID"""
        self._game_id = game_id

    def connection(self, time: datetime):
        self._player_history[time].append(f'МСК-{time}| Подключение {self._steam_id}\n')

    def steam_disconnect(self, time: datetime):
        """Отключение соединения Steam P2P"""
        self._connection_history.append(time)
        self._player_history[time].append(
            f'МСК-{time}| {self._name} |{self._steam_id}| Вышел из игры!\n\n'
        )
        self._game_id = None

    def set_owning(self, time: datetime, owning_id: int):
        """Устанавлеваем ID владелца"""
        if self._owning_account is not None and self._owning_account != owning_id:
            self._player_history[time].append(
                f'{self._name} перезашел на другой аккаунт! Теперь его айди {owning_id}\n'
            )
        self._owning_account = owning_id
        self._player_history[time].append(f'Игроку {self._steam_id} установлен ID владельца {owning_id}\n')

    def find_owning(self, steam_id: int) -> int:
        """Проверяем совпадает ли ID игрока с ID владельца"""
        if self._owning_account is not None and steam_id != self._owning_account:
            return self._owning_account
        return steam_id

    def naming(self, time: datetime, name: str):
        if self._name is not None and self._name != name:
            self._player_history[time].append(f'МСК-{time}| Игрок {self._name} сменил ник!\nТеперь он {name}\n')
        self._name = name
        self._player_history[time].append(f'МСК-{time}| Игроку {self._steam_id} присвоен никнейм {name}\n')

    def add_ret_in_slots(self, time: datetime):
        self._player_history[time].append(
            f'\nМСК-{time}| {self._name} |{self._steam_id}| {self._game_id} | вышел в меню слотов,'
            f' он был на {self._last_spawn}\n\n'
        )
        self._last_spawn = None

    def add_spawn(self, time: datetime, dino_type: str):
        """Спавн игрока на дино"""
        self._last_spawn = dino_type
        self._player_history[time].append(
            f'\nМСК-{time}| {self._name} |{self._steam_id}| {self._game_id} | заспавнился на {dino_type}\n\n'
        )

    def add_command(self, time: datetime, cmd: str):
        self._player_history[time].append(
            f'МСК-{time}| {self._name}  прописывает консольную комманду --> {cmd}\n'
        )

    def add_death(self, time: datetime, reason: str, dino: str, killer: str or None, killer_dino: str or None):
        reason = f'{killer} на {killer_dino}' if killer is not None else reason
        self._player_history[time].append(
            f'\nМСК-{time}| {self._name} |{self._steam_id}| {self._game_id} | на {dino} {reason}\n\n'
        )

    def add_kill(self, time: datetime, dino: str, victim: str):
        self._player_history[time].append(
            f'\nМСК-{time}| {self._name} |{self._steam_id}| {self._game_id} | на своём {dino}, убивает {victim}\n\n'
        )

    def add_message(self, time: datetime, mes_type: str, message):
        self._player_history[time].append(
            f'МСК-{time}|{self._steam_id}| {self._game_id} | {mes_type} {self._name} --> {message}'
        )

    def clear_player_info(self):
        self._game_id = None
        self._name = None
        self._connection_history = []
        self._owning_account = None
        self._last_spawn = None
        self._dino = []
        self._player_history = defaultdict(list)

    def __repr__(self):
        return f"Player:{self._name} with SteamID:{self._steam_id}"

    @property
    def get_player_history(self) -> defaultdict:
        return self._player_history

    @property
    def game_id(self):
        return self._game_id

    @property
    def steam_id(self):
        return self._steam_id

    @property
    def name(self):
        return self._name

    @property
    def last_spawn(self):
        return self._last_spawn


class LogParser:
    """ Class for parsing server logs file"""
    def __init__(self, filename: str):
        self._file = f'{path.dirname(__file__)}/{LOG_DIR}/{filename}'
        self._players_list = defaultdict(Player)

    def _message_definition(self, line):
        content = line[search(pattern.MESSAGE, line).end():]
        message_type = 'в ЛС/Групп/Локал чат:' if search(r'Private', content.split('Msg')[0].strip()) \
            else 'в Глобал чат:'
        steam_id, message = content.split('] || Msg:')
        steam_id = int(steam_id.split('[')[-1].strip())
        self._players_list[steam_id].add_message(self._time_identify(line), message_type, message)

    def _death_definition(self, line, log_file):
        time = self._time_identify(line)
        reason = self._death_reason_detect(line)
        steam_id, dino, growth = line.split(r'Dead Player ID:')[-1].split(',')
        steam_id = int(steam_id.strip())
        dino = f'{dino.replace("Dead Player Creature:", "").strip()} ' \
               f'{growth.replace("Dead Player Growth:", "").strip()[:5]}'
        if reason in pattern.DEATH_REASON.keys():
            self._players_list[steam_id].add_death(time, reason, dino, None, None)
        else:
            self._killer_detect(time, steam_id, dino, reason, log_file)

    def _killer_detect(self, time, steam_id, dino, reason, log_file):
        killer_info = log_file.__next__()
        k_id, k_dino, k_growth = killer_info[search(r'Killing Player ID', killer_info).end():].split(',')
        k_id = int(k_id.strip())
        k_dino = k_dino.replace('Killing Player Creature:', '').strip()
        k_growth = k_growth.replace('Killing Player Growth:', '').strip()
        k_dino = f'{k_dino} {k_growth[:5]}'
        victim = f'{self._players_list[steam_id].name} |{steam_id}| на {dino}'
        self._players_list[steam_id].add_death(time, reason, dino, k_id, k_dino)
        self._players_list[k_id].add_kill(time, k_dino, victim)

    def _spawned_definition(self, line: str, log_file: TextIO):
        s_entity, steam_id = line[search(pattern.SPAWNED_SAVED_ENTITY, line).end():].split('owning account')
        s_entity, steam_id = int(s_entity.strip().strip(',')), int(steam_id.strip())
        try:
            steam_id = self._players_list[steam_id].find_owning(steam_id)
        except KeyError:
            pass
        # ищем в следующих строчках на ком игрок заспавнился
        for next_line in log_file:
            if search(pattern.SPAWN, next_line):
                spawn = next_line[search(pattern.SPAWN, next_line).end():].strip()
                self._players_list[steam_id].add_spawn(self._time_identify(next_line), spawn)
                break

    def _disappearance_definition(self, line):
        dino = line[search(pattern.RET_IN_SLOTS, line).end():].strip()
        for player in self._players_list.values():
            if player.last_spawn == dino:
                player.add_ret_in_slots(self._time_identify(line))

    def _connection_definition(self, line: str):
        steam_id = int(line[search(pattern.STEAM_CONNECT, line).end():].split()[0].strip())
        self._players_list[steam_id].steam_connect(self._time_identify(line), steam_id)

    def _registration_definition(self, line: str):
        steam_id = int(line.split(':')[-1].split()[2])
        game_id = int(line.split('=')[-1].split()[0].replace(')', ''))
        self._players_list[steam_id].set_game_id(game_id)

    def _new_profile_definition(self, line: str):
        owning_id, steam_id = line[search(pattern.NEW_PROFILE, line).end():].split('| Owning account ID')
        owning_id, steam_id = int(owning_id.strip()), int(steam_id.strip())
        self._players_list[steam_id].set_owning(self._time_identify(line), owning_id)

    def _login_definition(self, line: str):
        nik_name, steam_id = line[search(pattern.CONNECT_START, line).end():].strip().split('with ID')
        nik_name, steam_id = nik_name.strip(), int(steam_id.strip())
        self._players_list[steam_id].connection(self._time_identify(line))
        self._players_list[steam_id].naming(self._time_identify(line), nik_name)

    def _disconnect_definition(self, line):
        steam_id = int(line.split(':')[-1].split()[0])
        self._players_list[steam_id].steam_disconnect(self._time_identify(line))

    def _console_command_definition(self, line):
        steam_id = int(line[search(pattern.USER_COMMAND, line).end():].split('|')[-3].replace('ID=', '').strip())
        cmd = line.split('|')[-1].strip()[:-1]
        self._players_list[steam_id].add_command(self._time_identify(line), cmd)

    def run(self):
        with open(self._file, 'r', encoding='utf-8') as log_file:
            for line in log_file:
                if search(pattern.MESSAGE, line):
                    self._message_definition(line)
                elif search(pattern.DEATH, line):
                    self._death_definition(line, log_file)
                elif search(pattern.SPAWNED_SAVED_ENTITY, line):
                    self._spawned_definition(line, log_file)
                elif search(pattern.RET_IN_SLOTS, line):
                    self._disappearance_definition(line)
                elif search(pattern.STEAM_CONNECT, line):
                    self._connection_definition(line)
                elif search(pattern.REGISTERED, line):
                    self._registration_definition(line)
                elif search(pattern.NEW_PROFILE, line):
                    self._new_profile_definition(line)
                elif search(pattern.CONNECT_START, line):
                    self._login_definition(line)
                elif search(pattern.DISCONNECT, line):
                    self._disconnect_definition(line)
                elif search(pattern.USER_COMMAND, line):
                    self._console_command_definition(line)
        return True

    @staticmethod
    def _time_identify(line: str) -> datetime:
        return datetime.strptime(line.split(']')[0], pattern.TIME_TEMPLATE) + timedelta(hours=3)

    @staticmethod
    def _death_reason_detect(line):
        killer_name_and_reason = line[search(pattern.DEATH, line).end():search(r', Dead Player Name:', line).start()]
        for reason in pattern.DEATH_REASON.keys():
            if search(reason, killer_name_and_reason):
                return pattern.DEATH_REASON[reason]
