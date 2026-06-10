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
    sigma_eq = MathTex(r"\Sigma =", font_size=42, color=NAVY)
    left_bracket = MathTex(r"\left[", font_size=86, color=NAVY)
    right_bracket = MathTex(r"\right]", font_size=86, color=NAVY)

    var_1 = MathTex(r"\mathrm{Var}(x_1)", font_size=36, color=BLUE_C)
    cov_12 = MathTex(r"\mathrm{Cov}(x_1,x_2)", font_size=36, color=ORANGE_C)
    cov_21 = MathTex(r"\mathrm{Cov}(x_2,x_1)", font_size=36, color=ORANGE_C)
    var_2 = MathTex(r"\mathrm{Var}(x_2)", font_size=36, color=BLUE_C)

    cells = VGroup(
        VGroup(var_1, cov_12).arrange(RIGHT, buff=0.54),
        VGroup(cov_21, var_2).arrange(RIGHT, buff=0.54),
    ).arrange(DOWN, buff=0.26)
    matrix_body = VGroup(left_bracket, cells, right_bracket).arrange(RIGHT, buff=0.08)
    matrix_tex = VGroup(sigma_eq, matrix_body).arrange(RIGHT, buff=0.18)
    matrix_tex.move_to(LEFT * 2.45 + DOWN * 0.25)

    slide.play(Write(sigma_eq), FadeIn(left_bracket), FadeIn(right_bracket), run_time=0.6)
    slide.play(LaggedStart(Write(var_1), Write(cov_12), Write(cov_21), Write(var_2), lag_ratio=0.15), run_time=1.0)

    # ── Color-coded labels ───────────────────────────────────────────────
    diag_tag = Text("● Diagonal = Variances", font_size=22, color=BLUE_C)
    offdiag_tag = Text("● Off-diagonal = Covariances", font_size=22, color=ORANGE_C)
    tag_group = VGroup(diag_tag, offdiag_tag).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    tag_group.next_to(matrix_tex, DOWN, buff=0.78)
    tag_group.shift(LEFT * 0.1)
    slide.play(FadeIn(tag_group, shift=UP * 0.2), run_time=0.5)

    # ── Explanation bullets (right side) ─────────────────────────────────
    bullets = make_bullet_list([
        "Diagonal entries → variances",
        "Off-diagonal entries → covariances",
        "Describes the shape of the data",
    ], font_size=25)
    bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.34)
    bullets.move_to(RIGHT * 3.85 + DOWN * 0.18)
    slide.play(FadeIn(bullets, shift=LEFT * 0.3), run_time=0.7)

    slide.next_slide()
