from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import get_current_user, security, Authorization
from backend.configs import get_async_session
from backend.repositories import Words
from backend.schemas import Message, Params, UserAuth, WordCreate, WordPublic, WordUpdate, PermissionType

router = APIRouter(
    prefix='/words',
    tags=['Palavras'],
    # dependencies=[Depends(get_token_header)],
)


@router.get(
    '/', status_code=status.HTTP_200_OK, response_model=list[WordPublic]
)
async def list_words(
    pagination: Params = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    words = await Words(session).get_list(pagination)
    return words


@router.get(
    '/{word_id}',
    status_code=status.HTTP_200_OK,
    responses={'404': {'model': Message}},
    response_model=WordPublic,
)
async def get_word(
    word_id: int, session: AsyncSession = Depends(get_async_session)
):
    word = await Words(session).get_by_id(word_id)
    return word


@router.post(
    '/',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(security), Authorization([PermissionType.USER, PermissionType.ADMIN])],
    responses={'403': {'model': Message}, '409': {'model': Message}}
)
#Depends(has_role_admin),
async def create_word(
    word: WordCreate,
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await Words(session).create(word, current_user)


@router.put(
    '/{word_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(security)],
    responses={'403': {'model': Message},'404': {'model': Message}, '409': {'model': Message}},
)
async def update_word(
    word_id: int,
    word: WordUpdate,
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    await Words(session).update_by_id(word_id, word, current_user)


