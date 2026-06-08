"""
Slide 5 — Variance: How Spread Out is the Data?
"""
from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ────────────────────────────────────────────────────────────
    title = make_title("Variance: How Spread Out is the Data?")
    slide.play(FadeIn(title), run_time=0.6)

    # ── Formula ──────────────────────────────────────────────────────────
    formula = MathTex(
        r"\mathrm{Var}(X)=\frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})^2",
        font_size=38, color=NAVY,
    )
    formula.next_to(title, DOWN, buff=0.45)
    slide.play(Write(formula), run_time=1.0)

    # ── Number lines ─────────────────────────────────────────────────────
    line_length = 8.0
    line_y_top = 0.6
    line_y_bot = -1.3
    line_left = -line_length / 2

    # --- Small variance (top) ---
    top_line = Line(
        start=LEFT * line_length / 2, end=RIGHT * line_length / 2,
        color=GRAY_TEXT, stroke_width=2,
    ).shift(UP * line_y_top)

    # Ticks on top line
    top_ticks = VGroup()
    for t in np.linspace(-line_length / 2, line_length / 2, 11):
        tick = Line(UP * 0.08, DOWN * 0.08, color=GRAY_TEXT, stroke_width=1.5)
        tick.move_to(top_line.get_start() + RIGHT * (t + line_length / 2))
        top_ticks.add(tick)

    # Small variance points (clustered around mean=0)
    small_var_vals = [-0.6, -0.3, -0.1, 0.15, 0.35, 0.55]
    mean_small = np.mean(small_var_vals)
    top_points = VGroup()
    for v in small_var_vals:
        pos = top_line.get_center() + RIGHT * v * (line_length / 8)
        dot = Dot(pos, radius=0.08, color=BLUE_C)
        top_points.add(dot)

    # Mean dot (top)
    mean_top_pos = top_line.get_center() + RIGHT * mean_small * (line_length / 8)
    mean_top_dot = Dot(mean_top_pos, radius=0.10, color=TEAL)
    mean_top_label = MathTex(r"\bar{x}", font_size=24, color=TEAL)
    mean_top_label.next_to(mean_top_dot, UP, buff=0.15)

    top_label = Text("Small variance", font_size=22, color=GREEN_C)
    top_label.next_to(top_line, LEFT, buff=0.3)

    # Dashed distance lines (top) — from two points to mean
    dash_top_lines = VGroup()
    for idx in [0, 5]:  # first and last point
        dline = DashedLine(
            top_points[idx].get_center(), mean_top_dot.get_center(),
            color=TEAL, stroke_width=1.5, dash_length=0.08,
        )
        dash_top_lines.add(dline)

    # --- Large variance (bottom) ---
    bot_line = Line(
        start=LEFT * line_length / 2, end=RIGHT * line_length / 2,
        color=GRAY_TEXT, stroke_width=2,
    ).shift(DOWN * abs(line_y_bot))

    # Ticks on bottom line
    bot_ticks = VGroup()
    for t in np.linspace(-line_length / 2, line_length / 2, 11):
        tick = Line(UP * 0.08, DOWN * 0.08, color=GRAY_TEXT, stroke_width=1.5)
        tick.move_to(bot_line.get_start() + RIGHT * (t + line_length / 2))
        bot_ticks.add(tick)

    # Large variance points (spread out)
    large_var_vals = [-2.8, -1.6, -0.4, 0.9, 2.0, 3.1]
    mean_large = np.mean(large_var_vals)
    bot_points = VGroup()
    for v in large_var_vals:
        pos = bot_line.get_center() + RIGHT * v * (line_length / 8)
        dot = Dot(pos, radius=0.08, color=BLUE_C)
        bot_points.add(dot)

    # Mean dot (bottom)
    mean_bot_pos = bot_line.get_center() + RIGHT * mean_large * (line_length / 8)
    mean_bot_dot = Dot(mean_bot_pos, radius=0.10, color=TEAL)
    mean_bot_label = MathTex(r"\bar{x}", font_size=24, color=TEAL)
    mean_bot_label.next_to(mean_bot_dot, UP, buff=0.15)

    bot_label = Text("Large variance", font_size=22, color=ORANGE_C)
    bot_label.next_to(bot_line, LEFT, buff=0.3)

    # Dashed distance lines (bottom) — from two points to mean
    dash_bot_lines = VGroup()
    for idx in [0, 5]:
        dline = DashedLine(
            bot_points[idx].get_center(), mean_bot_dot.get_center(),
            color=ORANGE_C, stroke_width=1.5, dash_length=0.08,
        )
        dash_bot_lines.add(dline)

    # Animate number lines
    slide.play(
        Create(top_line), Create(top_ticks),
        Create(bot_line), Create(bot_ticks),
        FadeIn(top_label), FadeIn(bot_label),
        run_time=0.8,
    )
    slide.play(
        FadeIn(top_points, lag_ratio=0.15),
        FadeIn(bot_points, lag_ratio=0.15),
        FadeIn(mean_top_dot), FadeIn(mean_top_label),
        FadeIn(mean_bot_dot), FadeIn(mean_bot_label),
        run_time=0.8,
    )
    slide.play(
        Create(dash_top_lines, lag_ratio=0.3),
        Create(dash_bot_lines, lag_ratio=0.3),
        run_time=0.7,
    )

    # ── Bullet list ──────────────────────────────────────────────────────
    bullets = make_bullet_list([
        "Small variance → points close together",
        "Large variance → points spread out",
        "PCA prefers large variance directions",
    ], font_size=24)
    bullets.to_edge(DOWN, buff=0.45)
    slide.play(FadeIn(bullets, shift=UP * 0.3), run_time=0.7)

    slide.next_slide()
