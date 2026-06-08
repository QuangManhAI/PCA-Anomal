from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ─────────────────────────────────────────────────────────────
    title = make_title("PCA Algorithm")
    slide.play(FadeIn(title), run_time=0.8)

    # ── Vertical flowchart ────────────────────────────────────────────────
    steps = [
        "Center the data",
        "Compute covariance matrix",
        "Find eigenvalues & eigenvectors",
        "Sort eigenvalues (descending)",
        "Choose top k components",
        "Project data onto new space",
    ]
    flowchart = make_flowchart_vertical(
        steps, box_width=4.5, box_height=0.5, font_size=20
    )
    flowchart.next_to(title, DOWN, buff=0.5)

    boxes = flowchart[0]   # VGroup of boxes
    arrows = flowchart[1]  # VGroup of arrows

    # Animate boxes one-by-one
    slide.play(
        LaggedStart(
            *[FadeIn(box, shift=DOWN * 0.3) for box in boxes],
            lag_ratio=0.25,
        ),
        run_time=3,
    )
    slide.wait(0.3)

    # Animate arrows
    slide.play(
        LaggedStart(
            *[Create(arr) for arr in arrows],
            lag_ratio=0.15,
        ),
        run_time=1.5,
    )
    slide.wait(0.3)

    # Surrounding rectangle highlight
    highlight = SurroundingRectangle(
        flowchart,
        color=TEAL,
        buff=0.25,
        corner_radius=0.15,
        stroke_width=2,
        fill_color=TEAL,
        fill_opacity=0.06,
    )
    slide.play(Create(highlight), run_time=0.8)
    slide.wait(0.5)

    slide.next_slide()
