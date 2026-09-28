# forms/frm_commit.py

"""Commit frame for psi-assets."""

import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

from psiutils.constants import PAD, WidgetState
from psiutils.utilities import window_resize

from psi_assets import logger
from psi_assets.buttons import ButtonFrame, IconButton
from psi_assets.config import config
from psi_assets.constants import (
    APP_TITLE,
    BUTTON_CONFIG_PATH,
    BUTTON_ICON_PATH,
    PSIUTILS_DIR,
    TEXT_FILE,
)
from psi_assets.main_menu import MainMenu
from psi_assets.state import state
from psi_assets.text import Text

txt = Text()


class CommitFrame:
    """Create CommitFrame for psi-assets application."""

    def __init__(self, parent: tk.Tk) -> None:
        self.root = tk.Toplevel(parent.root)

        # tk variables
        self.button_config_file = tk.StringVar(value=BUTTON_CONFIG_PATH)
        self.button_icon_path = tk.StringVar(value=BUTTON_ICON_PATH)
        self.text_file = tk.StringVar(value=TEXT_FILE)

        # Trace
        # self.xxx.trace_add('write', self._value_changed)

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
            row=8, column=0, columnspan=9, sticky=tk.EW, padx=PAD, pady=PAD
        )

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(column=0, sticky=tk.SE)

        root.update_idletasks()
        root.bind("<Control-x>", self._dismiss)
        root.bind(
            "<Configure>",
            lambda e: window_resize(root, __file__, state),
        )

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        # frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        row = 0
        label = ttk.Label(frame, text="Button Config File")
        label.grid(row=row, column=0, sticky=tk.W, padx=PAD, pady=PAD)
        entry = ttk.Entry(
            frame,
            textvariable=self.button_config_file,
            state=WidgetState.READONLY,
        )
        entry.grid(row=row, column=1, sticky=tk.EW, padx=PAD, pady=PAD)

        row += 1
        label = ttk.Label(frame, text="Button Icon Path")
        label.grid(row=row, column=0, sticky=tk.W, padx=PAD, pady=PAD)
        entry = ttk.Entry(
            frame,
            textvariable=self.button_icon_path,
            state=WidgetState.READONLY,
        )
        entry.grid(row=row, column=1, sticky=tk.EW, padx=PAD, pady=PAD)

        row += 1
        label = ttk.Label(frame, text="Text File")
        label.grid(row=row, column=0, sticky=tk.W, padx=PAD, pady=PAD)
        entry = ttk.Entry(
            frame,
            textvariable=self.text_file,
            state=WidgetState.READONLY,
        )
        entry.grid(row=row, column=1, sticky=tk.EW, padx=PAD, pady=PAD)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = self._frame_buttons(frame)
        frame.enable(False)
        return frame

    def _frame_buttons(self, frame: ButtonFrame) -> list[IconButton]:
        return [
            frame.icon_button("git-commit", self._git_commit),
            frame.icon_button("cancel", self._dismiss),
        ]

    def _value_changed(self, *args) -> bool:
        """
        Determine whether any configuration value has changed.
        """
        enable = self.xxx.get() != config.xxx
        self.button_frame.enable(enable)

    def _git_commit(self, *args) -> None:
        self._run_git_commit(self.commit_text.get(), False)

    def _run_git_commit(self, message: str, push: bool) -> None:
        try:
            subprocess.run(
                ["git", "add", "-A"],
                cwd=PSIUTILS_DIR,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=PSIUTILS_DIR,
                check=True,
                capture_output=True,
                text=True,
            )
            logger.info(
                "git commit", directory=str(PSIUTILS_DIR), message=message
            )

            if push:
                subprocess.run(
                    ["git", "push"],
                    cwd=PSIUTILS_DIR,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                logger.info("git push", directory=str(PSIUTILS_DIR))

        except subprocess.CalledProcessError as e:
            logger.error(
                "git command failed",
                directory=str(PSIUTILS_DIR),
                stdout=e.stdout,
                stderr=e.stderr,
            )
            messagebox.showerror(
                self, title="Git error", message=e.stderr or str(e)
            )

    def _dismiss(self, *args) -> None:
        self.root.destroy()
