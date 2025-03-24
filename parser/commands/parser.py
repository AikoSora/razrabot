"""
File with commands (start and message handlers)
for the WB parser bot.
"""

from asyncio import create_task

from quirkink.bot.router import Router
from quirkink.bot.request import Request

from services import get_product_info, parse_keywords


router = Router()


@router.message(path='/start')
async def start_handler(request: Request):
    """
    Start handler for the bot.
    """

    await request.message.reply(
        'Привет! Я Razrabot, пришли мне ссылку на продукт или номер продукта '
        'и я пришлю тебе ключевые слова.'
    )


@router.message(path='')
async def parse_handler(request: Request):
    """
    Parse handler for the bot.
    """

    create_task(
        request.bot.send_chat_action(
            chat_id=request.message.chat.id,
            action='typing',
        )
    )

    url = request.message.text

    response = await get_product_info(url)

    text = 'Не получилось получить информацию о товаре'

    if response and response.get('description', None):
        nlp_response = await parse_keywords(response.get('description'))

        text = nlp_response

    await request.message.reply(text=text)


__all__ = (
    'router',
)
