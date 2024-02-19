from fastapi import FastAPI

from backend.routers import auth, categories, references, words

app = FastAPI(
    redoc_url=None,
    title='WaiWaiTapota API',
    summary='Serviço de API do Dicionário WaiWai - UFOPA',
)

app.include_router(auth)
app.include_router(words)
app.include_router(categories)
app.include_router(references)


@app.get('/', tags=['Health'])
def health() -> dict:
    return {'message': 'hello'}
