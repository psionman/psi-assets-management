# buttons.py
import tkinter as tk
from collections.abc import Callable

from psiutils.buttons import ButtonFrame as ButtonFrameBase
from psiutils.buttons import IconButton as IconButtonBase
from psiutils.buttons import IconButtonConfig

from .constants import BUTTON_CONFIG_PATH, BUTTON_ICON_PATH
from .text import Text

txt = Text()


class IconButton(IconButtonBase):
    def __init__(
        self,
        master: tk.Frame,
        text: str,
        icon: str,
        command: Callable | None = None,
        dimmable: bool = False,
        *,
        sticky: str = "",
        icon_path: str = BUTTON_ICON_PATH,
        icon_colour: str | tuple[int] = "",
        text_colour: str | tuple[int] = "",
        tag: str = "",
        **kwargs,
    ):
        super().__init__(
            master,
            text,
            icon,
            command,
            dimmable,
            sticky=sticky,
            icon_path=icon_path,
            icon_colour=icon_colour,
            text_colour=text_colour,
            tag=tag,
            **kwargs,
        )


class ButtonFrame(ButtonFrameBase):
    def __init__(
        self,
        master: tk.Frame,
        orientation: str = tk.HORIZONTAL,
        button_config_path: str = BUTTON_CONFIG_PATH,
        icon_path: str = BUTTON_ICON_PATH,
        **kwargs: dict,
    ):
        super().__init__(
            master,
            orientation,
            button_config_path,
            icon_path=icon_path,
            **kwargs,
        )


# copied for safety from psiutils.buttons
psi_assets_defns = {
    "backup": IconButtonConfig(txt.BACKUP, "backup"),
    "build": IconButtonConfig(txt.BUILD, "build"),
    "check": IconButtonConfig(txt.CHECK, "check"),
    "clear": IconButtonConfig(txt.CLEAR, "clear"),
    "close": IconButtonConfig(txt.CLOSE, "cancel"),
    "close-red": IconButtonConfig(txt.CLOSE, "cancel"),
    "code": IconButtonConfig(txt.CODE, "code"),
    "code-blue": IconButtonConfig(txt.CODE, "code"),
    "compare": IconButtonConfig(txt.COMPARE, "compare"),
    "compare-orange": IconButtonConfig(txt.COMPARE, "compare"),
    "config": IconButtonConfig(txt.CONFIG, "gear"),
    "console": IconButtonConfig(txt.KONSOLE, "console"),
    "convert": IconButtonConfig(txt.CONVERT, "convert"),
    "copy_docs": IconButtonConfig(txt.COPY, "copy_docs"),
    "copy_clipboard": IconButtonConfig(txt.COPY, "copy_clipboard"),
    "delete": IconButtonConfig(txt.DELETE, "delete"),
    "download": IconButtonConfig(txt.DOWNLOAD, "download"),
    "diff": IconButtonConfig(txt.DIFF, "diff"),
    "done": IconButtonConfig(txt.DONE, "done"),
    "edit": IconButtonConfig(txt.EDIT, "edit"),
    "exit": IconButtonConfig(txt.EXIT, "cancel"),
    "exit-red": IconButtonConfig(txt.EXIT, "cancel"),
    "exit-orange": IconButtonConfig(txt.EXIT, "cancel"),
    "help": IconButtonConfig(txt.HELP, "help"),
    "new": IconButtonConfig(txt.NEW, "new"),
    "next": IconButtonConfig(txt.NEXT, "next"),
    "open": IconButtonConfig(txt.OPEN, "open"),
    "paste": IconButtonConfig(txt.PASTE, "paste"),
    "pause": IconButtonConfig(txt.PAUSE, "pause"),
    "preferences": IconButtonConfig(txt.PREFERENCES, "preferences"),
    "previous": IconButtonConfig(txt.PREVIOUS, "previous"),
    "process": IconButtonConfig(txt.PROCESS, "process"),
    "redo": IconButtonConfig(txt.REDO, "redo"),
    "refresh": IconButtonConfig(txt.REFRESH, "refresh"),
    "rename": IconButtonConfig(txt.RENAME, "rename"),
    "report": IconButtonConfig(txt.REPORT, "report"),
    "reset": IconButtonConfig(txt.RESET, "reset"),
    "restore": IconButtonConfig(txt.RESTORE, "restore"),
    "restore_database": IconButtonConfig(txt.RESTORE, "restore_database"),
    "restore_page": IconButtonConfig(txt.RESTORE, "restore_page"),
    "revert": IconButtonConfig(txt.REVERT, "revert"),
    "run": IconButtonConfig(txt.RUN, "start"),
    "save": IconButtonConfig(txt.SAVE, "save"),
    "script": IconButtonConfig(txt.SCRIPT, "script"),
    "search": IconButtonConfig(txt.SEARCH, "search"),
    "send": IconButtonConfig(txt.SEND, "send"),
    "start": IconButtonConfig(txt.START, "start"),
    "update": IconButtonConfig(txt.UPDATE, "update"),
    "upgrade": IconButtonConfig(txt.UPGRADE, "upgrade"),
    "upload": IconButtonConfig(txt.UPLOAD, "upload"),
    "use": IconButtonConfig(txt.USE, "done"),
    "windows": IconButtonConfig(txt.WINDOWS, "windows"),
    "windsurf": IconButtonConfig(txt.WINDSURF, "windsurf"),
}
