from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def _project_point(px, py, angle_rad):
    """Project point (px, py) onto the line through origin at angle_rad."""
    dx, dy = np.cos(angle_rad), np.sin(angle_rad)
    t = px * dx + py * dy
    return t * dx, t * dy


def build(slide):
    clear_slide(slide)

    # ── Title ────────────────────────────────────────────────────────────
    title = make_title("Complete Example: PCA to Anomaly Detection")
    slide.play(FadeIn(title), run_time=0.6)

    # ====================================================================
    # LEFT HALF — 2D scatter with projections & Error Distribution
    # ====================================================================
    axes_group = make_light_axes(
        x_range=[-4, 4, 1], y_range=[-4, 4, 1],
        x_length=4.0, y_length=2.8,
        x_label="x₁", y_label="x₂",
    )
    axes = axes_group[0]
    axes_group.shift(LEFT * 3.6 + UP * 0.7)

    # Normal data along diagonal (~35°)
    angle_deg = 35
    angle_rad = np.radians(angle_deg)
    normal_points = generate_correlated_data(n=20, angle_deg=angle_deg, spread=0.3, seed=55)
    normal_dots = make_scatter_points(axes, normal_points, color=BLUE_C, radius=0.05)

    # Anomaly point far from the diagonal
    anomaly_pt = (1.0, -2.8)
    anomaly_dot = Dot(axes.c2p(*anomaly_pt), radius=0.08, color=RED_C)

    # PC₁ arrow along the diagonal
    pc_len = 3.5
    pc_start = (-pc_len * np.cos(angle_rad), -pc_len * np.sin(angle_rad))
    pc_end = (pc_len * np.cos(angle_rad), pc_len * np.sin(angle_rad))
    pc_arrow = make_principal_arrow(axes, pc_start, pc_end, color=ORANGE_C, stroke_width=3)
    pc_label = Text("PC₁", font_size=16, color=ORANGE_C)
    pc_label.next_to(axes.c2p(*pc_end), UR, buff=0.1)

    # Projection of a normal point (pick one near center)
    norm_pt = normal_points[5]
    norm_proj = _project_point(norm_pt[0], norm_pt[1], angle_rad)
    normal_proj_line = DashedLine(
        axes.c2p(*norm_pt), axes.c2p(*norm_proj),
        color=GREEN_C, stroke_width=1.5, dash_length=0.08,
    )
    small_err_label = Text("Small error", font_size=12, color=GREEN_C)
    mid_x = (norm_pt[0] + norm_proj[0]) / 2
    mid_y = (norm_pt[1] + norm_proj[1]) / 2
    small_err_label.next_to(axes.c2p(mid_x, mid_y), RIGHT, buff=0.1)

    # Projection of the anomaly
    anom_proj = _project_point(anomaly_pt[0], anomaly_pt[1], angle_rad)
    anomaly_proj_line = DashedLine(
        axes.c2p(*anomaly_pt), axes.c2p(*anom_proj),
        color=RED_C, stroke_width=1.5, dash_length=0.08,
    )
    large_err_label = Text("Large error", font_size=12, color=RED_C)
    mid_ax = (anomaly_pt[0] + anom_proj[0]) / 2
    mid_ay = (anomaly_pt[1] + anom_proj[1]) / 2
    large_err_label.next_to(axes.c2p(mid_ax, mid_ay), RIGHT, buff=0.1)

    # Projection dots
    norm_proj_dot = Dot(axes.c2p(*norm_proj), radius=0.05, color=GREEN_C)
    anom_proj_dot = Dot(axes.c2p(*anom_proj), radius=0.05, color=RED_C)

    # --- Gaussian Error Distribution Curve ---
    error_axes = Axes(
        x_range=[0, 2.0, 0.5],
        y_range=[0, 4.0, 1.0],
        x_length=4.0,
        y_length=1.4,
        axis_config={
            "color": GRAY_TEXT,
            "stroke_width": 1.5,
            "include_tip": True,
            "include_ticks": False,
        }
    )
    error_axes.move_to(LEFT * 3.6 + DOWN * 2.1)

    err_x_lbl = Text("e", font_size=12, color=GRAY_TEXT).next_to(error_axes.x_axis.get_end(), DR, buff=0.05)
    err_y_lbl = Text("p(e)", font_size=12, color=GRAY_TEXT).next_to(error_axes.y_axis.get_end(), UP, buff=0.05)
    err_axes_labels = VGroup(err_x_lbl, err_y_lbl)

    def error_pdf(x):
        mu = 0.15
        sigma = 0.12
        return (1.0 / (sigma * np.sqrt(2.0 * np.pi))) * np.exp(-((x - mu) ** 2) / (2.0 * sigma ** 2))

    err_curve = error_axes.plot(error_pdf, x_range=[0, 1.8], color=NAVY, stroke_width=2.5)

    norm_err_val = 0.08
    norm_err_dot = Dot(error_axes.c2p(norm_err_val, error_pdf(norm_err_val)), radius=0.06, color=BLUE_C)
    norm_err_lbl = MathTex(r"e_N", font_size=14, color=BLUE_C).next_to(norm_err_dot, UP, buff=0.05)

    anom_err_val = 1.45
    anom_err_dot = Dot(error_axes.c2p(anom_err_val, error_pdf(anom_err_val)), radius=0.06, color=RED_C)
    anom_err_lbl = MathTex(r"e_A", font_size=14, color=RED_C).next_to(anom_err_dot, UP, buff=0.05)

    tau_line = DashedLine(
        error_axes.c2p(0.5, 0), error_axes.c2p(0.5, 3.5),
        color=RED_C, stroke_width=1.5, dash_length=0.06
    )
    tau_lbl = MathTex(r"\tau = 0.5", font_size=14, color=RED_C)
    tau_lbl.next_to(tau_line.get_top(), UP, buff=0.05)

    err_title = VGroup(
        Text("Fit Gaussian on", font_size=13, color=NAVY, weight=BOLD, font="Arial"),
        Text("PCA", font_size=13, color=TEAL, weight=BOLD, font="Arial"),
        Text("error:", font_size=13, color=TEAL, weight=BOLD, font="Arial"),
        Text("e ~ N(μ, σ²)", font_size=13, color=NAVY, weight=BOLD, font="Arial"),
    ).arrange(RIGHT, buff=0.08)
    err_title.next_to(error_axes, UP, buff=0.22)

    # ====================================================================
    # RIGHT HALF — Gaussian detector on PCA reconstruction error
    # ====================================================================
    right_x = 3.55

    detector_title = VGroup(
        Text("Gaussian detector uses", font_size=17, color=NAVY, weight=BOLD, font="Arial"),
        Text("PCA", font_size=17, color=TEAL, weight=BOLD, font="Arial"),
        Text("error", font_size=17, color=TEAL, weight=BOLD, font="Arial"),
    ).arrange(RIGHT, buff=0.10)
    detector_title.move_to(RIGHT * right_x + UP * 2.15)

    pca_step = VGroup(
        RoundedRectangle(width=2.4, height=0.55, corner_radius=0.08, stroke_color=TEAL, stroke_width=2, fill_color=WHITE, fill_opacity=0.9),
        Text("PCA reconstruction", font_size=15, color=NAVY),
    )
    pca_step[1].move_to(pca_step[0].get_center())

    error_step = VGroup(
        RoundedRectangle(width=2.4, height=0.55, corner_radius=0.08, stroke_color=ORANGE_C, stroke_width=2, fill_color=WHITE, fill_opacity=0.9),
        MathTex(r"e=\|x-\hat{x}\|^2", font_size=24, color=ORANGE_C),
    )
    error_step[1].move_to(error_step[0].get_center())

    gaussian_step = VGroup(
        RoundedRectangle(width=2.4, height=0.55, corner_radius=0.08, stroke_color=BLUE_C, stroke_width=2, fill_color=WHITE, fill_opacity=0.9),
        MathTex(r"e_{\text{normal}}\sim\mathcal{N}(\mu,\sigma^2)", font_size=20, color=BLUE_C),
    )
    gaussian_step[1].move_to(gaussian_step[0].get_center())

    rule_step = VGroup(
        RoundedRectangle(width=2.4, height=0.55, corner_radius=0.08, stroke_color=RED_C, stroke_width=2, fill_color=WHITE, fill_opacity=0.9),
        MathTex(r"p(e)<\epsilon \Rightarrow \text{anomaly}", font_size=19, color=RED_C),
    )
    rule_step[1].move_to(rule_step[0].get_center())

    detector_steps = VGroup(pca_step, error_step, gaussian_step, rule_step).arrange(DOWN, buff=0.22)
    detector_steps.move_to(RIGHT * right_x + UP * 0.30)

    detector_arrows = VGroup()
    for i in range(len(detector_steps) - 1):
        detector_arrows.add(Arrow(
            detector_steps[i].get_bottom(),
            detector_steps[i + 1].get_top(),
            color=GRAY_TEXT,
            stroke_width=2,
            buff=0.06,
            max_tip_length_to_length_ratio=0.25,
        ))

    normal_decision = VGroup(
        Text("Normal sample", font_size=15, color=BLUE_C, weight=BOLD),
        MathTex(r"e_N=0.08", font_size=20, color=BLUE_C),
        MathTex(r"p(e_N)\ \text{high}", font_size=18, color=GREEN_C),
        Text("keep", font_size=15, color=GREEN_C, weight=BOLD),
    ).arrange(DOWN, buff=0.06)
    normal_box = RoundedRectangle(
        width=2.15, height=1.25, corner_radius=0.08,
        stroke_color=GREEN_C, stroke_width=2,
        fill_color=WHITE, fill_opacity=0.9,
    )
    normal_card = VGroup(normal_box, normal_decision)
    normal_decision.move_to(normal_box.get_center())

    anomaly_decision = VGroup(
        Text("Anomaly sample", font_size=15, color=RED_C, weight=BOLD),
        MathTex(r"e_A=1.45", font_size=20, color=RED_C),
        MathTex(r"p(e_A)\ \text{tiny}", font_size=18, color=RED_C),
        Text("flag", font_size=15, color=RED_C, weight=BOLD),
    ).arrange(DOWN, buff=0.06)
    anomaly_box = RoundedRectangle(
        width=2.15, height=1.25, corner_radius=0.08,
        stroke_color=RED_C, stroke_width=2,
        fill_color=WHITE, fill_opacity=0.9,
    )
    anomaly_card = VGroup(anomaly_box, anomaly_decision)
    anomaly_decision.move_to(anomaly_box.get_center())

    decision_cards = VGroup(normal_card, anomaly_card).arrange(RIGHT, buff=0.35)
    decision_cards.move_to(RIGHT * right_x + DOWN * 1.85)

    decision_arrow = Arrow(
        rule_step.get_bottom(),
        decision_cards.get_top(),
        color=GRAY_TEXT,
        stroke_width=2,
        buff=0.08,
        max_tip_length_to_length_ratio=0.18,
    )

    bridge_arrow = Arrow(
        error_axes.get_right() + RIGHT * 0.15,
        detector_steps.get_left() + LEFT * 0.1,
        color=TEAL,
        stroke_width=3,
        buff=0.05,
        max_tip_length_to_length_ratio=0.12,
    )
    bridge_label = Text("PCA gives e", font_size=14, color=TEAL, weight=BOLD)
    bridge_label.next_to(bridge_arrow, UP, buff=0.08)

    # Vertical separator
    separator = DashedLine(
        UP * 3.2, DOWN * 3.5,
        color=LIGHT_GRAY, stroke_width=1.5, dash_length=0.15,
    ).move_to(RIGHT * 0.3)

    # ── Animations ───────────────────────────────────────────────────────
    slide.play(FadeIn(title), run_time=0.7)

    # Left side: scatter
    slide.play(Create(axes_group), run_time=0.7)
    slide.play(
        LaggedStart(*[FadeIn(d, scale=0.5) for d in normal_dots], lag_ratio=0.04),
        run_time=0.8,
    )
    slide.play(GrowArrow(pc_arrow), FadeIn(pc_label), run_time=0.7)

    # Normal projection
    slide.play(
        Create(normal_proj_line),
        FadeIn(norm_proj_dot),
        run_time=0.6,
    )
    slide.play(FadeIn(small_err_label), run_time=0.4)

    # Anomaly point and projection
    slide.play(FadeIn(anomaly_dot, scale=1.5), run_time=0.5)
    slide.play(
        Flash(anomaly_dot, color=RED_C, flash_radius=0.3, num_lines=8),
        run_time=0.5,
    )
    slide.play(
        Create(anomaly_proj_line),
        FadeIn(anom_proj_dot),
        run_time=0.6,
    )
    slide.play(FadeIn(large_err_label), run_time=0.4)

    # Error Distribution Group
    slide.play(
        Create(error_axes),
        FadeIn(err_axes_labels),
        FadeIn(err_title),
        Create(err_curve),
        run_time=1.0
    )
    slide.play(
        FadeIn(norm_err_dot, scale=1.2),
        FadeIn(norm_err_lbl),
        run_time=0.5
    )
    slide.play(
        Create(tau_line),
        FadeIn(tau_lbl),
        run_time=0.6
    )
    slide.play(
        FadeIn(anom_err_dot, scale=1.2),
        FadeIn(anom_err_lbl),
        run_time=0.5
    )
    slide.play(
        Flash(anom_err_dot, color=RED_C, flash_radius=0.25, num_lines=6),
        run_time=0.5
    )
    slide.wait(0.3)

    # Separator
    slide.play(Create(separator), run_time=0.4)

    # Right side: Gaussian detector fed by PCA error
    slide.play(FadeIn(detector_title), Create(bridge_arrow), FadeIn(bridge_label), run_time=0.6)
    slide.play(FadeIn(pca_step, shift=UP * 0.1), run_time=0.4)
    slide.play(GrowArrow(detector_arrows[0]), FadeIn(error_step, shift=UP * 0.1), run_time=0.5)
    slide.play(GrowArrow(detector_arrows[1]), FadeIn(gaussian_step, shift=UP * 0.1), run_time=0.5)
    slide.play(GrowArrow(detector_arrows[2]), FadeIn(rule_step, shift=UP * 0.1), run_time=0.5)
    slide.play(GrowArrow(decision_arrow), FadeIn(decision_cards, shift=UP * 0.1), run_time=0.8)

    slide.next_slide()
