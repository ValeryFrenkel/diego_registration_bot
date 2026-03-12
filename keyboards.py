from typing import Iterable
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def cancel_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="❌ Отмена", callback_data="cancel")
    return kb.as_markup()

def games_list_kb(games: list[tuple[int, str]], page: int = 1, page_size: int = 8) -> InlineKeyboardMarkup:
    total = len(games)
    start = (page - 1) * page_size
    end = start + page_size
    chunk = games[start:end]

    kb = InlineKeyboardBuilder()
    for gid, title in chunk:
        kb.button(text=title, callback_data=f"game:{gid}")
    kb.adjust(1)

    nav_btns: list[InlineKeyboardButton] = []
    if start > 0:
        nav_btns.append(InlineKeyboardButton(text="⬅️", callback_data=f"page:{page-1}"))
    if end < total:
        nav_btns.append(InlineKeyboardButton(text="➡️", callback_data=f"page:{page+1}"))
    nav_btns.append(InlineKeyboardButton(text="🗂 Мои регистрации", callback_data="my_regs"))

    kb.row(*nav_btns)
    return kb.as_markup()

def reg_manage_kb(reg_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✏️ Имя", callback_data=f"edit_name:{reg_id}")
    kb.button(text="👥 Игроки", callback_data=f"edit_players:{reg_id}")
    kb.button(text="🗑 Удалить", callback_data=f"delete_reg:{reg_id}")
    # Если хочешь и эти кнопки в колонку — раскомментируй следующую строку
    # kb.adjust(1); return kb.as_markup()
    kb.adjust(3)
    return kb.as_markup()

def admin_main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="➕ Добавить игру", callback_data="admin:add_game")
    kb.button(text="📋 Список игр", callback_data="admin:list_games")
    kb.adjust(1)
    return kb.as_markup()

def admin_games_kb(items: Iterable[tuple[int, str, bool]]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for gid, title, active in items:
        state = "🟢" if active else "🔴"
        kb.button(text=f"{state} {title}", callback_data=f"admin:game:{gid}")
    kb.adjust(1)
    kb.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="admin:back"))
    return kb.as_markup()

def admin_game_actions_kb(game_id: int, active: bool) -> InlineKeyboardMarkup:
    """
    🔸 Главное изменение: все кнопки идут одной колонкой (kb.adjust(1)),
    чтобы текст полностью помещался и не обрезался «…».
    """
    kb = InlineKeyboardBuilder()
    kb.button(text=("🔒 Выключить приём" if active else "🔓 Включить приём"), callback_data=f"admin:toggle:{game_id}")
    kb.button(text="📊 Команды", callback_data=f"admin:teams:{game_id}")
    kb.button(text="➕ Добавить команду", callback_data=f"admin:add_team:{game_id}")
    kb.button(text="📤 Экспорт CSV", callback_data=f"admin:export:{game_id}")
    kb.button(text="🗑 Удалить игру", callback_data=f"admin:delete:{game_id}")
    kb.adjust(1)  # ← одна кнопка в строку (колонка)
    kb.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="admin:list_games"))
    return kb.as_markup()

def admin_teams_list_kb(pairs: list[tuple[int, str]], game_id: int) -> InlineKeyboardMarkup:
    """
    pairs: [(reg_id, 'Team — 4 чел. ✅'), ...]
    Уже было колонкой; оставляем так.
    """
    kb = InlineKeyboardBuilder()
    for reg_id, label in pairs[:60]:
        kb.button(text=f"🗑 {label}", callback_data=f"admin:delteam:{reg_id}")
    kb.adjust(1)
    kb.row(
        InlineKeyboardButton(text="➕ Добавить команду", callback_data=f"admin:add_team:{game_id}"),
        InlineKeyboardButton(text="⬅️ Назад", callback_data=f"admin:game:{game_id}")
    )
    return kb.as_markup()
