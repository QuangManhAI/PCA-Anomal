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
    formula.move_to([4.0, 2.45, 0])

    bullets = VGroup(
        Text("X : original data", font_size=22, color=GRAY_TEXT),
        Text("W : principal components", font_size=22, color=GRAY_TEXT),
        Text("Z : lower-dimensional data", font_size=22, color=GRAY_TEXT),
    )
    bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    bullets.next_to(formula, DOWN, buff=0.24)

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

    # ── PC₁ and PC₂ direction lines ─────────────────────────────────────
    angle_rad = np.radians(30)
    pc1_dir = np.array([np.cos(angle_rad), np.sin(angle_rad)])
    pc2_dir = np.array([-np.sin(angle_rad), np.cos(angle_rad)])

    pc1_line = Line(
        axes.c2p(*(-3.5 * pc1_dir)), axes.c2p(*(3.5 * pc1_dir)),
        color=ORANGE_C, stroke_width=3,
    )
    pc1_label = Text("PC₁", font_size=20, color=ORANGE_C)
    pc1_label.next_to(pc1_line.get_end(), UR, buff=0.1)
    pc1_arrow = Arrow(
        axes.c2p(0, 0), axes.c2p(*(2.2 * pc1_dir)),
        color=ORANGE_C, stroke_width=4, buff=0,
        max_tip_length_to_length_ratio=0.1,
    )

    pc2_line = Line(
        axes.c2p(*(-2.4 * pc2_dir)), axes.c2p(*(2.4 * pc2_dir)),
        color=PURPLE_C, stroke_width=3,
    )
    pc2_label = Text("PC₂", font_size=20, color=PURPLE_C)
    pc2_label.next_to(pc2_line.get_end(), UL, buff=0.1)
    pc2_arrow = Arrow(
        axes.c2p(0, 0), axes.c2p(*(1.35 * pc2_dir)),
        color=PURPLE_C, stroke_width=4, buff=0,
        max_tip_length_to_length_ratio=0.13,
    )

    slide.play(GrowArrow(pc1_arrow), Create(pc1_line), FadeIn(pc1_label), run_time=0.7)
    slide.play(GrowArrow(pc2_arrow), Create(pc2_line), FadeIn(pc2_label), run_time=0.7)
    slide.wait(0.3)

    def make_projection_group(direction, color):
        lines = VGroup()
        dots = VGroup()
        scalars = []
        for px, py in data:
            point_vec = np.array([px, py])
            proj_scalar = float(np.dot(point_vec, direction))
            proj_point = proj_scalar * direction
            scalars.append(proj_scalar)

            dash = DashedLine(
                axes.c2p(px, py), axes.c2p(*proj_point),
                color=color, stroke_width=1.15, dash_length=0.06,
            )
            dash.set_opacity(0.42)
            pdot = Dot(axes.c2p(*proj_point), radius=0.045, color=color)
            pdot.set_stroke(WHITE, width=0.7, opacity=0.85)
            lines.add(dash)
            dots.add(pdot)
        return lines, dots, scalars

    pc1_proj_lines, pc1_proj_dots, pc1_scalars = make_projection_group(pc1_dir, ORANGE_C)
    pc2_proj_lines, pc2_proj_dots, pc2_scalars = make_projection_group(pc2_dir, PURPLE_C)

    pc1_num_line = NumberLine(
        x_range=[-4, 4, 1],
        length=4.3,
        color=ORANGE_C,
        stroke_width=2,
        include_numbers=False,
        include_tip=True,
        tip_length=0.12,
    )
    pc1_num_line.move_to([4.0, -0.45, 0])
    pc1_nl_label = Text("Projection on PC₁", font_size=17, color=ORANGE_C, weight=BOLD)
    pc1_nl_label.next_to(pc1_num_line, UP, buff=0.16)
    pc1_var_label = Text("larger spread → higher variance", font_size=15, color=ORANGE_C)
    pc1_var_label.next_to(pc1_num_line, DOWN, buff=0.12)

    pc2_num_line = NumberLine(
        x_range=[-4, 4, 1],
        length=4.3,
        color=PURPLE_C,
        stroke_width=2,
        include_numbers=False,
        include_tip=True,
        tip_length=0.12,
    )
    pc2_num_line.move_to([4.0, -2.0, 0])
    pc2_nl_label = Text("Projection on PC₂", font_size=17, color=PURPLE_C, weight=BOLD)
    pc2_nl_label.next_to(pc2_num_line, UP, buff=0.16)
    pc2_var_label = Text("smaller spread → lower variance", font_size=15, color=PURPLE_C)
    pc2_var_label.next_to(pc2_num_line, DOWN, buff=0.12)

    pc1_1d_dots = VGroup(*[
        Dot(pc1_num_line.n2p(s), radius=0.045, color=ORANGE_C)
        for s in pc1_scalars
    ])
    pc2_1d_dots = VGroup(*[
        Dot(pc2_num_line.n2p(s), radius=0.045, color=PURPLE_C)
        for s in pc2_scalars
    ])

    variance_compare = MathTex(
        rf"\mathrm{{Var}}(PC_1)\approx {np.var(pc1_scalars):.2f}"
        rf"\;>\;"
        rf"\mathrm{{Var}}(PC_2)\approx {np.var(pc2_scalars):.2f}",
        font_size=24,
        color=NAVY,
    )
    variance_compare.move_to([4.0, -3.05, 0])

    slide.play(
        LaggedStart(*[Create(line) for line in pc1_proj_lines], lag_ratio=0.015),
        LaggedStart(*[FadeIn(dot, scale=1.4) for dot in pc1_proj_dots], lag_ratio=0.015),
        Create(pc1_num_line),
        FadeIn(pc1_nl_label),
        run_time=1.35,
    )
    slide.play(
        LaggedStart(*[FadeIn(d, scale=1.4) for d in pc1_1d_dots], lag_ratio=0.02),
        FadeIn(pc1_var_label, shift=UP * 0.08),
        run_time=0.8,
    )
    slide.wait(0.25)

    slide.play(FadeOut(pc1_proj_lines), FadeOut(pc1_proj_dots), run_time=0.35)
    slide.play(
        LaggedStart(*[Create(line) for line in pc2_proj_lines], lag_ratio=0.015),
        LaggedStart(*[FadeIn(dot, scale=1.4) for dot in pc2_proj_dots], lag_ratio=0.015),
        Create(pc2_num_line),
        FadeIn(pc2_nl_label),
        run_time=1.35,
    )
    slide.play(
        LaggedStart(*[FadeIn(d, scale=1.4) for d in pc2_1d_dots], lag_ratio=0.02),
        FadeIn(pc2_var_label, shift=UP * 0.08),
        FadeIn(variance_compare, shift=UP * 0.08),
        run_time=0.9,
    )
    slide.wait(0.5)

    slide.next_slide()
