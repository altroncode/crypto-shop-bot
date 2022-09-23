import aiogram
from aiogram import dispatcher
from aiogram.dispatcher import filters

import config
import responses.main_menu
from filters import is_admin
from loader import dp
from utils import file_system


@dp.message_handler(filters.Command('cancel'), state='*')
async def cancel(message: aiogram.types.Message, state: dispatcher.FSMContext):
    file_system.delete_dir(config.PENDING_PATH / str(message.from_user.id))
    await state.finish()
    await message.answer('⛔️ Canceled')


@dp.callback_query_handler(filters.Text('close'), state='*')
async def close(query: aiogram.types.CallbackQuery, state: dispatcher.FSMContext):
    file_system.delete_dir(config.PENDING_PATH / str(query.from_user.id))
    await state.finish()
    await query.message.delete()


@dp.message_handler(is_admin.IsUserAdmin(), filters.Text('⬅️ Back'), state='*')
async def cancel(message: aiogram.types.Message, state: dispatcher.FSMContext):
    file_system.delete_dir(config.PENDING_PATH / str(message.from_user.id))
    await state.finish()
    await responses.main_menu.AdminMainMenuResponse(message)


@dp.message_handler(filters.Text('⬅️ Back'), state='*')
async def cancel(message: aiogram.types.Message, state: dispatcher.FSMContext):
    file_system.delete_dir(config.PENDING_PATH / str(message.from_user.id))
    await state.finish()
    await responses.main_menu.UserMainMenuResponse(message)
