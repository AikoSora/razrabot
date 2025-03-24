"""
Main file for the WB parser bot.

Quirkink - A set of my private libraries
for convenient and fast development

:author: Mikhail Shevelkov
:copyright: (c) 2025 Mikhail Shevelkov
:license: MIT
"""

from os import getenv

from dotenv import load_dotenv

from quirkink.bot import Application

from commands import router


load_dotenv()


def application_setup():
    """
    Setup the application.

    :return: Application instance
    """

    return Application(
        router=router,
        api_token=getenv('TELEGRAM_BOT_TOKEN'),
    )


app = application_setup()


if __name__ == '__main__':
    app.run()
