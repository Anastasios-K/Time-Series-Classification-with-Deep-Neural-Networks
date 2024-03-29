import plotly.graph_objects as go


class ScatterTrace:

    def __init__(self,
                 xdata,
                 ydata,
                 name,
                 mode="lines",
                 linecolour="red",
                 linewidth=2,
                 linestyle="solid",  # either of ‘solid’, ‘dot’, ‘dash’, ‘longdash’, ‘dashdot’, ‘longdashdot’
                 ):
        self.trace = go.Scatter(x=xdata,
                                y=ydata,
                                mode=mode,
                                line=dict(
                                    color=linecolour,
                                    width=linewidth,
                                    dash=linestyle
                                ),
                                name=name
                                )
