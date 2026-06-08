from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ────────────────────────────────────────────────────────────
    title = make_title("What is Anomaly Detection?")

    # ── Bullet list (left side) ──────────────────────────────────────────
    bullets = make_bullet_list([
        "An anomaly = significantly different from normal data",
        "Examples:",
    ], font_size=26)

    sub_items = VGroup(
        Text("▸  Fraudulent transaction", font_size=22, color=GRAY_TEXT),
        Text("▸  Sensor failure", font_size=22, color=GRAY_TEXT),
        Text("▸  Corrupted image", font_size=22, color=GRAY_TEXT),
        Text("▸  Unusual route", font_size=22, color=GRAY_TEXT),
    )
    sub_items.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    sub_items.next_to(bullets, DOWN, aligned_edge=LEFT, buff=0.25)
    sub_items.shift(RIGHT * 0.6)

    text_group = VGroup(bullets, sub_items)
    text_group.next_to(title, DOWN, buff=0.5)
    text_group.to_edge(LEFT, buff=0.8)

    # ── Scatter plot (right side) ────────────────────────────────────────
    axes_group = make_light_axes(
        x_range=[-4, 4, 1], y_range=[-4, 4, 1],
        x_length=5, y_length=4.5,
        x_label="", y_label="",
    )
    axes = axes_group[0]  # the Axes object
    axes_group.to_edge(RIGHT, buff=0.8)
    axes_group.shift(DOWN * 0.5)

    # Generate ~25 normal points in a tight cluster
    rng = np.random.default_rng(123)
    normal_xs = rng.normal(0, 0.8, 25)
    normal_ys = rng.normal(0, 0.8, 25)
    normal_points = list(zip(normal_xs.tolist(), normal_ys.tolist()))
    normal_dots = make_scatter_points(axes, normal_points, color=BLUE_C, radius=0.06)

    # 2 red anomaly points far from the cluster
    anomaly_points = [(3.0, 2.5), (-2.8, -2.8)]
    anomaly_dots = make_scatter_points(axes, anomaly_points, color=RED_C, radius=0.09)

    # Dashed warning circles around anomaly points
    warning_circles = VGroup()
    for ax, ay in anomaly_points:
        circle = DashedVMobject(
            Circle(radius=0.4, color=RED_C).move_to(axes.c2p(ax, ay)),
            num_dashes=12,
        )
        circle.set_stroke(opacity=0.5)
        warning_circles.add(circle)

    # Labels for anomaly points
    anom_label_1 = Text("Anomaly", font_size=16, color=RED_C)
    anom_label_1.next_to(axes.c2p(3.0, 2.5), UP, buff=0.35)
    anom_label_2 = Text("Anomaly", font_size=16, color=RED_C)
    anom_label_2.next_to(axes.c2p(-2.8, -2.8), DOWN, buff=0.35)

    normal_label = Text("Normal data", font_size=16, color=BLUE_C)
    normal_label.next_to(axes.c2p(0, 0), DOWN, buff=0.6)

    # ── Animations ───────────────────────────────────────────────────────
    slide.play(FadeIn(title), run_time=0.8)
    slide.play(Write(bullets), run_time=1.0)
    slide.play(
        LaggedStart(*[FadeIn(s, shift=RIGHT * 0.3) for s in sub_items], lag_ratio=0.2),
        run_time=1.0,
    )

    slide.play(Create(axes_group), run_time=0.8)
    slide.play(
        LaggedStart(*[FadeIn(d, scale=0.5) for d in normal_dots], lag_ratio=0.04),
        run_time=1.2,
    )
    slide.play(FadeIn(normal_label), run_time=0.5)

    # Anomaly dots with flash effect
    slide.play(
        FadeIn(anomaly_dots[0], scale=1.5),
        FadeIn(anomaly_dots[1], scale=1.5),
        run_time=0.8,
    )
    slide.play(
        Flash(anomaly_dots[0], color=RED_C, flash_radius=0.4, num_lines=8),
        Flash(anomaly_dots[1], color=RED_C, flash_radius=0.4, num_lines=8),
        run_time=0.6,
    )
    slide.play(
        Create(warning_circles),
        FadeIn(anom_label_1),
        FadeIn(anom_label_2),
        run_time=0.8,
    )

    slide.next_slide()
