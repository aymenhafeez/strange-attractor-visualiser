from pathlib import Path
from typing import Any

import streamlit as st


def apply_theme() -> None:
    css_path = Path(__file__).with_name("theme.css")
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True
    )


def render_hud_header(container: Any | None = None) -> None:
    target = container or st
    target.markdown(
        """
        <section class="hud-shell">
            <p class="hud-kicker">Chaos / System / Dynamics</p>
            <h1>Strange Attractor Visualiser</h1>
        </section>
        """,
        unsafe_allow_html=True,
    )
