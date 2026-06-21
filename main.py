import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from strange_attractor_visualiser.ui.plot_page import render_plot_page

if __name__ == "__main__":
    render_plot_page()
