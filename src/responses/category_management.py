import aiogram.types

import keyboards.inline.category_management_keyboards
from keyboards.inline import common_keybords, callback_factories
from services.db_api import schemas
from keyboards import inline
from responses import base


class CategoriesResponse(base.BaseResponse):
    def __init__(self, update: aiogram.types.Message | aiogram.types.CallbackQuery,
                 categories: list[schemas.Category]):
        self.__update = update
        self.__keyboard = inline.category_management_keyboards.CategoriesKeyboard(categories)

    async def _send_response(self) -> aiogram.types.Message:
        message_text = '📂 All available categories'
        if isinstance(self.__update, aiogram.types.Message):
            return await self.__update.answer(message_text, reply_markup=self.__keyboard)
        elif isinstance(self.__update, aiogram.types.CallbackQuery):
            await self.__update.answer()
            return await self.__update.message.edit_text(
                message_text, reply_markup=self.__keyboard
            )


class AddCategoriesResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self) -> aiogram.types.Message:
        await self.__query.answer()
        return await self.__query.message.edit_text('Enter category name')


class CategoryMenuResponse(base.BaseResponse):
    def __init__(self, update: aiogram.types.CallbackQuery | aiogram.types.Message,
                 category_id: int, category_name: str, subcategories: list[schemas.Subcategory]):
        self.__update = update
        self.__subcategories = subcategories
        self.__category_name = category_name
        self.__keyboard = keyboards.inline.category_management_keyboards.CategoryMenuKeyboard(category_id)

    async def _send_response(self) -> aiogram.types.Message:
        new_line_symbol = "\n"
        message_text = (
            f'📁 Category: {self.__category_name}\n'
            'Available subcategories:\n'
            f'{new_line_symbol.join(["▫️" + subcategory.name for subcategory in self.__subcategories])}\n\n'
            '❗️ When deleting a category/subcategory, Delete All products/categories in it'
        )
        if isinstance(self.__update, aiogram.types.CallbackQuery):
            await self.__update.answer()
            return await self.__update.message.edit_text(message_text, reply_markup=self.__keyboard)
        elif isinstance(self.__update, aiogram.types.Message):
            return await self.__update.answer(message_text, reply_markup=self.__keyboard)


class SuccessRemovalCategoryResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self) -> aiogram.types.Message:
        await self.__query.answer()
        await self.__query.message.delete()
        return await self.__query.message.answer('✅ Category Removed')


class SuccessAddingCategoryResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self) -> aiogram.types.Message:
        return await self.__message.answer(f'✅ Category added successfully')


class DeleteSubcategoriesResponse(base.BaseResponse):
    def __init__(self, update: aiogram.types.CallbackQuery | aiogram.types.Message,
                 subcategories: list[schemas.Subcategory], category_id: int):
        self.__update = update
        self.__keyboard = keyboards.inline.category_management_keyboards.SubcategoriesForRemovalKeyboard(
            subcategories=subcategories, category_id=category_id
        )

    async def _send_response(self) -> aiogram.types.Message:
        message_text = '📁 Select subcategory'
        if isinstance(self.__update, aiogram.types.CallbackQuery):
            await self.__update.answer()
            return await self.__update.message.edit_text(message_text, reply_markup=self.__keyboard)
        elif isinstance(self.__update, aiogram.types.Message):
            await self.__update.answer(message_text, reply_markup=self.__keyboard)


class SuccessRemovalSubcategoryResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self) -> aiogram.types.Message:
        await self.__query.answer()
        return await self.__query.message.edit_text('✅ Category Removed')


class ConfirmationRemovalCategoryResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, number_of_subcategories: int,
                 number_of_products: int, callback_data: dict[str: str]):
        self.__query = query
        self.__number_of_subcategories = number_of_subcategories
        self.__number_of_products = number_of_products
        self.__callback_data = callback_data

    async def _send_response(self) -> None:
        await self.__query.answer()
        await self.__query.message.edit_text(
            self.__get_text(), reply_markup=common_keybords.ConfirmationKeyboard(
                callback_factories.CategoryCallbackFactory(),
                **self.__callback_data)
        )

    def __get_text(self) -> str:
        return (
            f'Are you sure you want to delete this category with {self.__number_of_subcategories} '
            f'subcategories and {self.__number_of_products} products?'
        )


class ConfirmationRemovalSubcategoryResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, number_of_products: int, callback_data: dict[str: str]):
        self.__query = query
        self.__number_of_products = number_of_products
        self.__callback_data = callback_data

    async def _send_response(self) -> None:
        await self.__query.answer()
        await self.__query.message.edit_text(
            self.__get_text(), reply_markup=common_keybords.ConfirmationKeyboard(
                callback_factories.CategoryCallbackFactory(),
                **self.__callback_data)
        )

    def __get_text(self) -> str:
        return f'Are you sure you want to delete this subcategory with {self.__number_of_products} products?'
