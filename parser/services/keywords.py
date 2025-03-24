"""
Parsing keywords from the product info.
"""

from os import getenv
from functools import lru_cache

from openai import AsyncOpenAI


@lru_cache
def get_openai_client() -> AsyncOpenAI:
    """
    Get openai client.

    :return: Openai client
    """

    return AsyncOpenAI(
        api_key=getenv('PROXY_API_KEY'),
        base_url='https://api.proxyapi.ru/openai/v1/'
    )


@lru_cache
def get_system_prompts() -> list[str]:
    """
    Get system prompts.
    """

    text_prompts = [
        'You are a keyword parser for a product.',
        'You are given a product info.',
        'You need to parse keywords from the product info.',
        'You need to return a list of keywords.',
        'You need to return a list of keywords in Russian.',
        'Separate keywords with commas.',
    ]

    prompts = []

    for prompt in text_prompts:
        prompts.append({'role': 'system', 'content': prompt})

    return prompts


async def parse_keywords(product_info: dict) -> list[str]:
    """
    Parse keywords from the product info.

    :param product_info: Product info
    :return: List of keywords
    """

    client = get_openai_client()

    response = await client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            *get_system_prompts(),
            {'role': 'user', 'content': product_info}
        ]
    )

    return response.choices[0].message.content
