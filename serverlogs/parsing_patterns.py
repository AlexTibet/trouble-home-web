CHECKED = ['LogOnline', ]

STEAM_CONNECT = r'LogOnline: STEAM: Adding P2P connection information with user'
REGISTERED = r'LogBeastsOfBermuda: Display: New player' \
             r' [\d]{17} \(CID = [\d]{3,4}\) successfully registered to the game server!'
NEW_PROFILE = r'LogBeastsOfBermuda: Display: Getting new profile for new player '
CONNECT_START = r'LogBeastsOfBermuda: Display: Starting post login streaming process for player'
DISCONNECT = r'LogOnline: STEAM: [\d]{17} has been removed.'

SPAWNED_SAVED_ENTITY = r'LogServerSave: Display: Spawned saved entity for '
SPAWN = r'Playable_Entity_'
RET_IN_SLOTS = r'LogTemp: Display: Saving actor Playable_Entity_'

USER_COMMAND = r'LogUserCommands: Display: < PLAYER= '
MESSAGE = r'LogChat: Display: Received'


DEATH = r'PLAYER DEATH::Reason:'
DEATH_REASON = {
    'Вы умерли от сильного стресса': 'Умер от сильного стресса',
    'Вы умерли от жажды': 'Умер от жажды',
    'Смертельное падение': 'Умер от падения',
    'Вы умерли от удара молнией': 'Умер от удара молнии',
}

TIME_TEMPLATE = '[%Y.%m.%d-%H.%M.%S:%f'
