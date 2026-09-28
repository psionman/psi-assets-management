# data_store.py
from collections.abc import Callable

from psiutils.buttons import IconButtonConfig

import psi_assets.io_operations as io
from psi_assets.constants import BUTTON_CONFIG_PATH

Listener = Callable[[], None]


class DataStore:
    """Singleton data store for psi_assets."""

    def __init__(self) -> None:
        self.buttons = ButtonStore()


class ButtonStore:
    """Single source of truth for all  buttons in the app."""

    def __init__(self) -> None:
        self._listeners: list[Listener] = []
        self.button_configs: dict[str, dict] = self._get_button_configs()

    def _get_button_configs(self) -> dict[str, IconButtonConfig]:
        button_dict = {}
        buttons_raw = io.read_json_file(BUTTON_CONFIG_PATH)

        for name, button_data in buttons_raw.items():
            button = IconButtonConfig(*button_data)
            button_dict[name] = button

        self._notify()
        return button_dict

    def serialize_button(self, button: IconButtonConfig) -> dict[str, dict]:
        return (button.text, button.icon)

    def save(self, buttons: dict[str, IconButtonConfig] = None) -> int:
        if not buttons:
            buttons = self.button_configs
        self.button_configs = buttons
        output = {
            name: self.serialize_button(button)
            for name, button in buttons.items()
        }
        self._notify()
        return io.update_json_file(BUTTON_CONFIG_PATH, output)

    # -- observer pattern for UI refresh -----------------------------
    def subscribe(self, listener: Listener) -> None:
        self._listeners.append(listener)

    def unsubscribe(self, listener: Listener) -> None:
        self._listeners.remove(listener)

    def _notify(self) -> None:
        for listener in self._listeners:
            listener()


# Module-level singleton - this is the instance everyone imports.
store = DataStore()
