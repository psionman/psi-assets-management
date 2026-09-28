# forms/frm_buttons.py

"""ButtonManagement for psi_assets."""

import tkinter as tk
from tkinter import messagebox, ttk

from psiutils.constants import PAD, Mode
from psiutils.utilities import window_resize
from psiutils.widgets import ScrollingCanvas

from psi_assets.buttons import ButtonFrame, IconButton
from psi_assets.constants import APP_TITLE
from psi_assets.data_store import store as data_store
from psi_assets.forms.frm_button_config_edit import ButtonConfigEditFrame
from psi_assets.forms.frm_convert import ConversionFrame
from psi_assets.state import state
from psi_assets.text import Text

txt = Text()


class ButtonManagement:
    """Create ButtonManagement for psi_assets application."""

    def __init__(self, parent: tk.Tk) -> None:
        self.root = tk.Toplevel(parent.root)
        data_store.buttons.subscribe(self._populate_buttons_frame)

        # tk variables
        self.icon_name = tk.StringVar()
        self.source = tk.StringVar()
        self.button = tk.StringVar()

        # Trace
        self.icon_name.trace_add("write", self._value_changed)

        self._show()
        self._populate_buttons_frame()

    def _show(self):
        root = self.root
        root.geometry(state.get_geometry(__file__))
        root.title(APP_TITLE)

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)

        self.button_frame = self._button_frame(root)
        self.button_frame.grid(
            row=0, column=2, rowspan=9, sticky=tk.NS, padx=PAD, pady=PAD
        )

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(column=2, sticky=tk.SE)

        root.update_idletasks()
        root.bind("<Control-x>", self._dismiss)
        root.bind("<Control-o>", self._process)
        root.bind(
            "<Configure>",
            lambda e: window_resize(root, __file__, state),
        )

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        row = 0
        self.icon_button_frame = ScrollingCanvas(
            frame,
            relief=tk.SUNKEN,
            borderwidth=2,
        )
        self.icon_button_frame.grid(
            row=row, column=0, columnspan=3, sticky=tk.NSEW
        )
        self._bind_mousewheel()
        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.VERTICAL)
        frame.buttons = self._frame_buttons(frame)
        frame.enable(False)
        return frame

    def _frame_buttons(self, frame: ButtonFrame) -> list[IconButton]:
        return [
            frame.icon_button("convert", self._convert),
            frame.icon_button("new-folder", self._new_button),
            frame.icon_button("edit", self._edit_button, True),
            frame.icon_button("delete", self._delete_button, True),
            frame.icon_button("cancel", self._dismiss, icon_colour="red"),
        ]

    def _populate_buttons_frame(self) -> None:
        frame = self.icon_button_frame.content
        for child in frame.winfo_children():
            child.destroy()

        buttons = data_store.buttons
        for row, name in enumerate(sorted(list(buttons.button_configs))):
            button_config = buttons.button_configs[name]

            radio_button = ttk.Radiobutton(
                frame,
                text=name,
                variable=self.button,
                value=name,
                command=self._button_selected,
            )
            radio_button.grid(row=row, column=0, sticky=tk.W, padx=PAD)

            button = IconButton(
                frame,
                text=button_config.text,
                icon=button_config.icon,
            )
            button.grid(row=row, column=1, sticky=tk.W, pady=2)

    def _convert(self, *args) -> None:
        dlg = ConversionFrame(self)
        self.root.wait_window(dlg.root)

    def _button_selected(self) -> None:
        self.button_frame.enable()

    def _new_button(self) -> None:
        dlg = ButtonConfigEditFrame(self, mode=Mode.NEW)
        dlg.root.transient(self.root)
        self.root.wait_window(dlg.root)

    def _edit_button(self) -> None:
        dlg = ButtonConfigEditFrame(
            self,
            mode=Mode.EDIT,
            button_name=self.button.get(),
        )
        dlg.root.transient(self.root)
        self.root.wait_window(dlg.root)

    def _delete_button(self) -> None:
        dlg = messagebox.askyesno(
            "Delete Button",
            "Are you sure you want to delete this button?",
        )
        if dlg:
            # TODO: Delete the button
            del data_store.button_configs[self.button.get()]
            data_store.save()
            self._populate_buttons_frame()

    def _value_changed(self, *args) -> bool:
        """
        Determine whether any configuration value has changed.
        """
        pass
        # enable = self.icon_name.get() != "" and self.source.get() != ""
        # self.button_frame.enable(enable)

    def _process(self, *args) -> None:
        pass

    def _bind_mousewheel(self) -> None:
        canvas = self.icon_button_frame.canvas
        canvas.bind_all(
            "<Button-4>", lambda e: canvas.yview_scroll(-1, "units")
        )
        canvas.bind_all(
            "<Button-5>", lambda e: canvas.yview_scroll(1, "units")
        )

    def _unbind_mousewheel(self) -> None:
        canvas = self.icon_button_frame.canvas
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    def _dismiss(self, *args) -> None:
        self._unbind_mousewheel()
        self.root.destroy()
