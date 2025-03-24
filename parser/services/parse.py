"""
File with services for parsing wb pages.
"""

from re import compile as re_compile

from loguru import logger
from aiohttp import ClientSession


url_pattern = re_compile(r'catalog\/(.*?)\/detail\.aspx')


def get_session() -> ClientSession:
    """
    Get aiohttp client session.
    """

    return ClientSession()


def parse_url(url: str) -> tuple[int, int, int]:
    """
    Parse the url to get the volume number,
    part number and product number.

    Obtained by deobfuscating the JS code
    from the WB product page
    """

    product_number = None
    volume_number = None
    part_number = None

    if url.startswith('https://www.wildberries.ru/catalog/'):
        url_match = url_pattern.search(url)

        if url_match:
            product_number = url_match.group(1)

    elif url.isdigit():
        product_number = url

    else:
        raise ValueError('Invalid url')

    if product_number:

        product_number = int(product_number)
        part_number = int(product_number // 1e3)
        volume_number = int(product_number // 1e5)

    return product_number, part_number, volume_number


def get_basket_url(
    product_number: int,
    part_number: int,
    volume_number: int,
) -> str:
    """
    Get the basket url for the product.

    Obtained by deobfuscating the JS code
    from the WB product page

    :param product_number: Product number
    :param part_number: Part number
    :param volume_number: Volume number
    :return: Basket url
    """

    basket_number = '01'

    if volume_number <= 143:
        basket_number = '01'

    elif volume_number <= 287:
        basket_number = '02'

    elif volume_number <= 431:
        basket_number = '03'

    elif volume_number <= 719:
        basket_number = '04'

    elif volume_number <= 1007:
        basket_number = '05'

    elif volume_number <= 1061:
        basket_number = '06'

    elif volume_number <= 1115:
        basket_number = '07'

    elif volume_number <= 1169:
        basket_number = '08'

    elif volume_number <= 1313:
        basket_number = '09'

    elif volume_number <= 1601:
        basket_number = '10'

    elif volume_number <= 1655:
        basket_number = '11'

    elif volume_number <= 1919:
        basket_number = '12'

    elif volume_number <= 2045:
        basket_number = '13'

    elif volume_number <= 2189:
        basket_number = '14'

    elif volume_number <= 2405:
        basket_number = '15'

    elif volume_number <= 2621:
        basket_number = '16'

    elif volume_number <= 2837:
        basket_number = '17'

    elif volume_number <= 3053:
        basket_number = "18"

    elif volume_number <= 3269:
        basket_number = '19'

    elif volume_number <= 3485:
        basket_number = '20'

    elif volume_number <= 3701:
        basket_number = '21'

    elif volume_number <= 3917:
        basket_number = '22'

    else:
        basket_number = '23'

    return (f'https://basket-{basket_number}.wbbasket.ru/vol{volume_number}/'
            f'part{part_number}/{product_number}/info/ru/card.json')


async def get_product_info(url: str) -> dict | None:
    """
    Get the product information.

    :param url: URL of the product
    :return: Product information
    """

    # https://basket-13.wbbasket.ru/vol1953/part195336/195336045/info/ru/card.json

    response = None

    product_number, part_number, volume_number = parse_url(url)

    if product_number and part_number and volume_number:
        url = get_basket_url(product_number, part_number, volume_number)

    else:
        return response

    try:
        async with get_session() as session:
            response = await session.get(url)

            if response.status == 200:
                return await response.json()

            raise Exception(f'Failed to get product info from {url}')

    except Exception as e:
        logger.error(f'Failed to get product info from {url}: {e}')

    return response


__all__ = (
    'get_product_info',
)
