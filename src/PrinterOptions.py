from dataclasses import dataclass

from src.ResultWithData import ResultWithData, get_result_with_error, get_result_with_data
from src.SidesEnum import SidesEnum


@dataclass
class PrinterOptions:
    num_pages: int
    gray_scale: bool
    wrap_long_edge: SidesEnum
    page_range_start: int
    page_range_end: int
    page_split: int

    def as_string(self):
        string = " -o 'sides={0}'".format(self.wrap_long_edge)
        if self.num_pages > 0:
            string += " -#{0}".format(self.num_pages)

        if not self.gray_scale:
            string += " -o 'ColorMode=Gray' -o 'ColorMode=False'"

        if self.page_range_start > 0 and self.page_range_end > 0:
            string += " -o {0}-{1}".format(self.page_range_start, self.page_range_end)

        return string


allowed_page_splits = [2, 4, 6, 9, 16]


def get_options(num_pages: int = 0,
                gray_scale: bool = False,
                wrap_long_edge: SidesEnum = SidesEnum.one_sided,
                page_range_start: int = 0,
                page_range_end: int = 0,
                page_split: int = 1) -> ResultWithData[PrinterOptions]:
    if page_split not in allowed_page_splits:
        return get_result_with_error(
            "page_split must be one of the following: {0}".format(" | ".join(allowed_page_splits)))

    return get_result_with_data(PrinterOptions(
        num_pages=num_pages,
        gray_scale=gray_scale,
        wrap_long_edge=wrap_long_edge,
        page_range_start=page_range_start,
        page_range_end=page_range_end,
        page_split=page_split
    ))
