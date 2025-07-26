# 脳波のプロット
import numpy as np
from typing import Optional
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.models import RangeTool
from bokeh.layouts import column

from scipy.signal import decimate


def eeg_plot(
    data_arr: np.ndarray,
    fs: float,
    ch_names: list,
    highlight_ch: Optional[list] = None,
    highlight_color: "str" = "red",
    downsampling_factor: int = 10,
    win_range=(300, 360),
    y_interval=150,
    fig_size=(1000, 500),
    jupyter=True,
    show_plot=True
):
    def check_ch_arr_length(data_arr, ch_names: list):
        if data_arr.shape[1] != len(ch_names):
            raise ValueError("Length of 'ch_names' and 'data_arr' does not match.")

    check_ch_arr_length(data_arr, ch_names)

    if jupyter:
        output_notebook()

    title_label = "EEG signal"

    p = figure(
        title=title_label, x_axis_label='time', y_axis_label='electrode',
        x_range=win_range, y_range=((len(ch_names)+1)*y_interval, -y_interval*2),
        width=fig_size[0], height=fig_size[1]
        )

    data_arr = decimate(data_arr, downsampling_factor, axis=0)
    times = np.arange(len(data_arr))/(fs/downsampling_factor)

    for i, ch_name in enumerate(ch_names):
        y = data_arr[:, i] + i*y_interval
        if highlight_ch is not None:
            c = highlight_color if ch_name in highlight_ch else "black"
        else:
            c = "black"
        p.line(times, y, line_width=1, line_color=c)

    ticks = [i*y_interval for i in range(len(ch_names))]
    p.yaxis.ticker = ticks
    p.yaxis.major_label_overrides = {
        tick: label for tick, label in zip(ticks, ch_names)
        }
    # p.y_range.flipped = True

    select = figure(title="select range",
                    height=fig_size[1]//5, width=fig_size[0],
                    # y_range=p.y_range, x_axis_type=None, y_axis_type=None,
                    y_range=p.y_range, y_axis_type=None,
                    tools="", toolbar_location=None, background_fill_color="#efefef")

    range_tool = RangeTool(x_range=p.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    for i, ch_name in enumerate(ch_names):
        y = data_arr[:, i] + i*y_interval
        if highlight_ch is not None:
            c = highlight_color if ch_name in highlight_ch else "black"
        else:
            c = "black"
        select.line(times, y, line_width=1, line_color=c)

    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)

    if show_plot:
        show(column(select, p))
