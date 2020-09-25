from dataclasses import dataclass

from src.ResultWithData import ResultWithData, get_result_with_error, get_result_with_data
from src.SidesEnum import SidesEnum
from src.configuration import ALLOWED_PAGE_SPLITS


@dataclass
class PrinterOptions:
    num_pages: int
    gray_scale: bool
    wrap_long_edge: SidesEnum
    page_range_start: int
    page_range_end: int
    page_split: int
    landscape: bool

    def as_string(self):
        string = ""
        if self.num_pages > 1:
            string += " -#{0}".format(self.num_pages)

        if self.gray_scale:
            string += " -o 'ColorMode=Gray' -o 'ColorMode=False'"

        if not self.wrap_long_edge == SidesEnum.one_sided:
            string += " -o sides={0}".format(self.wrap_long_edge.value)

        if self.page_range_start >= 0 and self.page_range_end >= 0:
            string += " -o {0}-{1}".format(self.page_range_start, self.page_range_end)

        if self.page_split in ALLOWED_PAGE_SPLITS and self.page_split != 1:
            string += " -o number-up={0}".format(self.page_split)

        if self.landscape:
            string += " -o landscape"

        return string


def get_options(num_pages: int = 0,
                gray_scale: bool = False,
                two_sided: bool = False,
                wrap_short: bool = False,
                page_range_start: int = 0,
                page_range_end: int = 0,
                page_split: int = 1,
                landscape: bool = False) -> ResultWithData[PrinterOptions]:
    wrap_long_edge = SidesEnum.one_sided

    if two_sided:
        wrap_long_edge = SidesEnum.two_sided_short if wrap_short else SidesEnum.two_sided_long

    return get_result_with_data(PrinterOptions(
        num_pages=num_pages,
        gray_scale=gray_scale,
        wrap_long_edge=wrap_long_edge,
        page_range_start=page_range_start,
        page_range_end=page_range_end,
        page_split=page_split,
        landscape=landscape
    ))
