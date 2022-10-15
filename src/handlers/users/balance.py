import decimal

import aiogram
from aiogram import filters

import config
import responses.balance
from filters import is_user_in_db, is_admin
from keyboards.inline import callback_factories
from loader import dp
from services import db_api
from services.db_api import queries
from services.payments_apis import coinbase_api
from states import balance_states


@dp.message_handler(filters.Text('💲 Balance'), is_admin.IsUserAdmin(), is_user_in_db.IsUserInDB())
async def balance(message: aiogram.types.Message):
    with db_api.create_session() as session:
        await responses.balance.BalanceResponse(
            message, queries.get_user(session, telegram_id=message.from_user.id).balance
        )


@dp.callback_query_handler(callback_factories.TopUpBalanceCallbackFactory().filter(
    amount='', payment_method=''), is_user_in_db.IsUserInDB())
async def top_up_balance(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    await responses.balance.BalanceAmountResponse(query)
    await balance_states.TopUpBalance.waiting_for_amount.set()
    await dp.current_state().update_data({'callback_data': callback_data})


@dp.message_handler(is_user_in_db.IsUserInDB(), state=balance_states.TopUpBalance.waiting_for_amount)
async def balance_amount(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    if message.text.replace('.', '').isdigit() and '-' not in message.text:
        callback_data = (await state.get_data())['callback_data']
        callback_data['amount'] = message.text
        await state.finish()
        await responses.balance.PaymentMethodResponse(
            message, callback_data=callback_data,
            crypto_payments=config.PaymentsSettings().crypto_payments
        )
    else:
        await responses.balance.IncorrectBalanceAmountResponse(message)


@dp.callback_query_handler(callback_factories.TopUpBalanceCallbackFactory().filter(payment_method='coinbase'),
                           filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE), is_user_in_db.IsUserInDB())
async def top_up_balance_with_coinbase(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    with db_api.create_session() as session:
        amount = float(callback_data['amount'])
        api = coinbase_api.CoinbaseAPI(config.CoinbaseSettings().api_key)
        charge = api.create_charge('Balance', amount)
        if api.check_payment(charge):
            await responses.balance.SuccessBalanceRefillResponse(query, amount)
        else:
            await responses.balance.SuccessBalanceRefillResponse(query, amount)
        queries.top_up_balance(session, query.from_user.id, decimal.Decimal(str(amount)))