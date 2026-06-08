from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    # ── Title and subtitle ──────────────────────────────────────────────
    title = Text(
        "PCA and Anomaly Detection",
        font_size=56,
        color=NAVY,
        weight=BOLD,
    )
    title.to_edge(UP, buff=0.7)

    subtitle = Text(
        "From Variance, Covariance, and Eigenvalues to Detecting Outliers",
        font_size=28,
        color=TEAL,
    )
    subtitle.next_to(title, DOWN, buff=0.35)

    # ── Scatter cloud ───────────────────────────────────────────────────
    axes = Axes(
        x_range=[-4, 4, 1],
        y_range=[-3, 3, 1],
        x_length=7,
        y_length=4,
        axis_config={"stroke_opacity": 0},  # invisible axes
    )
    axes.next_to(subtitle, DOWN, buff=0.6)

    data = generate_correlated_data(n=25, angle_deg=35)
    dots = make_scatter_points(axes, data, color=BLUE_C, radius=0.07)

    # ── Translucent ellipse around the data ─────────────────────────────
    angle_rad = np.radians(35)
    ellipse = Ellipse(
        width=6.0,
        height=1.6,
        color=TEAL,
        fill_color=TEAL,
        fill_opacity=0.1,
        stroke_width=2,
    )
    ellipse.rotate(angle_rad)
    ellipse.move_to(axes.c2p(0, 0))

    # ── Principal direction arrow ───────────────────────────────────────
    pc_length = 2.8
    start_pt = np.array([
        -pc_length * np.cos(angle_rad),
        -pc_length * np.sin(angle_rad),
    ])
    end_pt = np.array([
        pc_length * np.cos(angle_rad),
        pc_length * np.sin(angle_rad),
    ])
    pc_arrow = Arrow(
        axes.c2p(start_pt[0], start_pt[1]),
        axes.c2p(end_pt[0], end_pt[1]),
        color=ORANGE_C,
        stroke_width=5,
        buff=0,
        max_tip_length_to_length_ratio=0.06,
    )

    # ── Animations ──────────────────────────────────────────────────────
    slide.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.8)
    slide.play(FadeIn(subtitle, shift=DOWN * 0.2), run_time=0.6)
    slide.play(Create(ellipse), run_time=0.6)
    slide.play(
        LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.05),
        run_time=1.2,
    )
    slide.play(GrowArrow(pc_arrow), run_time=0.8)
    slide.wait(0.5)

    slide.next_slide()
