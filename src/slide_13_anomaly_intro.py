from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ────────────────────────────────────────────────────────────
    title = make_title("Anomaly Detection: The Gaussian Perspective")
    slide.play(FadeIn(title), run_time=0.6)

    # ── Left Side: Math & Concepts ───────────────────────────────────────
    bullets = make_bullet_list([
        "Model normal data with a probability density p(x)",
        "Normal samples lie in high probability density regions",
        "Anomalies lie in the tails (extremely low density)",
    ], font_size=18)
    
    pdf_formula = MathTex(
        r"p(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}",
        font_size=24, color=NAVY
    )
    
    thresh_formula = MathTex(
        r"\text{Anomaly if: } p(x) < \epsilon \iff \int_{\text{extreme}} p(t) dt < \alpha",
        font_size=20, color=RED_C
    )

    left_group = VGroup(bullets, pdf_formula, thresh_formula).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
    left_group.to_edge(LEFT, buff=0.8)
    left_group.shift(DOWN * 0.3)

    # ── Right Side: Gaussian Bell Curve ─────────────────────────────────
    axes_group = make_light_axes(
        x_range=[-4, 4, 1],
        y_range=[0, 0.45, 0.1],
        x_length=5.6,
        y_length=3.8,
        x_label="x",
        y_label="p(x)"
    )
    axes_group.to_edge(RIGHT, buff=0.8)
    axes_group.shift(DOWN * 0.3)
    axes = axes_group[0]

    def gaussian_pdf(x):
        return (1.0 / np.sqrt(2.0 * np.pi)) * np.exp(-x**2 / 2.0)

    curve = axes.plot(gaussian_pdf, x_range=[-4, 4], color=NAVY, stroke_width=3)

    # Shaded areas representing integrals/tail probability
    # Normal region: [-2, 2]
    # Tail regions: [-4, -2] and [2, 4]
    normal_area = axes.get_area(curve, x_range=[-2, 2], color=BLUE_C, opacity=0.15)
    left_tail = axes.get_area(curve, x_range=[-4, -2], color=RED_C, opacity=0.25)
    right_tail = axes.get_area(curve, x_range=[2, 4], color=RED_C, opacity=0.25)

    # Labels for regions
    normal_label = Text("Normal Region\np(x) ≥ ε", font_size=15, color=BLUE_C)
    normal_label.move_to(axes.c2p(0, 0.12))

    tail_label = Text("Anomaly Tail\np(x) < ε", font_size=15, color=RED_C)
    tail_label.move_to(axes.c2p(2.8, 0.18))
    tail_arrow = Arrow(
        start=axes.c2p(2.8, 0.15),
        end=axes.c2p(2.4, 0.02),
        color=RED_C,
        stroke_width=2.5,
        max_tip_length_to_length_ratio=0.15
    )

    # Dots representing samples
    norm_pt = Dot(axes.c2p(0.5, gaussian_pdf(0.5)), radius=0.07, color=BLUE_C)
    norm_pt_lbl = Text("Normal sample", font_size=12, color=BLUE_C).next_to(norm_pt, UP, buff=0.1)

    anom_pt = Dot(axes.c2p(2.5, gaussian_pdf(2.5)), radius=0.07, color=RED_C)
    anom_pt_lbl = Text("Anomaly", font_size=12, color=RED_C).next_to(anom_pt, UR, buff=0.08)

    # ── Animations ──────────────────────────────────────────────────────
    # 1. Title and Left-side text
    slide.play(
        LaggedStart(*[Write(b) for b in bullets], lag_ratio=0.3),
        run_time=1.0
    )
    slide.play(Write(pdf_formula), run_time=0.8)
    slide.play(Write(thresh_formula), run_time=0.8)
    slide.wait(0.3)

    # 2. Right-side Axes & Gaussian Curve
    slide.play(Create(axes_group), run_time=0.6)
    slide.play(Create(curve), run_time=1.0)
    slide.wait(0.3)

    # 3. Shaded Regions & Labels
    slide.play(
        FadeIn(normal_area),
        FadeIn(normal_label),
        run_time=0.6
    )
    slide.play(
        FadeIn(left_tail),
        FadeIn(right_tail),
        FadeIn(tail_label, shift=LEFT * 0.1),
        GrowArrow(tail_arrow),
        run_time=0.8
    )
    slide.wait(0.5)

    # 4. Sample Points with Indicators
    slide.play(
        FadeIn(norm_pt, scale=1.5),
        FadeIn(norm_pt_lbl),
        run_time=0.6
    )
    slide.play(
        FadeIn(anom_pt, scale=1.5),
        FadeIn(anom_pt_lbl),
        run_time=0.6
    )
    slide.play(
        Flash(anom_pt, color=RED_C, flash_radius=0.35, num_lines=8),
        run_time=0.6
    )
    slide.wait(1.0)

    slide.next_slide()
