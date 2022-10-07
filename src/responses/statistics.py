import typing

import aiogram.types

from keyboards.reply import statistics_keyboard
from responses import base


class User(typing.TypedDict):
    id: int
    username: str
    purchase_number: int
    orders_amount: float


class StatisticsMenuResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message
        self.__keyboard = statistics_keyboard.StatisticsKeyboard()

    async def _send_response(self):
        await self.__message.answer('📊 Statistics', reply_markup=self.__keyboard)


class StatisticsResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, buyers_number: int, orders_amount: float,
                 sold_products_quantity: int, products_sold_units_quantity: list[tuple[str, int]],
                 active_buyers: list[User]):
        self.__message = message
        self.__buyers_number = buyers_number
        self.__orders_amount = orders_amount
        self.__sold_products_quantity = sold_products_quantity
        self.__products_sold_units_quantity = products_sold_units_quantity
        self.__active_buyers = active_buyers

    async def _send_response(self):
        text = (
                f'🙍‍♂ Number of buyers: {self.__buyers_number}\n'
                f'💰 Total Orders: {self.__orders_amount} $.\n'
                '➖➖➖➖➖➖➖➖➖➖\n'
                f'🛒 Number of purchased items: {self.__sold_products_quantity}\n\n' +
                (''.join(
                    [f'▫️ {name} - {quantity}\n' for name, quantity in self.__products_sold_units_quantity]
                )) +
                '➖➖➖➖➖➖➖➖➖➖\n'
                '🙍‍♂ Active buyers:\n\n' +
                ''.join(
                    [f'{buyer["id"]}{"|@" + buyer["username"] if buyer["username"] is not None else ""}|'
                     f'{buyer["purchase_number"]}|{buyer["orders_amount"]}\n'
                     for buyer in self.__active_buyers]
                ) +
                '➖➖➖➖➖➖➖➖➖➖'
        )
        await self.__message.answer(text)
