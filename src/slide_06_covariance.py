"""
Slide 6 — Covariance: How Two Variables Move Together
"""
from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ────────────────────────────────────────────────────────────
    title = make_title("Covariance: How Two Variables Move Together")
    slide.play(FadeIn(title), run_time=0.6)

    # ── Formula ──────────────────────────────────────────────────────────
    formula = MathTex(
        r"\mathrm{Cov}(X,Y)=\frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})",
        font_size=36, color=NAVY,
    )
    formula.next_to(title, DOWN, buff=0.4)
    slide.play(Write(formula), run_time=1.0)

    # ── Three mini scatter plots ─────────────────────────────────────────
    def make_mini_axes():
        """Create small axes for a mini scatter plot."""
        ax = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=3,
            y_length=2.5,
            axis_config={
                "color": GRAY_TEXT,
                "stroke_width": 1.5,
                "include_tip": False,
                "include_ticks": False,
            },
        )
        return ax

    # --- Positive covariance ---
    ax1 = make_mini_axes()
    pts_pos = generate_correlated_data(n=15, angle_deg=30, spread=0.4, seed=10)
    dots_pos = make_scatter_points(ax1, pts_pos, color=BLUE_C, radius=0.05)
    label_pos = Text("Positive", font_size=20, color=GREEN_C)
    label_pos.next_to(ax1, DOWN, buff=0.2)
    plot_pos = VGroup(ax1, dots_pos, label_pos)

    # --- Negative covariance ---
    ax2 = make_mini_axes()
    pts_neg = generate_correlated_data(n=15, angle_deg=-30, spread=0.4, seed=20)
    dots_neg = make_scatter_points(ax2, pts_neg, color=BLUE_C, radius=0.05)
    label_neg = Text("Negative", font_size=20, color=RED_C)
    label_neg.next_to(ax2, DOWN, buff=0.2)
    plot_neg = VGroup(ax2, dots_neg, label_neg)

    # --- Near-zero covariance (circular cloud) ---
    ax3 = make_mini_axes()
    rng = np.random.default_rng(30)
    angles = rng.uniform(0, 2 * np.pi, 15)
    radii = rng.uniform(0.2, 1.5, 15)
    pts_zero = list(zip((radii * np.cos(angles)).tolist(),
                        (radii * np.sin(angles)).tolist()))
    dots_zero = make_scatter_points(ax3, pts_zero, color=BLUE_C, radius=0.05)
    label_zero = Text("Near zero", font_size=20, color=GRAY_TEXT)
    label_zero.next_to(ax3, DOWN, buff=0.2)
    plot_zero = VGroup(ax3, dots_zero, label_zero)

    # Arrange the three plots side by side
    plots = VGroup(plot_pos, plot_neg, plot_zero)
    plots.arrange(RIGHT, buff=0.9)
    plots.move_to(DOWN * 1.0)

    # Animate plots one by one
    slide.play(FadeIn(ax1), FadeIn(dots_pos, lag_ratio=0.1), FadeIn(label_pos), run_time=0.8)
    slide.play(FadeIn(ax2), FadeIn(dots_neg, lag_ratio=0.1), FadeIn(label_neg), run_time=0.8)
    slide.play(FadeIn(ax3), FadeIn(dots_zero, lag_ratio=0.1), FadeIn(label_zero), run_time=0.8)

    slide.next_slide()
