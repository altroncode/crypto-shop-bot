import aiogram.types

import config
from keyboards.inline import payments_keyboards
from responses import base
from services.db_api import schemas


class CoinbasePaymentLinkResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, amount: float,
                 quantity: int, payment_url: str):
        self.__query = query
        self.__amount = amount
        self.__quantity = quantity
        self.__keyboard = payments_keyboards.CoinbasePaymentKeyboard(payment_url)

    async def _send_response(self):
        await self.__query.answer()
        await self.__query.message.edit_text(
            "<b>Currency</b>: USD\n"
            f"<b>Quantity</b>: {self.__quantity}\n"
            f"<b>Amount: {self.__amount}</b>",
            reply_markup=self.__keyboard
        )


class FailedPurchaseResponse(base.BaseResponse):

    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self):
        await self.__message.edit_text('🚫 Purchase failed')


class NotEnoughBalanceResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self):
        await self.__query.message.edit_text('⭕️ Not enough balance!')


class PurchaseInformationResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, sale_id: int, product_name: str,
                 quantity: int, amount: float, product_units: list[schemas.ProductUnit]):
        self.__query = query
        self.__sale_id = sale_id
        self.__product_name = product_name
        self.__quantity = quantity
        self.__amount = amount
        self.__product_units = product_units

    async def _send_response(self):
        text = self.get_text()
        await self.__query.answer()
        await self.__query.message.edit_text(text)
        media_group = aiogram.types.MediaGroup()
        for i, unit in enumerate(self.__product_units):
            if unit.type == 'document':
                path = config.PRODUCT_UNITS_PATH / unit.content
                media_group.attach_document(aiogram.types.InputFile(path))
                if (i + 1) % 10 == 0:
                    await self.__query.message.answer_media_group(media_group)
                    media_group = aiogram.types.MediaGroup()

    def get_text(self):
        text = (
            '🛒 Purchase Information\n'
            '➖➖➖➖➖➖➖➖➖➖\n'
            f'🆔 Order Number: {self.__sale_id}\n'
            '➖➖➖➖➖➖➖➖➖➖\n'
            f'📙 Product Name: {self.__product_name}\n'
            f'📦 Quantity: {self.__quantity} pc(s).\n'
            f'💰 Amount of purchase: ${self.__amount}.\n'
            '➖➖➖➖➖➖➖➖➖➖\n'
            '📱 Data:\n\n'
        )

        for product_unit in self.__product_units:
            if product_unit.type == 'text':
                text += f'{product_unit.content}\n'
        return text