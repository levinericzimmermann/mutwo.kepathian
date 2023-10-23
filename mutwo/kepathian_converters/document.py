import os
import subprocess
import typing

import chevron

from mutwo import core_converters
from mutwo import kepathian_converters

__all__ = ("ContentToDocument",)


class ContentToDocument(core_converters.abc.Converter):
    def __init__(self, papersize: typing.Optional[str] = None):
        self._papersize = (
            papersize or kepathian_converters.configurations.DEFAULT_PAPERSIZE
        )

    def convert(
        self, content: str, path: typing.Optional[str] = None, cleanup: bool = True
    ) -> str:
        t = kepathian_converters.constants.TEMPLATE_PATH
        sileext = kepathian_converters.constants.SILEEXT_PATH
        with open(rf"{t}/document.sil.mustache", "r") as f:
            t = f.read()
        r = chevron.render(
            t,
            {
                "content": content,
                "papersize": self._papersize,
                "kepathianlua": f"{sileext}/kepathian.lua",
            },
        )
        if path:
            silepath = f"{path}.sile"
            with open(silepath, "w") as f:
                f.write(r)
            subprocess.call(["sile", silepath, "-o", path])
            if cleanup:
                os.remove(path)
        return r
