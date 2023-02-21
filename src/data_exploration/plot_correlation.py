import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from src.plotly_plots.heatmap import HeatmapTrace
from src.config.load_conifg import Configurator


class CorrPlot:
    """ Calculate correlation and Plot heatmap. """

    def __init__(self,
                 data: pd.DataFrame,
                 config: Configurator,
                 fig_title: str,
                 colorscale: str = "Magma"):

        corr = self.__calc_correlation(
            dataframe=data,
            config=config
        )
        trace = self.__create_trace(
            corr_df=corr,
            colorscale=colorscale
        )
        layout = self.__create_layout(
            fig_title=fig_title,
            config=config
        )
        self.__create_fig(
            trace=trace,
            layout=layout,
            config=config,
            fig_title=fig_title
        )

    @staticmethod
    def __calc_correlation(dataframe: pd.DataFrame,
                           config: Configurator) -> pd.DataFrame:
        return dataframe.corr(method=config.dataexpl.corrmethod)

    @staticmethod
    def __create_trace(corr_df: pd.DataFrame,
                       colorscale: str) -> go.Trace:
        heatmap_trace = HeatmapTrace(
            data=np.array(corr_df),
            xaxis_vals=corr_df.columns,
            yaxis_vals=corr_df.columns,
            colorscale=colorscale
        )
        return heatmap_trace.trace

    @staticmethod
    def __create_layout(fig_title: str,
                        config: Configurator) -> go.Layout:
        heatmap_layout = go.Layout(
            title=dict(
                font=dict(
                    color=config.plotdefault.title_color,
                    family=config.plotdefault.title_font_style,
                    size=config.plotdefault.title_font_size
                ),
                text=fig_title,
                x=0.5
            )
        )
        return heatmap_layout

    @staticmethod
    def __create_fig(trace: go.Trace,
                     layout: go.Layout,
                     config: Configurator,
                     fig_title: str):
        fig = go.Figure(
            data=trace,
            layout=layout
        )
        fig.write_html(os.path.join(
            *config.dirs2make.figures,
            fig_title + ".html"
        ))
