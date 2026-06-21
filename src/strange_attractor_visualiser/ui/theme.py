import time
from pathlib import Path

import streamlit as st
from streamlit.delta_generator import DeltaGenerator


def apply_theme() -> None:
    css_path = Path(__file__).with_name("theme.css")
    cache_buster = int(time.time() * 1000)
    st.markdown(
        f"<style>/* {cache_buster} */\n{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


def render_hud_header(container: DeltaGenerator | None = None) -> None:
    target = container or st
    target.markdown(
        """
        <section class="hud-shell">
            <p class="hud-kicker">Chaos / System / Dynamics</p>
            <h1>Strange Attractor<br>Visualiser</h1>
        </section>
        """,
        unsafe_allow_html=True,
    )
