"""Interactive category trend radar."""

import plotly.graph_objects as go
import streamlit as st

from components.layout import page_heading
from services.demo_data import TREND_RADAR as SAMPLE_RADAR
from services.feeds import topic_momentum
from services.live import get_signals


def render() -> None:
    """Render the radar chart and category strength table."""
    page_heading("MARKET MOMENTUM", "Trend Radar", "Compare signal intensity across the markets you follow.")
    signals, is_live, _ = get_signals()
    TREND_RADAR = topic_momentum(signals) if is_live else SAMPLE_RADAR
    if len(TREND_RADAR) < 3:
        TREND_RADAR = SAMPLE_RADAR
        is_live = False
    st.caption("Live momentum = 50% story volume + 50% average signal score per topic, from today's feeds. Follow more topics in Settings to widen the radar."
               if is_live else "Illustrative sample scores (live feeds unavailable or too few topics followed).")
    categories = list(TREND_RADAR)
    values = list(TREND_RADAR.values())
    figure = go.Figure(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(124, 58, 237, 0.20)",
            line={"color": "#9b7bff", "width": 2},
            marker={"color": "#22d3ee", "size": 7},
            hovertemplate="%{theta}: %{r}/100<extra></extra>",
        )
    )
    figure.update_layout(
        polar={
            "bgcolor": "rgba(0,0,0,0)",
            "radialaxis": {"visible": True, "range": [0, 100], "gridcolor": "rgba(148,163,184,.14)", "color": "#75829a"},
            "angularaxis": {"gridcolor": "rgba(148,163,184,.12)", "linecolor": "rgba(148,163,184,.18)", "color": "#aab5c8"},
        },
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif", "color": "#c9d2e3"},
        showlegend=False,
        margin={"l": 38, "r": 38, "t": 34, "b": 34},
        height=480,
    )
    left, right = st.columns([1.35, 1])
    with left:
        st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})
    with right:
        st.markdown("#### Momentum by sector")
        for topic, score in sorted(TREND_RADAR.items(), key=lambda item: item[1], reverse=True):
            st.markdown(f'<div class="trend-row"><span>{topic}</span><strong>{score}</strong></div>', unsafe_allow_html=True)
            st.progress(score / 100)
