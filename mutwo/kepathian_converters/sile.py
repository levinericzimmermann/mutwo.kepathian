import functools
import operator
import os
import subprocess
import typing

import chevron

from mutwo import core_converters
from mutwo import kepathian_converters
from mutwo import kepathian_events

__all__ = ("ContentToDocument", "KTableToMustacheData", "KTableToSileStr")


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


class KTableToMustacheData(core_converters.abc.Converter):
    def __init__(
        self,
        kvalue_to_mvalue: typing.Callable[
            [kepathian_events.KValue], str
        ] = lambda kvalue: kvalue.value,
        kvalue_to_width: typing.Callable[
            [kepathian_events.KValue], float
        ] = lambda kvalue: getattr(kvalue, "width", 0),
    ):
        self.kvalue_to_mvalue = kvalue_to_mvalue
        self.kvalue_to_width = kvalue_to_width

    def convert(
        self, ktable_to_convert: kepathian_events.KTable, cell_width: float
    ) -> list[dict[str, list[dict[str, str]]]]:
        mtable = []
        for krow in ktable_to_convert:
            mrow = []
            for kcell in krow:
                # The width of a cell represents its full duration.
                # We try to make the individual values as long as their
                # duration is.
                kcell = kcell.copy().set("duration", cell_width)
                # Each KValue may also have a width in itself, and we need to
                # subtract this width from the amount of totally available
                # width (e.g. glue width) to print good results.
                kvalue_widths = (self.kvalue_to_width(kvalue) for kvalue in kcell)
                glues = (
                    rf"\glue[width={float(kvalue.duration - kwidth)}cm]"
                    for kvalue, kwidth in zip(kcell, kvalue_widths)
                )
                mvalues = (self.kvalue_to_mvalue(kvalue) for kvalue in kcell)
                mvalue = "".join(
                    tuple(functools.reduce(operator.add, zip(mvalues, glues)))
                )
                mcell = {"item": mvalue}
                mrow.append(mcell)
            mtable.append({"items": mrow})
        return mtable


class KTableToSileStr(core_converters.abc.Converter):
    def __init__(
        self,
        width: typing.Optional[float] = None,
        ktable_to_mustache_data: KTableToMustacheData = KTableToMustacheData(),
    ):
        self._width = width
        self._ktable_to_mustache_data = ktable_to_mustache_data

    def convert(self, ktable_to_convert: kepathian_events.KTable) -> str:
        width = cell_width = (
            self._width
            or kepathian_converters.constants.PAPERSIZE_TO_WIDTH[
                kepathian_converters.configurations.DEFAULT_PAPERSIZE
            ]
        )
        if column_count := ktable_to_column_count(ktable_to_convert):
            cell_width = (width) / column_count
        mustache_data = self._ktable_to_mustache_data.convert(
            ktable_to_convert, cell_width
        )

        t = kepathian_converters.constants.TEMPLATE_PATH
        with open(rf"{t}/kepathian.sil.mustache", "r") as f:
            t = f.read()

        return chevron.render(
            t,
            {
                "size": cell_width,
                "columns": tuple(range(column_count)),
                "rows": mustache_data,
            },
        )


def ktable_to_column_count(ktable: kepathian_events.KTable) -> int:
    try:
        column_count = len(ktable[0])
    except IndexError:
        return 0
    for r in ktable[1:]:
        assert len(r) == column_count, "Uneven column count!"
    return column_count
