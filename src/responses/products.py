import typing

import aiogram.types

from keyboards.buttons import navigation_buttons
from keyboards.inline import product_keyboards, callback_factories, payments_keyboards
from responses import base
from services.db_api import schemas


class CategoriesResponses(base.BaseResponse):
    def __init__(self, update: aiogram.types.Message | aiogram.types.CallbackQuery,
                 categories: list[schemas.Category]):
        self.__update = update
        self.__categories = categories
        self.__keyboard = product_keyboards.CategoriesKeyboard(categories)

    async def _send_response(self) -> aiogram.types.Message:
        message_text = (
            '📂 All available categories' if self.__categories
            else '😔 Oh, there is nothing here (')
        if isinstance(self.__update, aiogram.types.CallbackQuery):
            await self.__update.answer()
            if len(self.__update.message.photo) > 0:
                await self.__update.message.delete()
                return await self.__update.message.answer(message_text, reply_markup=self.__keyboard)
            return await self.__update.message.edit_text(message_text, reply_markup=self.__keyboard)
        elif isinstance(self.__update, aiogram.types.Message):
            return await self.__update.answer(message_text, reply_markup=self.__keyboard)


class CategoryItemsResponse(base.BaseResponse):
    def __init__(self, update: aiogram.types.Message | aiogram.types.CallbackQuery,
                 items: list[tuple[int, str, str]], category_id: int):
        self.__update = update
        self.__items = items
        self.__keyboard = product_keyboards.CategoryItemsKeyboard(items, category_id)

    async def _send_response(self) -> aiogram.types.Message:
        message_text = (
            '🛒 All available products and subcategories' if self.__items
            else '😔 Oh, there is nothing here ('
        )
        if isinstance(self.__update, aiogram.types.CallbackQuery):
            await self.__update.answer()
            if len(self.__update.message.photo) > 0:
                await self.__update.message.delete()
                return await self.__update.message.answer(message_text, reply_markup=self.__keyboard)
            return await self.__update.message.edit_text(message_text, reply_markup=self.__keyboard)
        elif isinstance(self.__update, aiogram.types.Message):
            return await self.__update.answer(message_text, reply_markup=self.__keyboard)


class SubcategoryProductsResponse(base.BaseResponse):
    def __init__(self, update: aiogram.types.Message | aiogram.types.CallbackQuery,
                 category_id: int, subcategory_id: int, products: list[schemas.Product]):
        self.__update = update
        self.__products = products
        self.__keyboard = product_keyboards.SubcategoryProductsKeyboard(products, category_id, subcategory_id)

    async def _send_response(self):
        message_text = (
            '🛒 All available products' if self.__products
            else '😔 Oh, there is nothing here ('
        )
        if isinstance(self.__update, aiogram.types.CallbackQuery):
            await self.__update.answer()
            if len(self.__update.message.photo) > 0:
                await self.__update.message.delete()
                return await self.__update.message.answer(message_text, reply_markup=self.__keyboard)
            return await self.__update.message.edit_text(message_text, reply_markup=self.__keyboard)
        elif isinstance(self.__update, aiogram.types.Message):
            return await self.__update.answer(message_text, reply_markup=self.__keyboard)


class ProductResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, product: schemas.Product,
                 product_quantity: int, category_id: int, subcategory_id: int = None,
                 picture: typing.BinaryIO = None):
        self.__query = query
        self.__product = product
        self.__picture = picture
        self.__product_quantity = product_quantity
        self.__is_available = product_quantity > 0
        self.__keyboard = product_keyboards.ProductKeyboard(
            self.__product.id, self.__product_quantity, category_id, subcategory_id, self.__is_available
        )

    async def _send_response(self) -> aiogram.types.Message:
        message_text = (
            f'📓 Name: {self.__product.name}\n'
            f'📋 Description:\n {self.__product.description}\n'
            f'💳 Price: ${self.__product.price}.\n\n'
            f'📦 Available to purchase: {self.__product_quantity} pc(s)\n\n'
        )
        if not self.__is_available:
            message_text += '❗️  The items are temporarily unavailable ❗️'

        await self.__query.answer()
        if self.__picture is not None:
            await self.__query.message.delete()
            await self.__query.message.answer_photo(
                self.__picture, caption=message_text, reply_markup=self.__keyboard
            )
        else:
            return await self.__query.message.edit_text(message_text, reply_markup=self.__keyboard)


class ProductQuantityResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, product_id: int, available_quantity: int):
        self.__query = query
        self.__keyboard = product_keyboards.ProductQuantityKeyboard(product_id, available_quantity)

    async def _send_response(self) -> aiogram.types.Message:
        text = '🛒 Enter the required quantity of the product'
        await self.__query.answer()
        if len(self.__query.message.photo) > 0:
            await self.__query.message.delete()
            return await self.__query.message.answer(text, reply_markup=self.__keyboard)
        return await self.__query.message.edit_text(
            text, reply_markup=self.__keyboard
        )


class AnotherProductQuantityResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, available_quantity: int):
        self.__query = query
        self.__available_quantity = available_quantity

    async def _send_response(self):
        message_text = (
            '🛒 Enter the quantity of the required product:\n\n'
            f'Minimum amount: <i>1 pc(s)</i>\n'
            f'Maximum: <i>{self.__available_quantity} pc(s)</i>')

        await self.__query.answer()
        return await self.__query.message.edit_text(message_text, parse_mode='HTML')


class IncorrectQuantity(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self) -> aiogram.types.Message:
        return await self.__message.answer('❗️ Incorrect quantity value ❗️')


class PaymentMethodResponse(base.BaseResponse):
    def __init__(self, update: aiogram.types.CallbackQuery | aiogram.types.Message,
                 callback_data: dict[str:str], crypto_payments: str = None):
        self.__update = update
        callback_data.pop('@')
        self.__keyboard = payments_keyboards.PaymentMethodsKeyboard(
            callback_data, callback_factories.BuyProductCallbackFactory(),
            is_balance=True, crypto_payments=crypto_payments
        )
        self.__keyboard.add(navigation_buttons.InlineBackButton(
            callback_factories.BuyProductCallbackFactory().new(
                **(callback_data | {'quantity': '', 'payment_method': ''})))
        )

    async def _send_response(self) -> aiogram.types.Message:
        message_text = '💳 Choose a desired payment method'
        if isinstance(self.__update, aiogram.types.CallbackQuery):
            await self.__update.answer()
            return await self.__update.message.edit_text(message_text, reply_markup=self.__keyboard)
        elif isinstance(self.__update, aiogram.types.Message):
            return await self.__update.answer(message_text, reply_markup=self.__keyboard)
