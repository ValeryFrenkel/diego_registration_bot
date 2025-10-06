from aiogram.fsm.state import StatesGroup, State

class RegisterFlow(StatesGroup):
    choosing_game = State()
    entering_team_name = State()
    entering_players = State()

class EditNameFlow(StatesGroup):
    entering_new_name = State()

class EditPlayersFlow(StatesGroup):
    entering_new_players = State()

class AddGameFlow(StatesGroup):
    entering_title = State()
    entering_when = State()
    entering_location = State()
    entering_teams_capacity = State()   # лимит по числу команд
    entering_people_capacity = State()  # лимит по числу людей
    confirming_active = State()
