from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ─────────────────────────────────────────────────────────────
    title = make_title("Projection: Reducing Dimensionality")
    slide.play(FadeIn(title), run_time=0.8)

    # ── Formula & explanation (right side) ────────────────────────────────
    formula = MathTex(r"Z = XW", font_size=44, color=NAVY)
    formula.move_to([4.0, 1.8, 0])

    bullets = VGroup(
        Text("X : original data", font_size=22, color=GRAY_TEXT),
        Text("W : principal components", font_size=22, color=GRAY_TEXT),
        Text("Z : lower-dimensional data", font_size=22, color=GRAY_TEXT),
    )
    bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    bullets.next_to(formula, DOWN, buff=0.4)

    slide.play(Write(formula), run_time=0.8)
    slide.play(FadeIn(bullets, shift=UP * 0.2), run_time=0.6)

    # ── 2D scatter plot (left side) ───────────────────────────────────────
    axes_group = make_light_axes(
        x_range=[-4, 4, 1], y_range=[-3, 3, 1],
        x_length=5.5, y_length=4.0,
        x_label="x₁", y_label="x₂",
    )
    axes_group.move_to([-2.8, -0.6, 0])
    axes = axes_group[0]  # the Axes object

    # Generate correlated data
    data = generate_correlated_data(n=20, angle_deg=30, spread=0.4, seed=42)
    scatter = make_scatter_points(axes, data, color=BLUE_C, radius=0.06)

    slide.play(Create(axes_group), run_time=0.8)
    slide.play(FadeIn(scatter, lag_ratio=0.05), run_time=0.8)
    slide.wait(0.3)

    # ── PC₁ direction line ────────────────────────────────────────────────
    angle_rad = np.radians(30)
    pc_dir = np.array([np.cos(angle_rad), np.sin(angle_rad)])
    pc_start = -3.5 * pc_dir
    pc_end = 3.5 * pc_dir

    pc_line = Line(
        axes.c2p(*pc_start), axes.c2p(*pc_end),
        color=ORANGE_C, stroke_width=3,
    )
    pc_label = Text("PC₁", font_size=20, color=ORANGE_C)
    pc_label.next_to(pc_line.get_end(), UR, buff=0.1)

    pc_arrow = Arrow(
        axes.c2p(0, 0), axes.c2p(*(2.2 * pc_dir)),
        color=ORANGE_C, stroke_width=4, buff=0,
        max_tip_length_to_length_ratio=0.1,
    )

    slide.play(GrowArrow(pc_arrow), run_time=0.6)
    slide.play(Create(pc_line), FadeIn(pc_label), run_time=0.6)
    slide.wait(0.3)

    # ── Projection animation for 5 points ────────────────────────────────
    # Pick 5 evenly spaced points from data
    indices = [0, 4, 8, 12, 16]
    proj_dots = VGroup()
    proj_lines = VGroup()

    for idx in indices:
        px, py = data[idx]
        point_vec = np.array([px, py])
        proj_scalar = np.dot(point_vec, pc_dir)
        proj_point = proj_scalar * pc_dir

        # Dashed line from point to projection
        dash = DashedLine(
            axes.c2p(px, py), axes.c2p(*proj_point),
            color=GRAY_TEXT, stroke_width=1.5, dash_length=0.08,
        )
        # Dot on PC₁ line
        pdot = Dot(axes.c2p(*proj_point), radius=0.07, color=ORANGE_C)

        proj_lines.add(dash)
        proj_dots.add(pdot)

    for dl, pd in zip(proj_lines, proj_dots):
        slide.play(Create(dl), FadeIn(pd), run_time=0.4)

    slide.wait(0.3)

    # ── 1D number line below ──────────────────────────────────────────────
    num_line = NumberLine(
        x_range=[-4, 4, 1],
        length=5.5,
        color=GRAY_TEXT,
        stroke_width=2,
        include_numbers=False,
        include_tip=True,
        tip_length=0.15,
    )
    num_line.move_to([-2.8, -3.2, 0])
    nl_label = Text("PC₁ axis", font_size=18, color=ORANGE_C)
    nl_label.next_to(num_line, RIGHT, buff=0.2)

    slide.play(Create(num_line), FadeIn(nl_label), run_time=0.6)

    # Place projected points on 1D line
    proj_1d_dots = VGroup()
    for idx in indices:
        px, py = data[idx]
        point_vec = np.array([px, py])
        proj_scalar = float(np.dot(point_vec, pc_dir))
        d1 = Dot(num_line.n2p(proj_scalar), radius=0.07, color=ORANGE_C)
        proj_1d_dots.add(d1)

    slide.play(
        LaggedStart(
            *[FadeIn(d, scale=1.5) for d in proj_1d_dots],
            lag_ratio=0.15,
        ),
        run_time=1.0,
    )
    slide.wait(0.5)

    slide.next_slide()
