"""
Slide 7 — Covariance Matrix
"""
from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ────────────────────────────────────────────────────────────
    title = make_title("Covariance Matrix")
    slide.play(FadeIn(title), run_time=0.6)

    # ── Large matrix formula ─────────────────────────────────────────────
    matrix_tex = MathTex(
        r"\Sigma", r"=",
        r"\begin{bmatrix}"
        r" \mathrm{Var}(x_1) & \mathrm{Cov}(x_1,x_2) \\"
        r" \mathrm{Cov}(x_2,x_1) & \mathrm{Var}(x_2)"
        r"\end{bmatrix}",
        font_size=40, color=NAVY,
    )
    matrix_tex.move_to(LEFT * 2.0 + DOWN * 0.3)
    slide.play(Write(matrix_tex), run_time=1.2)

    # ── Highlight boxes ──────────────────────────────────────────────────
    # We'll create colored rectangles to highlight diagonal vs off-diagonal,
    # positioned relative to the bmatrix content.
    bmatrix = matrix_tex[2]  # the bmatrix submobject

    # Diagonal highlight — covers top-left and bottom-right entries
    diag_label_1 = Text("Var(x₁)", font_size=20, color=BLUE_C)
    diag_label_2 = Text("Var(x₂)", font_size=20, color=BLUE_C)

    # We locate entries by approximate position within the bmatrix
    # Top-left entry: Var(x_1), Bottom-right entry: Var(x_2)
    # Off-diag: Cov(x_1,x_2) top-right, Cov(x_2,x_1) bottom-left

    # Use surrounding rectangles on parts of bmatrix
    # Since indexing into bmatrix submobjects can be fragile, we create
    # manually positioned rectangles.
    bm_center = bmatrix.get_center()
    bm_w = bmatrix.get_width()
    bm_h = bmatrix.get_height()

    # Diagonal cells (top-left, bottom-right quadrants of the inner matrix)
    # Approximate offsets: matrix is 2x2
    cell_w = (bm_w - 0.5) / 2  # subtract bracket width estimate
    cell_h = bm_h / 2 - 0.05

    inner_left = bm_center[0] - (bm_w / 2 - 0.25) + cell_w / 2
    inner_right = bm_center[0] + (bm_w / 2 - 0.25) - cell_w / 2
    inner_top = bm_center[1] + cell_h / 2
    inner_bot = bm_center[1] - cell_h / 2

    diag_rect_1 = RoundedRectangle(
        width=cell_w, height=cell_h, corner_radius=0.05,
        stroke_color=BLUE_C, stroke_width=2,
        fill_color=BLUE_C, fill_opacity=0.12,
    ).move_to([inner_left, inner_top, 0])

    diag_rect_2 = RoundedRectangle(
        width=cell_w, height=cell_h, corner_radius=0.05,
        stroke_color=BLUE_C, stroke_width=2,
        fill_color=BLUE_C, fill_opacity=0.12,
    ).move_to([inner_right, inner_bot, 0])

    offdiag_rect_1 = RoundedRectangle(
        width=cell_w, height=cell_h, corner_radius=0.05,
        stroke_color=ORANGE_C, stroke_width=2,
        fill_color=ORANGE_C, fill_opacity=0.12,
    ).move_to([inner_right, inner_top, 0])

    offdiag_rect_2 = RoundedRectangle(
        width=cell_w, height=cell_h, corner_radius=0.05,
        stroke_color=ORANGE_C, stroke_width=2,
        fill_color=ORANGE_C, fill_opacity=0.12,
    ).move_to([inner_left, inner_bot, 0])

    slide.play(
        Create(diag_rect_1), Create(diag_rect_2),
        run_time=0.7,
    )
    slide.play(
        Create(offdiag_rect_1), Create(offdiag_rect_2),
        run_time=0.7,
    )

    # ── Color-coded labels ───────────────────────────────────────────────
    diag_tag = Text("● Diagonal = Variances", font_size=22, color=BLUE_C)
    offdiag_tag = Text("● Off-diagonal = Covariances", font_size=22, color=ORANGE_C)
    tag_group = VGroup(diag_tag, offdiag_tag).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    tag_group.next_to(matrix_tex, DOWN, buff=0.55)
    slide.play(FadeIn(tag_group, shift=UP * 0.2), run_time=0.5)

    # ── Explanation bullets (right side) ─────────────────────────────────
    bullets = make_bullet_list([
        "Diagonal entries → variances",
        "Off-diagonal entries → covariances",
        "Describes the shape of the data",
    ], font_size=24)
    bullets.move_to(RIGHT * 3.5 + DOWN * 0.3)
    slide.play(FadeIn(bullets, shift=LEFT * 0.3), run_time=0.7)

    slide.next_slide()
