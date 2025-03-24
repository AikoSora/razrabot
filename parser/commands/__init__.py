"""
Commands for the WB parser bot.
"""

from quirkink.bot.router import Router

from .parser import router as ParserRouter


router = Router()
router.add_route(ParserRouter)


__all__ = (
    'router',
)
