import os
import unittest

from mutwo import core_events
from mutwo import kepathian_converters

sim, seq, s = (
    core_events.SimultaneousEvent,
    core_events.SequentialEvent,
    core_events.SimpleEvent,
)


class KTableToMustacheDataTest(unittest.TestCase):
    def setUp(self):
        self.c = kepathian_converters.KTableToMustacheData()

    def test_convert(self):
        cell_count = 4
        ktable = simple_ktable(cell_count)
        cell_width = 2.0
        converted_table = self.c.convert(ktable, cell_width)
        self.assertTrue(converted_table)
        converted_cell_ok = {"item": rf"A\glue[width={cell_width}cm]"}
        converted_table_ok = [{"items": [converted_cell_ok for _ in range(cell_count)]}]
        self.assertEqual(converted_table, converted_table_ok)


class KTableToSileStrTest(unittest.TestCase):
    def setUp(self):
        self.c = kepathian_converters.KTableToSileStr()

    def test_convert(self):
        ktable = simple_ktable()
        converted_table = self.c.convert(ktable)
        converted_table_ok = (
            r"\begin{center}"
            r"\kepathian{"
            r"    % Set formatting (minimal width per cell)"
            r"    \tr{"
            r"        \td{\glue[width=3.7cm]}"
            r"        \td{\glue[width=3.7cm]}"
            r"        \td{\glue[width=3.7cm]}"
            r"    }"
            r"    "
            r"    % Insert the actual data"
            r"    \tr{"
            r"        \td{A\glue[width=3.7cm]}"
            r"        \td{A\glue[width=3.7cm]}"
            r"        \td{A\glue[width=3.7cm]}"
            r"        \td{A\glue[width=3.7cm]}"
            r"    }"
            r"}"
            r"\end{center}"
        )
        self.assertTrue(converted_table, converted_table_ok)


class ContentToDocumentTest(unittest.TestCase):
    def setUp(self):
        self.c = kepathian_converters.ContentToDocument()
        self.path = "test.pdf"
        self.silepath = "test.pdf.sile"

    def tearDown(self):
        def rm(path):
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

        rm(self.path)
        rm(self.silepath)

    def test_convert(self):
        text = self.c.convert("hello world", self.path, cleanup=False)
        self.assertTrue(os.path.exists(self.path))
        self.assertTrue(os.path.exists(self.silepath))
        self.assertTrue(text)
        self.assertTrue("hello world" in text)
        self.assertEqual(text.split()[-1], r"\end{document}")

    def test_convert_table(self):
        content = kepathian_converters.KTableToSileStr().convert(simple_ktable())
        text = self.c.convert(content, self.path, cleanup=False)
        self.assertTrue(text)


def simple_ktable(cell_count: int = 4):
    cell = seq([s(1).set("value", "A")])
    return sim([seq([cell for _ in range(cell_count)])])
