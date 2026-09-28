# forms/frm_main.py

"""AppFrame for psi-assets."""

import tkinter as tk
from tkinter import ttk

from psiutils.constants import PAD
from psiutils.utilities import window_resize

from psi_assets.buttons import ButtonFrame, IconButton
from psi_assets.config import config
from psi_assets.constants import APP_TITLE
from psi_assets.forms.frm_buttons import ButtonManagement
from psi_assets.forms.frm_commit import CommitFrame
from psi_assets.main_menu import MainMenu
from psi_assets.state import state
from psi_assets.text import Text

txt = Text()


class AppFrame:
    """Create AppFrame for psi-assets application."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self._show()

    def _show(self):
        root = self.root
        root.geometry(state.get_geometry(__file__))
        root.title(APP_TITLE)

        main_menu = MainMenu(self)
        main_menu.create()

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)

        self.button_frame = self._button_frame(root)
        self.button_frame.grid(
            row=0, column=0, rowspan=9, sticky=tk.NS, padx=PAD, pady=PAD
        )

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(column=0, sticky=tk.SE)

        root.update_idletasks()
        root.bind("<Control-x>", self._dismiss)
        root.bind("<Control-o>", self._manage_buttons)
        root.bind(
            "<Configure>",
            lambda e: window_resize(root, __file__, state),
        )

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.VERTICAL)
        frame.buttons = self._frame_buttons(frame)
        frame.enable(False)
        return frame

    def _frame_buttons(self, frame: ButtonFrame) -> list[IconButton]:
        return [
            frame.icon_button("build", self._manage_buttons, text="Buttons"),
            frame.icon_button("psi-text", self._manage_buttons),
            frame.icon_button("git-commit", self._git_commit),
            frame.icon_button("cancel", self._dismiss),
        ]

    def _value_changed(self, *args) -> bool:
        """
        Determine whether any configuration value has changed.
        """
        enable = self.xxx.get() != config.xxx
        self.button_frame.enable(enable)

    def _manage_buttons(self, *args) -> None:
        dlg = ButtonManagement(self)
        dlg.root.transient(self.root)
        self.root.wait_window(dlg.root)

    def _git_commit(self, *args) -> None:
        dlg = CommitFrame(self)
        dlg.root.transient(self.root)
        self.root.wait_window(dlg.root)

    def _dismiss(self, *args) -> None:
        self.root.destroy()
