from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from tgbot.dialogs.states import BookingInfo, RestaurantSelection


async def selected_restaurant(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["restaurant_id"] = item_id
    await dialog_manager.switch_to(RestaurantSelection.time_selection)
    # await dialog_manager.next()


async def selected_timeslot(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["time_slot"] = item_id
    await dialog_manager.switch_to(RestaurantSelection.num_people)


async def entered_num_people(
    message: Message,
    widget: ManagedTextInput[int],
    dialog_manager: DialogManager,
    value: int,
):
    dialog_manager.dialog_data["num_people"] = value
    await dialog_manager.start(state=BookingInfo.name, data=dialog_manager.dialog_data)


async def invalid_num_people(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    value: int,
):
    await message.reply("Invalid number of people. Please try again.")


async def confirm_reservation(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await callback_query.message.answer("Reservation confirmed!")
    await dialog_manager.done()
