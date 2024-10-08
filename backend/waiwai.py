from fastapi import Depends, FastAPI, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

from backend.configs import Settings, get_async_session
from backend.repositories import Versions
from backend.routers import (
    attachments,
    auth,
    categories,
    meanings,
    references,
    users,
    wordattachments,
    wordmeanings,
    words,
    wordcategory,
)
from backend.schemas import VersionPublic

settings = Settings()

app = FastAPI(
    redoc_url=None,
    title='WaiWaiTapota API',
    summary='Serviço de API do Dicionário WaiWai - UFOPA',
)

app.include_router(auth)
app.include_router(words)
app.include_router(wordmeanings)
app.include_router(meanings)
app.include_router(categories)
app.include_router(references)
app.include_router(wordattachments)
app.include_router(attachments)
app.include_router(wordcategory)
app.include_router(users)


app.mount('/uploads', StaticFiles(directory='backend/static'), 'static')


@app.get('/', tags=['Ping'])
def health() -> dict:
    return {'detail': 'hello world!'}


@app.get(
    '/version',
    status_code=status.HTTP_200_OK,
    response_model=VersionPublic,
    tags=['Versão'],
)
async def get_version(session: AsyncSession = Depends(get_async_session)):
    version = await Versions(session).first()
    return version
