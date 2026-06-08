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

    # ====================================================================
    # LEFT HALF — 2D scatter with projections
    # ====================================================================
    axes_group = make_light_axes(
        x_range=[-4, 4, 1], y_range=[-4, 4, 1],
        x_length=5, y_length=4.5,
        x_label="x₁", y_label="x₂",
    )
    axes = axes_group[0]
    axes_group.shift(LEFT * 3.5 + DOWN * 0.6)

    # Normal data along diagonal (~30°)
    angle_deg = 35
    angle_rad = np.radians(angle_deg)
    normal_points = generate_correlated_data(n=20, angle_deg=angle_deg, spread=0.3, seed=55)
    normal_dots = make_scatter_points(axes, normal_points, color=BLUE_C, radius=0.055)

    # Anomaly point far from the diagonal
    anomaly_pt = (1.0, -2.8)
    anomaly_dot = Dot(axes.c2p(*anomaly_pt), radius=0.09, color=RED_C)

    # PC₁ arrow along the diagonal
    pc_len = 3.5
    pc_start = (-pc_len * np.cos(angle_rad), -pc_len * np.sin(angle_rad))
    pc_end = (pc_len * np.cos(angle_rad), pc_len * np.sin(angle_rad))
    pc_arrow = make_principal_arrow(axes, pc_start, pc_end, color=ORANGE_C, stroke_width=3)
    pc_label = Text("PC₁", font_size=18, color=ORANGE_C)
    pc_label.next_to(axes.c2p(*pc_end), UR, buff=0.1)

    # Projection of a normal point (pick one near center)
    norm_pt = normal_points[5]
    norm_proj = _project_point(norm_pt[0], norm_pt[1], angle_rad)
    normal_proj_line = DashedLine(
        axes.c2p(*norm_pt), axes.c2p(*norm_proj),
        color=GREEN_C, stroke_width=2, dash_length=0.08,
    )
    small_err_label = Text("Small error", font_size=14, color=GREEN_C)
    mid_x = (norm_pt[0] + norm_proj[0]) / 2
    mid_y = (norm_pt[1] + norm_proj[1]) / 2
    small_err_label.next_to(axes.c2p(mid_x, mid_y), RIGHT, buff=0.15)

    # Projection of the anomaly
    anom_proj = _project_point(anomaly_pt[0], anomaly_pt[1], angle_rad)
    anomaly_proj_line = DashedLine(
        axes.c2p(*anomaly_pt), axes.c2p(*anom_proj),
        color=RED_C, stroke_width=2, dash_length=0.08,
    )
    large_err_label = Text("Large error", font_size=14, color=RED_C)
    mid_ax = (anomaly_pt[0] + anom_proj[0]) / 2
    mid_ay = (anomaly_pt[1] + anom_proj[1]) / 2
    large_err_label.next_to(axes.c2p(mid_ax, mid_ay), RIGHT, buff=0.15)

    # Projection dots
    norm_proj_dot = Dot(axes.c2p(*norm_proj), radius=0.05, color=GREEN_C)
    anom_proj_dot = Dot(axes.c2p(*anom_proj), radius=0.05, color=RED_C)

    # ====================================================================
    # RIGHT HALF — Image comparison
    # ====================================================================
    right_x = 3.2

    # Normal image — smooth gradient pattern (8x8)
    rng = np.random.default_rng(42)
    normal_matrix = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            normal_matrix[i, j] = 0.1 + 0.1 * (i + j) / 14.0
    normal_grid = make_image_grid(normal_matrix, cell_size=0.22)

    # Reconstructed normal — very similar
    recon_normal_matrix = normal_matrix + rng.normal(0, 0.02, (8, 8))
    recon_normal_matrix = np.clip(recon_normal_matrix, 0, 1)
    recon_normal_grid = make_image_grid(recon_normal_matrix, cell_size=0.22)

    # Anomaly image — noisy
    anomaly_matrix = rng.uniform(0.1, 0.9, (8, 8))
    anomaly_grid = make_image_grid(anomaly_matrix, cell_size=0.22)

    # Reconstructed anomaly — blurry/averaged (poorly reconstructed)
    recon_anomaly_matrix = np.full((8, 8), anomaly_matrix.mean())
    recon_anomaly_matrix += rng.normal(0, 0.05, (8, 8))
    recon_anomaly_matrix = np.clip(recon_anomaly_matrix, 0, 1)
    recon_anomaly_grid = make_image_grid(recon_anomaly_matrix, cell_size=0.22)

    # Layout — top row: Normal
    normal_title = Text("Normal", font_size=18, color=BLUE_C, weight=BOLD)
    normal_grid.move_to(RIGHT * (right_x - 1.3) + UP * 0.4)
    arrow_n = Arrow(
        normal_grid.get_right(), normal_grid.get_right() + RIGHT * 0.8,
        color=GRAY_TEXT, stroke_width=2, buff=0.1,
        max_tip_length_to_length_ratio=0.3,
    )
    recon_normal_grid.next_to(arrow_n, RIGHT, buff=0.15)
    error_n = Text("Error: 0.08", font_size=16, color=GREEN_C)
    error_n.next_to(recon_normal_grid, RIGHT, buff=0.25)
    normal_title.next_to(normal_grid, LEFT, buff=0.3)

    normal_row = VGroup(normal_title, normal_grid, arrow_n, recon_normal_grid, error_n)

    # Layout — bottom row: Anomaly
    anomaly_title = Text("Anomaly", font_size=18, color=RED_C, weight=BOLD)
    anomaly_grid.move_to(RIGHT * (right_x - 1.3) + DOWN * 1.5)
    arrow_a = Arrow(
        anomaly_grid.get_right(), anomaly_grid.get_right() + RIGHT * 0.8,
        color=GRAY_TEXT, stroke_width=2, buff=0.1,
        max_tip_length_to_length_ratio=0.3,
    )
    recon_anomaly_grid.next_to(arrow_a, RIGHT, buff=0.15)
    error_a = Text("Error: 1.45", font_size=16, color=RED_C)
    error_a.next_to(recon_anomaly_grid, RIGHT, buff=0.25)
    anomaly_title.next_to(anomaly_grid, LEFT, buff=0.3)

    anomaly_row = VGroup(anomaly_title, anomaly_grid, arrow_a, recon_anomaly_grid, error_a)

    # Divider label
    img_section_label = Text("Image Reconstruction", font_size=18, color=NAVY, weight=BOLD)
    img_section_label.move_to(RIGHT * right_x + UP * 1.6)

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

    # Separator
    slide.play(Create(separator), run_time=0.4)

    # Right side: image comparison
    slide.play(FadeIn(img_section_label), run_time=0.4)

    slide.play(
        FadeIn(normal_title),
        FadeIn(normal_grid),
        run_time=0.6,
    )
    slide.play(GrowArrow(arrow_n), run_time=0.3)
    slide.play(FadeIn(recon_normal_grid), FadeIn(error_n), run_time=0.5)

    slide.play(
        FadeIn(anomaly_title),
        FadeIn(anomaly_grid),
        run_time=0.6,
    )
    slide.play(GrowArrow(arrow_a), run_time=0.3)
    slide.play(FadeIn(recon_anomaly_grid), FadeIn(error_a), run_time=0.5)

    slide.next_slide()
