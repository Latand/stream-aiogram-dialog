from aiogram.fsm.state import State, StatesGroup


class MainMenu(StatesGroup):
    main = State()


class RestaurantSelection(StatesGroup):
    selection = State()
    time_selection = State()
    num_people = State()


class BookingInfo(StatesGroup):
    name = State()
    contact = State()
    special_requests = State()
    confirm = State()
