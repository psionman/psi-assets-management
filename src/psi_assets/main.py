# main.py

"""
A tkinter application for psi_assets.
"""

import sys
import tkinter as tk

from forms.frm_main import AppFrame
from psiutils.utilities import display_icon
from psiutils.widgets import get_styles

from psi_assets import __app_name__, __version__
from psi_assets.constants import APP_TITLE, ICON_FILE
from psi_assets.module_caller import ModuleCaller

PARSER_ARGS = (
    ("module", "Module to load"),
    ("project", "Project name"),
    ("secondary", "Secondary argument"),
)


def main() -> None:
    root = tk.Tk()
    root.title(APP_TITLE)
    display_icon(root, ICON_FILE, ignore_error=True)

    root.protocol("WM_DELETE_WINDOW", root.destroy)

    get_styles()

    if PARSER_ARGS:
        args = ModuleCaller.create_parser(PARSER_ARGS)
        if args.module:
            try:
                ModuleCaller(root, args)
            except Exception:
                root.destroy()
        else:
            AppFrame(root)

    root.mainloop()


if __name__ == "__main__":
    if "--version" in sys.argv:
        print(f"{__app_name__}. Version: {__version__}")
        sys.exit(0)
    main()
