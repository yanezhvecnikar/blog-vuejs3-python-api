from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from models import Project

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📂 Мои проекты"), KeyboardButton(text="🧑‍💻 Обо мне")],
        [KeyboardButton(text="⭐ Навыки"), KeyboardButton(text="📬 Контакты")]
    ],
    resize_keyboard=True
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить проект")],
        [KeyboardButton(text="🗑 Удалить проект")],
        [KeyboardButton(text="📜 Список проектов")],
    ],
    resize_keyboard=True
)

def projects_list_keyboard(projects: list[Project]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=p.title, callback_data=f"proj_{p.id}")]
            for p in projects
        ]
    )
