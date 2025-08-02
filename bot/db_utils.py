from sqlalchemy.future import select
from sqlalchemy import text
from database import async_session, engine
from models import Project

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Project.metadata.create_all)

async def is_projects_table_exists():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT to_regclass('public.projects')"))
        return result.scalar() is not None

async def is_projects_empty():
    async with async_session() as session:
        result = await session.execute(select(Project))
        return len(result.scalars().all()) == 0

async def add_test_projects():
    test_data = [
        Project(
            title="ProxyFoxy Game 🎮",
            description="Браузерная игра-симулятор сети прокси с элементами стратегии и токенами LUCO.",
            github_url="https://github.com/yanezhvecnikar/proxyfoxy",
            image_url="https://raw.githubusercontent.com/yanezhvecnikar/images/main/image1.png"
        ),
        Project(
            title="LUCO Reputation System 💠",
            description="Ончейн-система репутации в сети TON с рейтингами пользователей.",
            github_url="https://github.com/yanezhvecnikar/luco",
            image_url="https://raw.githubusercontent.com/yanezhvecnikar/images/main/image2.png"
        ),
        Project(
            title="Trading Analytics Bot 📊",
            description="Телеграм-бот для анализа рынка и отправки еженедельных отчётов.",
            github_url="https://github.com/yanezhvecnikar/trading-bot",
            image_url="https://raw.githubusercontent.com/yanezhvecnikar/images/main/image3.png"
        )
    ]
    async with async_session() as session:
        session.add_all(test_data)
        await session.commit()

async def ensure_db_ready():
    if not await is_projects_table_exists():
        await init_db()
    if await is_projects_empty():
        await add_test_projects()

async def add_project(title, description, github_url, image_url):
    async with async_session() as session:
        project = Project(
            title=title,
            description=description,
            github_url=github_url,
            image_url=image_url
        )
        session.add(project)
        await session.commit()

async def delete_project(project_id):
    async with async_session() as session:
        project = await session.get(Project, project_id)
        if project:
            await session.delete(project)
            await session.commit()

async def get_all_projects():
    async with async_session() as session:
        result = await session.execute(select(Project))
        return result.scalars().all()

async def get_project_by_id(project_id: int):
    async with async_session() as session:
        result = await session.execute(select(Project).where(Project.id == project_id))
        return result.scalars().first()
