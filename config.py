import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_ids: tuple[int, ...]
    database_url: str
    tz: str

def _parse_admin_ids(raw: str | None) -> tuple[int, ...]:
    if not raw:
        return tuple()
    return tuple(int(x.strip()) for x in raw.split(",") if x.strip().isdigit())

settings = Settings(
    bot_token=os.environ["BOT_TOKEN"],
    admin_ids=_parse_admin_ids(os.environ.get("ADMIN_IDS")),
    database_url=os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./bot.db"),
    tz=os.environ.get("TZ", "Europe/Minsk"),
)
