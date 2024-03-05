from dataclasses import dataclass

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Column,
    Next,
    Row,
    ScrollingGroup,
    Select,
    Start,
)
from aiogram_dialog.widgets.text import Const, Format, Multi

from tgbot.dialogs.callbacks import (
    confirm_reservation,
    entered_num_people,
    invalid_num_people,
    selected_restaurant,
    selected_timeslot,
)
from tgbot.dialogs.states import BookingInfo, MainMenu, RestaurantSelection

main_menu_dialog = Dialog(
    Window(
        Multi(
            Const("Welcome to the Restaurant Reservation Bot!"),
            Const("Please select an option:"),
            sep="\n\n",
        ),
        Start(
            Const("Make a reservation"),
            id="make_reservation",
            state=RestaurantSelection.selection,
        ),
        state=MainMenu.main,
    )
)


@dataclass
class Restaurant:
    id: int
    name: str
    image: str


@dataclass
class TimeSlot:
    time: int
    label: str


async def get_restaurants(dialog_manager: DialogManager, **kwargs):
    return {
        "restaurants": [
            Restaurant(1, "The Seaside Grill", "https://example.com/restaurant1.jpg"),
            Restaurant(
                2, "Mountain View Bistro", "https://example.com/restaurant2.jpg"
            ),
            Restaurant(3, "Urban Garden Vegan", "https://example.com/restaurant3.jpg"),
            Restaurant(
                4, "Grandma's Italian Kitchen", "https://example.com/restaurant4.jpg"
            ),
        ]
    }


async def get_time_slots(dialog_manager: DialogManager, **kwargs):
    return {
        "time_slots": [
            TimeSlot(0, "12:00 PM"),
            TimeSlot(1, "1:00 PM"),
            TimeSlot(2, "2:00 PM"),
            TimeSlot(3, "3:00 PM"),
            TimeSlot(4, "4:00 PM"),
            TimeSlot(5, "5:00 PM"),
            TimeSlot(6, "6:00 PM"),
            TimeSlot(7, "7:00 PM"),
            TimeSlot(8, "8:00 PM"),
            TimeSlot(9, "9:00 PM"),
            TimeSlot(10, "10:00 PM"),
            TimeSlot(11, "11:00 PM"),
            TimeSlot(12, "12:00 AM"),
        ]
    }


async def close_dialog(_, __, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.done()


restaurant_selection_dialog = Dialog(
    Window(
        Const("Please select a restaurant:"),
        Column(
            Select(
                id="restaurants_select",
                items="restaurants",
                item_id_getter=lambda item: item.id,
                on_click=selected_restaurant,
                text=Format("{item.name}"),
            ),
        ),
        getter=get_restaurants,
        state=RestaurantSelection.selection,
    ),
    Window(
        Const("Please select a time:"),
        ScrollingGroup(
            Select(
                id="time_select",
                items="time_slots",
                item_id_getter=lambda item: item.time,
                text=Format("{item.label}"),
                on_click=selected_timeslot,
            ),
            id="time_group",
            height=4,
            width=2,
            hide_on_single_page=True,
        ),
        Back(Const("⬅️ Back")),
        state=RestaurantSelection.time_selection,
        getter=get_time_slots,
    ),
    Window(
        Const("Please enter the number of people:"),
        TextInput(
            id="num_people",
            type_factory=int,
            on_success=entered_num_people,
            on_error=invalid_num_people,
        ),
        Back(Const("⬅️ Back")),
        state=RestaurantSelection.num_people,
    ),
    on_process_result=close_dialog,
)


async def get_user_info(dialog_manager: DialogManager, **kwargs):
    name_widget: TextInput = dialog_manager.find("name")
    contact_widget: TextInput = dialog_manager.find("contact")
    special_requests_widget: TextInput = dialog_manager.find("special_requests")

    return {
        "name": name_widget.get_widget_data(dialog_manager, None),
        "contact": contact_widget.get_widget_data(dialog_manager, None),
        "special_requests": special_requests_widget.get_widget_data(
            dialog_manager, None
        ),
    }


booking_info_dialog = Dialog(
    Window(
        Multi(
            Const("Please enter your name:"),
            Format("Entered name: {name}", when="name"),
            sep="\n\n",
        ),
        TextInput(id="name"),
        Row(
            Cancel(Const("⬅️ Back")),
            Next(when="name"),
        ),
        state=BookingInfo.name,
    ),
    Window(
        Const("Please enter your contact information:"),
        Format("Entered contact: {contact}", when="contact"),
        TextInput(id="contact"),
        Row(
            Back(Const("⬅️ Back")),
            Next(when="contact"),
        ),
        state=BookingInfo.contact,
    ),
    Window(
        Multi(
            Const("Any special requests?"),
            Format("Special requests: {special_requests}", when="special_requests"),
            sep="\n\n",
        ),
        TextInput(id="special_requests"),
        Row(
            Back(Const("⬅️ Back")),
            Next(when="special_requests"),
        ),
        state=BookingInfo.special_requests,
    ),
    Window(
        Multi(
            Const("Please confirm your reservation:"),
            Format("Thank you, {name}!"),
            Format("Contact: {contact}"),
            Format("Number of people: {start_data[num_people]}"),
            Format("Restaurant: {start_data[restaurant_id]}"),
        ),
        Back(Const("⬅️ Back")),
        Button(Const("Confirm"), id="confirm", on_click=confirm_reservation),
        state=BookingInfo.confirm,
    ),
    getter=get_user_info,
)
