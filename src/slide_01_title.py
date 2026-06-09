from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    # ── Title and subtitle ──────────────────────────────────────────────
    title = Text(
        "PCA and Anomaly Detection",
        font_size=56,
        color=NAVY,
        weight=BOLD,
    )
    title.to_edge(UP, buff=0.7)

    subtitle = Text(
        "From Variance, Covariance, and Eigenvalues to Detecting Outliers",
        font_size=26,
        color=TEAL,
    )
    subtitle.next_to(title, DOWN, buff=0.35)

    # ── Hero plot: PCA structure + anomaly signal ───────────────────────
    plot_bg = RoundedRectangle(
        width=10.8,
        height=4.8,
        corner_radius=0.16,
        stroke_color=LIGHT_GRAY,
        stroke_width=1.4,
        fill_color=WHITE,
        fill_opacity=0.65,
    )
    plot_bg.next_to(subtitle, DOWN, buff=0.45)

    axes_group = make_light_axes(
        x_range=[-4.2, 4.2, 1],
        y_range=[-3.2, 3.2, 1],
        x_length=6.45,
        y_length=3.65,
        x_label="x₁",
        y_label="x₂",
    )
    axes = axes_group[0]
    axes_group.move_to(plot_bg.get_center() + LEFT * 1.9 + UP * 0.02)

    data = generate_correlated_data(n=34, angle_deg=35, spread=0.34, seed=12)
    dots = make_scatter_points(axes, data, color=BLUE_C, radius=0.055)
    for dot in dots:
        dot.set_fill(BLUE_C, opacity=0.82)
        dot.set_stroke(WHITE, width=1.0, opacity=0.9)

    # ── Translucent ellipse around the data ─────────────────────────────
    angle_rad = np.radians(35)
    ellipse = Ellipse(
        width=5.9,
        height=1.25,
        color=TEAL,
        fill_color=TEAL,
        fill_opacity=0.09,
        stroke_width=2,
    )
    ellipse.rotate(angle_rad)
    ellipse.move_to(axes.c2p(0, 0))

    # ── Principal direction arrow ───────────────────────────────────────
    pc_length = 3.25
    start_pt = np.array([
        -pc_length * np.cos(angle_rad),
        -pc_length * np.sin(angle_rad),
    ])
    end_pt = np.array([
        pc_length * np.cos(angle_rad),
        pc_length * np.sin(angle_rad),
    ])
    pc_arrow = Arrow(
        axes.c2p(start_pt[0], start_pt[1]),
        axes.c2p(end_pt[0], end_pt[1]),
        color=ORANGE_C,
        stroke_width=5,
        buff=0,
        max_tip_length_to_length_ratio=0.06,
    )
    pc_label = VGroup(
        Text("PC1", font_size=19, color=ORANGE_C, weight=BOLD, font="Arial", disable_ligatures=True),
        Text("main structure", font_size=14, color=ORANGE_C, font="Arial", disable_ligatures=True),
    ).arrange(DOWN, buff=0.02, aligned_edge=LEFT)
    pc_label.move_to(axes.c2p(2.35, 1.95))
    pc_label_bg = BackgroundRectangle(pc_label, color=WHITE, fill_opacity=0.82, buff=0.04)

    anomaly_pt = (1.05, -2.55)
    anomaly_dot = Dot(axes.c2p(*anomaly_pt), radius=0.085, color=RED_C)
    anomaly_dot.set_stroke(WHITE, width=1.2, opacity=0.95)
    anomaly_label = Text("anomaly", font_size=16, color=RED_C, weight=BOLD, font="Arial")
    anomaly_label.next_to(anomaly_dot, DR, buff=0.08)

    dx, dy = np.cos(angle_rad), np.sin(angle_rad)

    def project_to_pc(point):
        px, py = point
        t = px * dx + py * dy
        return t * dx, t * dy

    sample_pt = data[9]
    sample_proj = project_to_pc(sample_pt)
    sample_line = DashedLine(
        axes.c2p(*sample_pt),
        axes.c2p(*sample_proj),
        color=GREEN_C,
        stroke_width=1.6,
        dash_length=0.08,
    )
    sample_proj_dot = Dot(axes.c2p(*sample_proj), radius=0.045, color=GREEN_C)

    anomaly_proj = project_to_pc(anomaly_pt)
    anomaly_line = DashedLine(
        axes.c2p(*anomaly_pt),
        axes.c2p(*anomaly_proj),
        color=RED_C,
        stroke_width=1.8,
        dash_length=0.08,
    )
    anomaly_proj_dot = Dot(axes.c2p(*anomaly_proj), radius=0.05, color=RED_C)

    normal_error_tag = Text(
        "small error",
        font_size=13,
        color=GREEN_C,
        font="Arial",
        disable_ligatures=True,
    )
    normal_error_tag.move_to(axes.c2p(-1.75, 1.65))
    normal_tag_line = Line(
        normal_error_tag.get_bottom() + DOWN * 0.03,
        sample_line.get_center(),
        color=GREEN_C,
        stroke_width=1.2,
    )
    anomaly_error_tag = Text(
        "large error",
        font_size=14,
        color=RED_C,
        weight=BOLD,
        font="Arial",
        disable_ligatures=True,
    )
    anomaly_error_tag.next_to(anomaly_dot, LEFT, buff=0.2)

    # ── Error distribution mini panel ───────────────────────────────────
    error_panel = VGroup()
    panel_box = RoundedRectangle(
        width=3.0,
        height=3.5,
        corner_radius=0.12,
        stroke_color=LIGHT_GRAY,
        stroke_width=1.2,
        fill_color=LIGHT_BG,
        fill_opacity=0.9,
    )
    panel_box.move_to(plot_bg.get_center() + RIGHT * 3.65 + UP * 0.05)

    panel_title = VGroup(
        Text("Gaussian on", font_size=17, color=NAVY, weight=BOLD, font="Arial", disable_ligatures=True),
        Text("PCA", font_size=17, color=NAVY, weight=BOLD, font="Arial", disable_ligatures=True),
        Text("error", font_size=17, color=NAVY, weight=BOLD, font="Arial", disable_ligatures=True),
    ).arrange(RIGHT, buff=0.11)
    panel_title.next_to(panel_box.get_top(), DOWN, buff=0.22)

    error_axes = Axes(
        x_range=[0, 1.8, 0.5],
        y_range=[0, 4, 1],
        x_length=2.35,
        y_length=1.35,
        axis_config={
            "color": GRAY_TEXT,
            "stroke_width": 1.4,
            "include_tip": True,
            "include_ticks": False,
        },
    )
    error_axes.move_to(panel_box.get_center() + UP * 0.36)

    def error_pdf(x):
        mu = 0.18
        sigma = 0.13
        return (1.0 / (sigma * np.sqrt(2.0 * np.pi))) * np.exp(-((x - mu) ** 2) / (2.0 * sigma ** 2))

    error_curve = error_axes.plot(error_pdf, x_range=[0, 1.65], color=NAVY, stroke_width=2.5)
    threshold_line = DashedLine(
        error_axes.c2p(0.55, 0),
        error_axes.c2p(0.55, 3.45),
        color=RED_C,
        stroke_width=1.5,
        dash_length=0.06,
    )
    threshold_label = MathTex(r"\tau", font_size=16, color=RED_C)
    threshold_label.next_to(threshold_line.get_top(), UP, buff=0.02)

    normal_err_dot = Dot(error_axes.c2p(0.12, error_pdf(0.12)), radius=0.055, color=BLUE_C)
    anomaly_err_dot = Dot(error_axes.c2p(1.35, error_pdf(1.35)), radius=0.06, color=RED_C)
    anomaly_err_label = Text("flag", font_size=15, color=RED_C, weight=BOLD, font="Arial", disable_ligatures=True)
    anomaly_err_label.next_to(anomaly_err_dot, UR, buff=0.11)

    decision_text = VGroup(
        Text("PCA gives error e", font_size=15, color=TEAL, weight=BOLD, font="Arial", disable_ligatures=True),
        Text("Gaussian threshold flags outliers", font_size=14, color=GRAY_TEXT, font="Arial", disable_ligatures=True),
    ).arrange(DOWN, buff=0.08)
    decision_text.next_to(error_axes, DOWN, buff=0.24)

    error_panel.add(
        panel_box,
        panel_title,
        error_axes,
        error_curve,
        threshold_line,
        threshold_label,
        normal_err_dot,
        anomaly_err_dot,
        anomaly_err_label,
        decision_text,
    )

    # ── Animations ──────────────────────────────────────────────────────
    slide.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.8)
    slide.play(FadeIn(subtitle, shift=DOWN * 0.2), run_time=0.6)
    slide.play(FadeIn(plot_bg), Create(axes_group), run_time=0.7)
    slide.play(Create(ellipse), run_time=0.6)
    slide.play(
        LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.05),
        run_time=1.2,
    )
    slide.play(GrowArrow(pc_arrow), FadeIn(pc_label_bg), FadeIn(pc_label, shift=LEFT * 0.1), run_time=0.8)
    slide.play(Create(sample_line), FadeIn(sample_proj_dot), FadeIn(normal_tag_line), FadeIn(normal_error_tag), run_time=0.55)
    slide.play(FadeIn(anomaly_dot, scale=1.3), FadeIn(anomaly_label), run_time=0.45)
    slide.play(
        Flash(anomaly_dot, color=RED_C, flash_radius=0.35, num_lines=8),
        Create(anomaly_line),
        FadeIn(anomaly_proj_dot),
        FadeIn(anomaly_error_tag),
        run_time=0.8,
    )
    slide.play(FadeIn(error_panel, shift=LEFT * 0.2), run_time=0.9)
    slide.wait(0.5)

    slide.next_slide()
