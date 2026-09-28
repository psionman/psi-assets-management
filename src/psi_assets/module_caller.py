# module_caller.py
"""Module caller for psi_assets."""

from psiutils.module_caller import ModuleCaller as ModuleCallerBase

from psi_assets.forms.frm_commit import CommitFrame
from psi_assets.forms.frm_config import ConfigFrame
from psi_assets.forms.frm_convert import ConversionFrame


class ModuleCaller(ModuleCallerBase):
    def __init__(self, root, parsed_args: dict) -> None:
        self.modules = {
            "config": (self._config, None),
            "convert": (self._convert, None),
            "commit": (self._commit, None),
        }
        super().__init__(root, parsed_args)

    def _config(self) -> None:
        print("Calling... config")
        dlg = ConfigFrame(self)
        self.root.wait_window(dlg.root)

    def _convert(self) -> None:
        print("Calling... convert")
        dlg = ConversionFrame(self)
        self.root.wait_window(dlg.root)

    def _commit(self) -> None:
        print("Calling... commit")
        dlg = CommitFrame(self)
        self.root.wait_window(dlg.root)
