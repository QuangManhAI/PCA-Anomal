from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ───────────────────────────────────────────────────────────
    title_group = make_title("Eigenvalue Intuition: Matrix → Scalar")
    slide.play(FadeIn(title_group, shift=DOWN * 0.3), run_time=0.6)

    # ── Top Section: Algebraic Equation ─────────────────────────────────
    eq_tex = MathTex(
        r"A \vec{v} =",
        r"\begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}",
        r"\begin{bmatrix} 1 \\ 1.62 \end{bmatrix}",
        r"=",
        r"3.62",
        r"\begin{bmatrix} 1 \\ 1.62 \end{bmatrix}",
        font_size=28, color=NAVY
    )
    eq_tex.move_to(UP * 2.2)
    
    box = SurroundingRectangle(eq_tex, color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=0.06, corner_radius=0.1)
    insight_lbl = Text("Matrix multiplication → just SCALING! This is dimensionality reduction.", font_size=16, color=TEAL, weight=BOLD)
    insight_lbl.next_to(box, DOWN, buff=0.15)
    
    slide.play(Write(eq_tex), run_time=1.0)
    slide.play(Create(box), FadeIn(insight_lbl, shift=UP * 0.1), run_time=0.6)
    slide.wait(0.5)

    # ── Middle Section: Conceptual Cards ───────────────────────────────
    def make_info_card(title_text, desc_text, color):
        rect = RoundedRectangle(
            width=3.6, height=0.85, corner_radius=0.1,
            stroke_color=color, stroke_width=2,
            fill_color=WHITE, fill_opacity=0.95
        )
        t = Text(title_text, font_size=16, color=color, weight=BOLD)
        d = Text(desc_text, font_size=13, color=GRAY_TEXT)
        card_content = VGroup(t, d).arrange(DOWN, buff=0.08)
        card_content.move_to(rect.get_center())
        return VGroup(rect, card_content)

    card1 = make_info_card("Covariance Matrix Σ (A)", "Captures data variance/covariance", NAVY)
    card2 = make_info_card("Eigenvector v⃗", "Direction of maximum variance", TEAL)
    card3 = make_info_card("Eigenvalue λ", "Amount of variance in direction v⃗", ORANGE_C)

    cards = VGroup(card1, card2, card3).arrange(RIGHT, buff=0.4)
    cards.next_to(insight_lbl, DOWN, buff=0.35)

    slide.play(
        LaggedStart(*[FadeIn(card, shift=UP * 0.2) for card in cards], lag_ratio=0.3),
        run_time=1.0
    )
    slide.wait(0.5)

    # ── Bottom Section: Geometric Scaling ──────────────────────────────
    axes_group = make_light_axes(
        x_range=[-1, 5, 1],
        y_range=[-1, 5, 1],
        x_length=4.2,
        y_length=2.2,
        x_label="x₁",
        y_label="x₂"
    )
    axes_group.to_edge(LEFT, buff=1.2)
    axes_group.shift(DOWN * 2.0)
    axes = axes_group[0]

    # Generate correlated data along the eigenvector direction (angle ~ 58 degrees)
    data = generate_correlated_data(n=25, angle_deg=58, spread=0.25, seed=42)
    shifted_data = [(x + 2.0, y + 3.0) for x, y in data]
    dots = make_scatter_points(axes, shifted_data, color=BLUE_C, radius=0.05)

    # Initial eigenvector arrow (v)
    center = np.array([2.0, 3.0])
    v_dir = np.array([np.cos(np.radians(58)), np.sin(np.radians(58))])
    v_len = 0.55
    v_end = center + v_len * v_dir

    v_arrow = Arrow(
        axes.c2p(*center), axes.c2p(*v_end),
        color=ORANGE_C, stroke_width=4, buff=0,
        max_tip_length_to_length_ratio=0.15
    )
    v_label = MathTex(r"\vec{v}", font_size=18, color=ORANGE_C)
    v_label.next_to(v_arrow.get_end(), UR, buff=0.05)

    # Scaled eigenvector arrow (lambda * v)
    scaled_end = center + (3.62 * v_len) * v_dir
    v_scaled_arrow = Arrow(
        axes.c2p(*center), axes.c2p(*scaled_end),
        color=RED_C, stroke_width=5, buff=0,
        max_tip_length_to_length_ratio=0.08
    )
    v_scaled_label = MathTex(r"\lambda\vec{v}\; (\lambda=3.62)", font_size=18, color=RED_C)
    v_scaled_label.next_to(v_scaled_arrow.get_end(), UR, buff=0.08)

    # Explanatory text side
    plot_label = Text("Geometric Interpretation:", font_size=24, color=NAVY, weight=BOLD, font="Arial", disable_ligatures=True)
    plot_desc1 = Text("• Eigenvector v⃗ points along data spread", font_size=19, color=GRAY_TEXT, font="Arial", disable_ligatures=True)
    plot_desc2 = Text("• Matrix multiplication scales v⃗ by λ", font_size=19, color=GRAY_TEXT, font="Arial", disable_ligatures=True)
    plot_desc3 = Text("• Arrow length scales, direction stays constant!", font_size=19, color=TEAL, weight=BOLD, font="Arial", disable_ligatures=True)
    plot_descs = VGroup(plot_label, plot_desc1, plot_desc2, plot_desc3).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    plot_descs.next_to(axes_group, RIGHT, buff=0.95)
    plot_descs.shift(RIGHT * 0.35 + UP * 0.12)

    # Animate bottom section
    slide.play(Create(axes_group), run_time=0.6)
    slide.play(
        LaggedStart(*[FadeIn(dot, scale=0.5) for dot in dots], lag_ratio=0.03),
        run_time=1.0
    )
    slide.play(GrowArrow(v_arrow), FadeIn(v_label), run_time=0.6)
    slide.wait(0.5)

    # Transform eigenvector to scaled version
    slide.play(
        Transform(v_arrow, v_scaled_arrow),
        Transform(v_label, v_scaled_label),
        FadeIn(plot_descs, shift=LEFT * 0.2),
        run_time=1.2
    )
    slide.wait(1.0)

    slide.next_slide()
