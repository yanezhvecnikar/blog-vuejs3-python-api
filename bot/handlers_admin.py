from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils import is_admin
from keyboards import admin_kb
from db_utils import add_project, delete_project, get_all_projects

router = Router()

# Открыть админку
@router.message(F.text == "/admin")
async def admin_panel(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("🚫 У вас нет доступа к админке.")
        return
    await message.answer("🔐 Админ-панель", reply_markup=admin_kb)


class AddProject(StatesGroup):
    waiting_for_data = State()

@router.message(F.text == "➕ Добавить проект")
async def add_project_start(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AddProject.waiting_for_data)
    await message.answer(
        "Отправь данные проекта в формате:\n"
        "`Название|Описание|GitHub URL|Image URL`",
        parse_mode="Markdown"
    )

@router.message(AddProject.waiting_for_data)
async def add_project_save(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    try:
        title, desc, github, image = message.text.split("|", 3)
    except ValueError:
        await message.answer("❌ Неверный формат. Пример:\n`Название|Описание|GitHub URL|Image URL`", parse_mode="Markdown")
        return

    await add_project(title.strip(), desc.strip(), github.strip(), image.strip())
    await state.clear()
    await message.answer("✅ Проект добавлен!", reply_markup=admin_kb)


# Удаление проекта
@router.message(F.text == "🗑 Удалить проект")
async def delete_project_start(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("Введи ID проекта для удаления.")


@router.message(F.text.regexp(r"^\d+$"))
async def delete_project_confirm(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    project_id = int(message.text)
    await delete_project(project_id)
    await message.answer(f"🗑 Проект {project_id} удалён.")


# Список проектов
@router.message(F.text == "📜 Список проектов")
async def list_projects(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    projects = await get_all_projects()
    if not projects:
        await message.answer("📂 В базе нет проектов.")
        return
    text = "\n\n".join([f"{p.id}. {p.title}\n{p.github_url}" for p in projects])
    await message.answer(f"📜 Список проектов:\n\n{text}")
