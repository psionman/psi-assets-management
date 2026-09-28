# forms/frm_button_config_edit.py
"""ButtonConfigEditFrame for psi-assets."""

import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk

from psiutils.buttons import IconButton, IconButtonConfig
from psiutils.constants import PAD, Mode, Status, WidgetState
from psiutils.utilities import window_resize

from psi_assets.buttons import ButtonFrame
from psi_assets.data_store import store as data_store
from psi_assets.state import state

FRAME_TITLE = "Button config editor"


@dataclass
class ChangeRecord:
    name: str
    object_value: any
    new_value: any


class ButtonConfigEditFrame:
    def __init__(self, parent, mode: int, button_name: str = None) -> None:
        self.root = tk.Toplevel(parent.root)
        self.mode = mode
        self.status = Status.NULL

        if not button_name:
            button_config = IconButtonConfig("", "")
        else:
            button_config = data_store.buttons.button_configs[button_name]
        self.button_config = button_config

        # tk variables
        self.button_name = tk.StringVar(value=button_name)
        self.button_text = tk.StringVar(value=button_config.text)
        self.button_icon = tk.StringVar(value=button_config.icon)

        # Trace
        self.button_text.trace_add("write", self._check_value_changed)
        self.button_icon.trace_add("write", self._check_value_changed)

        self.show()

    def show(self):
        root = self.root
        root.geometry(state.get_geometry(__file__))
        root.title(FRAME_TITLE)

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)
        self.button_frame = self._button_frame(root)
        self.button_frame.grid(
            row=8, column=0, columnspan=9, sticky=tk.EW, padx=PAD, pady=PAD
        )
        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(sticky=tk.SE)
        root.bind("<Control-x>", self._dismiss)
        root.bind("<Control-s>", self._save)
        root.bind(
            "<Configure>",
            lambda event, arg=None: window_resize(root, __file__, state),
        )

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        edit_frame = self._edit_frame(frame)
        edit_frame.grid(row=0, column=0, sticky=tk.NSEW)

        return frame

    def _edit_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        frame.columnconfigure(1, weight=1)

        state = (
            WidgetState.NORMAL
            if self.mode in (Mode.EDIT, Mode.NEW)
            else WidgetState.READONLY
        )

        row = 0
        label = ttk.Label(frame, text="Name")
        label.grid(row=row, column=0, sticky=tk.E, pady=PAD)

        entry = ttk.Entry(frame, textvariable=self.button_name, state=state)
        entry.grid(row=row, column=1, sticky=tk.EW, padx=PAD)
        entry.focus_set()

        row += 1
        label = ttk.Label(frame, text="Text")
        label.grid(row=row, column=0, sticky=tk.E, pady=PAD)

        entry = ttk.Entry(
            frame,
            textvariable=self.button_text,
        )
        entry.grid(row=row, column=1, sticky=tk.EW, padx=PAD)

        row += 1
        label = ttk.Label(frame, text="Icon")
        label.grid(row=row, column=0, sticky=tk.E, pady=PAD)

        entry = ttk.Entry(
            frame,
            textvariable=self.button_icon,
        )
        entry.grid(row=row, column=1, sticky=tk.EW, padx=PAD)
        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = self._frame_buttons(frame)
        frame.enable(False)
        return frame

    def _frame_buttons(self, frame: ButtonFrame) -> list[IconButton]:
        return [
            frame.icon_button("save", self._save, True),
            frame.icon_button("cancel", self._dismiss),
        ]

    def _check_value_changed(self, *args) -> None:
        enable = self._record_changes()
        self.button_frame.enable(enable)

    def _record_changes(self) -> dict:
        changes = {}
        tests = [
            ChangeRecord("text", self.button_config.text, self.button_text),
            ChangeRecord("icon", self.button_config.icon, self.button_icon),
        ]
        for test in tests:
            result = self._test_change(test.object_value, test.new_value)
            if result:
                changes[test.name] = result
        return changes

    def _test_change(self, object_value: any, textvariable: any) -> any | None:
        if object_value != textvariable.get():
            return (
                object_value,
                textvariable,
            )
        return None

    def _save(self, *args) -> None:
        data_store.buttons.button_configs[self.button_name.get()] = (
            IconButtonConfig(
                self.button_text.get(),
                self.button_icon.get(),
            )
        )
        data_store.buttons.save(data_store.buttons.button_configs)
        self._dismiss()

    def _dismiss(self, *args) -> None:
        self.root.destroy()
