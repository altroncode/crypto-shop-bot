import aiogram.types


class ShopButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='đ Products')


class ShopManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='đĻ All Products')


class PaymentManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='đŗ Payment Management')


class ShopInformationButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='đĒ Shop Information')


class BalanceButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='đ˛ Balance')


class SupportButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='đ¨âđģ Support')


class StatisticsButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='đ Statistics')


class UserManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='đââ Users')


class MailingButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='đ§ Newsletter')


class FAQButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='âšī¸ FAQ')


class RulesButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='đ Rules')


class ProfileButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='đą Profile')


class BackupButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='đž Backup')
