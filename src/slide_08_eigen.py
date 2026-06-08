from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ────────────────────────────────────────────────────────────
    title = make_title("From Covariance to Principal Components")
    slide.play(FadeIn(title), run_time=0.6)

    # ── Left Side: Vertical Journey ──────────────────────────────────────
    step1_lbl = Text("Step 1: Compute variances & covariances", font_size=15, color=NAVY, weight=BOLD)
    step1_math = MathTex(r"\mathrm{Var}(X),\; \mathrm{Cov}(X,Y)", font_size=20, color=GRAY_TEXT)
    step1 = VGroup(step1_lbl, step1_math).arrange(DOWN, buff=0.08)

    arr1 = MathTex(r"\downarrow", font_size=20, color=TEAL)

    step2_lbl = Text("Step 2: Build covariance matrix", font_size=15, color=NAVY, weight=BOLD)
    step2_math = MathTex(
        r"\Sigma = \begin{bmatrix} \mathrm{Var}(x_1) & \mathrm{Cov}(x_1,x_2) \\ \mathrm{Cov}(x_2,x_1) & \mathrm{Var}(x_2) \end{bmatrix}",
        font_size=20, color=GRAY_TEXT
    )
    step2 = VGroup(step2_lbl, step2_math).arrange(DOWN, buff=0.08)

    arr2 = MathTex(r"\downarrow", font_size=20, color=TEAL)

    step3_lbl = Text("Step 3: Eigendecomposition", font_size=15, color=NAVY, weight=BOLD)
    step3_math = MathTex(r"\Sigma\vec{v} = \lambda\vec{v}", font_size=22, color=GRAY_TEXT)
    step3 = VGroup(step3_lbl, step3_math).arrange(DOWN, buff=0.08)

    arr3 = MathTex(r"\downarrow", font_size=20, color=TEAL)

    step4_lbl = Text("Result: Principal Components!", font_size=16, color=TEAL, weight=BOLD)

    left_flow = VGroup(step1, arr1, step2, arr2, step3, arr3, step4_lbl).arrange(DOWN, buff=0.15)
    left_flow.to_edge(LEFT, buff=0.8)
    left_flow.shift(DOWN * 0.4)

    # Animate Left Side
    slide.play(FadeIn(step1), run_time=0.5)
    slide.play(Create(arr1), FadeIn(step2), run_time=0.7)
    slide.play(Create(arr2), FadeIn(step3), run_time=0.7)
    slide.play(Create(arr3), FadeIn(step4_lbl), run_time=0.7)
    slide.wait(0.3)

    # ── Right Side: Scatter Cloud & Covariance Ellipse ──────────────────
    axes = Axes(
        x_range=[-4, 4, 1],
        y_range=[-3, 3, 1],
        x_length=5.0,
        y_length=3.6,
        axis_config={
            "color": GRAY_TEXT,
            "stroke_width": 1.5,
            "include_tip": False,
            "include_ticks": False,
        },
    )
    axes.to_edge(RIGHT, buff=0.8)
    axes.shift(UP * 0.3)

    data = generate_correlated_data(n=30, angle_deg=35, spread=0.4, seed=42)
    scatter = make_scatter_points(axes, data, color=BLUE_C, radius=0.05)

    # Covariance Ellipse
    x_scale = axes.x_axis.get_unit_size()
    y_scale = axes.y_axis.get_unit_size()
    ellipse = Ellipse(
        width=4.6 * x_scale,
        height=1.8 * y_scale,
        color=TEAL,
        fill_color=TEAL,
        fill_opacity=0.08,
        stroke_width=2,
        stroke_opacity=0.4
    )
    ellipse.rotate(np.radians(35))
    ellipse.move_to(axes.c2p(0, 0))

    # PC Arrows
    angle1 = np.radians(35)
    pc1_len = 2.3
    pc1_arrow = Arrow(
        axes.c2p(0, 0), axes.c2p(pc1_len * np.cos(angle1), pc1_len * np.sin(angle1)),
        color=ORANGE_C, stroke_width=5, buff=0,
        max_tip_length_to_length_ratio=0.1
    )
    pc1_label = Text("PC₁ (λ₁ = 3.62)", font_size=14, color=ORANGE_C, weight=BOLD)
    pc1_label.next_to(pc1_arrow.get_end(), UR, buff=0.08)

    angle2 = angle1 + np.pi / 2
    pc2_len = 0.9
    pc2_arrow = Arrow(
        axes.c2p(0, 0), axes.c2p(pc2_len * np.cos(angle2), pc2_len * np.sin(angle2)),
        color=PURPLE_C, stroke_width=4, buff=0,
        max_tip_length_to_length_ratio=0.15
    )
    pc2_label = Text("PC₂ (λ₂ = 0.38)", font_size=14, color=PURPLE_C, weight=BOLD)
    pc2_label.next_to(pc2_arrow.get_end(), UL, buff=0.08)

    # Bottom Right Insight
    insight_text1 = Text("Large λ₁ → PC₁ captures 90% variance (KEEP)", font_size=14, color=GREEN_C, weight=BOLD)
    insight_text2 = Text("Small λ₂ → PC₂ captures 10% variance (DROP)", font_size=14, color=GRAY_TEXT)
    insight_box = VGroup(insight_text1, insight_text2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    insight_box.next_to(axes, DOWN, buff=0.4)
    insight_box.align_to(axes, LEFT)

    # Animate Right Side
    slide.play(FadeIn(axes), run_time=0.4)
    slide.play(
        LaggedStart(*[FadeIn(dot, scale=0.5) for dot in scatter], lag_ratio=0.03),
        run_time=0.8
    )
    slide.play(Create(ellipse), run_time=0.6)
    
    slide.play(GrowArrow(pc1_arrow), FadeIn(pc1_label), run_time=0.6)
    slide.play(GrowArrow(pc2_arrow), FadeIn(pc2_label), run_time=0.6)
    slide.wait(0.3)

    # Highlight PC1
    highlight = pc1_arrow.copy().set_stroke(width=10, opacity=0.4)
    slide.play(FadeIn(highlight), run_time=0.2)
    slide.play(FadeOut(highlight), run_time=0.2)

    slide.play(FadeIn(insight_box, shift=UP * 0.15), run_time=0.6)
    slide.wait(1.0)

    slide.next_slide()
