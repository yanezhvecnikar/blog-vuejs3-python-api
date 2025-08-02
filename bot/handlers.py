from aiogram import Router, types, F
from keyboards import main_kb, projects_list_keyboard
from db_utils import get_all_projects, get_project_by_id

router = Router()

@router.message(F.text == "/start")
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Привет! Я Евгений — Vue.js & Python разработчик.\n"
        "Можешь посмотреть мои проекты, навыки и контакты.",
        reply_markup=main_kb
    )

@router.message(F.text.in_(["🧑‍💻 Обо мне", "/about"]))
async def about_me(message: types.Message):
    await message.answer(
        "Я Евгений Ракинцев — Vue.js & Python разработчик.\n"
        "Люблю автоматизацию, UX и чистый код.\n"
        "Опыт: веб-приложения, боты, блокчейн."
    )

@router.message(F.text.in_(["⭐ Навыки", "/skills"]))
async def skills(message: types.Message):
    await message.answer(
        "💻 Backend: Python, FastAPI, Django\n"
        "🎨 Frontend: Vue.js, Tailwind, Vite\n"
        "📦 БД: PostgreSQL, SQLite\n"
        "🤖 Bots: Telegram, Trading Bots"
    )

@router.message(F.text.in_(["📬 Контакты", "/contacts"]))
async def contacts(message: types.Message):
    await message.answer(
        "📧 Email: i@euorik.ru\n"
        "💬 Telegram: @euoriks\n"
        "🌐 Сайт: https://euorik.com\n"
        "📄 Резюме: https://euorik.com/cv.pdf\n"
        "🌐 GitHub: https://github.com/yanezhvecnikar"
    )

@router.message(F.text.in_(["📂 Мои проекты", "/projects"]))
async def cmd_projects(message: types.Message):
    projects = await get_all_projects()
    if not projects:
        await message.answer("Пока нет проектов.")
        return
    await message.answer("Выбери проект:", reply_markup=projects_list_keyboard(projects))

@router.callback_query(F.data.startswith("proj_"))
async def show_project_details(callback: types.CallbackQuery):
    project_id = int(callback.data.replace("proj_", ""))
    project = await get_project_by_id(project_id)
    if not project:
        await callback.answer("Проект не найден", show_alert=True)
        return
    caption = (
        f"<b>{project.title}</b>\n"
        f"{project.description}\n\n"
        f"<a href='{project.github_url}'>🔗 GitHub</a>"
    )
    await callback.message.answer_photo(
        photo=project.image_url,
        caption=caption,
        parse_mode="HTML"
    )
    await callback.answer()