# forms/frm_convert.py

"""ConversionFrame for psi-assets."""

import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from psiutils.buttons import IconButton
from psiutils.constants import PAD
from psiutils.utilities import window_resize
from psiutils.widgets import status_bar

from psi_assets.buttons import ButtonFrame
from psi_assets.constants import BUTTON_ICON_PATH
from psi_assets.state import state

FRAME_TITLE = "Convert SVG to PNG"

SOURCES = {
    "breeze actions": "/usr/share/icons/breeze/actions/22/",
    "breeze apps": "/usr/share/icons/breeze/apps/22/",
    "breeze preferences": "/usr/share/icons/breeze/preferences/22/",
    "devin": "/opt/devin-desktop-next/resources/app/node_modules/@vscode/codicons/src/icons",
}


class ConversionFrame:
    def __init__(self, parent: tk.Tk) -> None:
        self.root = tk.Toplevel(parent.root)

        # tk variables
        self.icon_name = tk.StringVar()
        self.source = tk.StringVar()
        self.status_text = tk.StringVar()

        # Trace
        self.icon_name.trace_add("write", self._value_changed)

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
            row=1, column=0, columnspan=9, sticky=tk.EW, padx=PAD, pady=PAD
        )
        self.status_bar = status_bar(root, self.status_text)
        self.status_bar.grid(
            row=2, column=0, columnspan=3, sticky=tk.EW, padx=PAD, pady=PAD
        )
        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(row=2, column=99, sticky=tk.SE)

        root.bind("<Control-x>", self._dismiss)
        root.bind("<Control-o>", self._process)
        root.bind(
            "<Configure>",
            lambda event, arg=None: window_resize(root, __file__, state),
        )

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        # frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        row = 0
        source_frame = self._source_frame(frame)
        source_frame.grid(
            row=row, column=0, columnspan=2, sticky=tk.W, padx=PAD, pady=PAD
        )
        row += 1

        label = ttk.Label(frame, text="Icon name")
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.icon_name)
        entry.grid(row=row, column=1, sticky=tk.EW, padx=PAD, pady=PAD)

        return frame

    def _source_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)

        for index, source in enumerate(SOURCES):
            button = ttk.Radiobutton(
                frame,
                text=source,
                variable=self.source,
                value=source,
                command=self._value_changed,
            )
            button.grid(row=index, column=0, sticky=tk.W, padx=PAD, pady=PAD)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = self._frame_buttons(frame)
        frame.enable(False)
        return frame

    def _frame_buttons(self, frame: ButtonFrame) -> list[IconButton]:
        return [
            frame.icon_button("convert", self._process, True),
            frame.icon_button("cancel", self._dismiss),
        ]

    def _value_changed(self, *args) -> bool:
        """
        Determine whether any configuration value has changed.
        """
        enable = self.icon_name.get() != "" and self.source.get() != ""
        self.button_frame.enable(enable)

    def _process(self, *args) -> None:
        icon_name = self.icon_name.get()
        icon_name = icon_name.lower().replace(".svg", "")
        source = SOURCES[self.source.get()]

        if not Path(source, f"{icon_name}.svg").exists():
            print(f"Icon not found: {Path(source, f'{icon_name}.svg')}")
            messagebox.showerror("Error", "Icon not found", parent=self.root)
            return

        # rsvg-convert -w 512 -h 512 $source/$icon.svg -o $target/$icon.png
        subprocess.run(
            [
                "rsvg-convert",
                "-w",
                "512",
                "-h",
                "512",
                Path(source, f"{icon_name}.svg"),
                "-o",
                Path(BUTTON_ICON_PATH, f"{icon_name}.png"),
            ]
        )
        self.status_text.set(f"Icon {icon_name} converted")

    def _dismiss(self, *args) -> None:
        self.root.destroy()
