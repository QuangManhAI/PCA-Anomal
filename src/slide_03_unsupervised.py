from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ───────────────────────────────────────────────────────────
    title_group = make_title("Unsupervised Learning: 3D → 2D")
    slide.play(FadeIn(title_group, shift=DOWN * 0.3), run_time=0.6)

    rng = np.random.default_rng(42)

    # Build one coherent dataset: three 2D clusters embedded in a tilted 3D plane.
    cluster_specs = [
        ([-2.2, 0.9], BLUE_C),
        ([0.2, -1.15], GREEN_C),
        ([2.15, 0.55], ORANGE_C),
    ]
    latent_clusters = [
        rng.normal(center, [0.34, 0.24], (18, 2))
        for center, _ in cluster_specs
    ]
    latent = np.vstack(latent_clusters)
    labels = np.concatenate([[i] * len(points) for i, points in enumerate(latent_clusters)])

    pc1_true = np.array([0.82, 0.37, 0.43])
    pc1_true = pc1_true / np.linalg.norm(pc1_true)
    pc2_true = np.array([-0.12, 0.86, -0.49])
    pc2_true = pc2_true - np.dot(pc2_true, pc1_true) * pc1_true
    pc2_true = pc2_true / np.linalg.norm(pc2_true)
    plane_normal = np.cross(pc1_true, pc2_true)
    plane_normal = plane_normal / np.linalg.norm(plane_normal)

    noise = rng.normal(0, 0.12, len(latent))[:, None] * plane_normal
    data_3d = latent[:, [0]] * pc1_true + latent[:, [1]] * pc2_true + noise

    centered = data_3d - data_3d.mean(axis=0)
    _, _, vh = np.linalg.svd(centered, full_matrices=False)
    scores = centered @ vh[:2].T
    display_center = np.array([1.5, 1.35, 1.35])
    display_scale = 1.05 / np.max(np.abs(centered))
    display_data_3d = centered * display_scale + display_center

    def points_for_label(points, label):
        return points[labels == label]

    # ── Left Half: Before PCA (3D space) ────────────────────────────────
    corner_origin = np.array([-1.18, -1.15, 0.0])
    x_axis_vec = np.array([0.88, 0.0, 0.0])
    y_axis_vec = np.array([-0.46, -0.28, 0.0])
    z_axis_vec = np.array([0.0, 0.88, 0.0])

    def corner_point(x, y, z):
        return corner_origin + x * x_axis_vec + y * y_axis_vec + z * z_axis_vec

    p000 = corner_point(0, 0, 0)
    p300 = corner_point(3, 0, 0)
    p030 = corner_point(0, 3, 0)
    p003 = corner_point(0, 0, 3)
    p330 = corner_point(3, 3, 0)
    p303 = corner_point(3, 0, 3)
    p033 = corner_point(0, 3, 3)

    corner_walls = VGroup(
        Polygon(
            p000,
            p300,
            p330,
            p030,
            stroke_color=LIGHT_GRAY,
            stroke_width=1.2,
            fill_color=BLUE_C,
            fill_opacity=0.035,
        ),
        Polygon(
            p000,
            p300,
            p303,
            p003,
            stroke_color=LIGHT_GRAY,
            stroke_width=1.2,
            fill_color=TEAL,
            fill_opacity=0.045,
        ),
        Polygon(
            p000,
            p030,
            p033,
            p003,
            stroke_color=LIGHT_GRAY,
            stroke_width=1.2,
            fill_color=PURPLE_C,
            fill_opacity=0.035,
        ),
    )

    x_axis_3d = Arrow(p000, p300, color=GRAY_TEXT, stroke_width=3.0, buff=0, max_tip_length_to_length_ratio=0.08)
    y_axis_3d = Arrow(p000, p030, color=GRAY_TEXT, stroke_width=3.0, buff=0, max_tip_length_to_length_ratio=0.08)
    z_axis_3d = Arrow(p000, p003, color=GRAY_TEXT, stroke_width=2.2, buff=0, max_tip_length_to_length_ratio=0.08)
    corner_axes = VGroup(x_axis_3d, y_axis_3d, z_axis_3d)
    corner_spine = Dot(p000, radius=0.045, color=NAVY).set_stroke(WHITE, width=1.0, opacity=0.9)

    plane_center = display_center
    plane_scale_u = 2.7 * display_scale
    plane_scale_v = 1.7 * display_scale
    plane_corners = [
        plane_center + sx * plane_scale_u * vh[0] + sy * plane_scale_v * vh[1]
        for sx, sy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    ]
    pca_plane = Polygon(
        *[corner_point(*corner) for corner in plane_corners],
        stroke_color=TEAL,
        stroke_width=2,
        fill_color=TEAL,
        fill_opacity=0.09,
    )
    pca_plane.set_z_index(2)
    plane_label = Text("PCA plane", font_size=14, color=TEAL, weight=BOLD)
    plane_label.add_background_rectangle(color=WHITE, opacity=0.78, buff=0.04)
    plane_label.next_to(pca_plane, UP, buff=0.04)
    plane_label.shift(RIGHT * 0.12)
    plane_label.set_z_index(8)

    def make_depth_dots(points, color):
        dots = VGroup()
        z_min, z_max = display_data_3d[:, 2].min(), display_data_3d[:, 2].max()
        for pt in points:
            depth = (pt[2] - z_min) / max(z_max - z_min, 1e-6)
            dot = Dot(
                corner_point(*pt),
                radius=0.055 + 0.018 * depth,
                color=color,
            )
            dot.set_fill(color, opacity=0.70 + 0.25 * depth)
            dot.set_stroke(WHITE, width=1.0, opacity=0.85)
            dot.set_z_index(5)
            dots.add(dot)
        return dots

    dots_c1 = make_depth_dots(points_for_label(display_data_3d, 0), BLUE_C)
    dots_c2 = make_depth_dots(points_for_label(display_data_3d, 1), GREEN_C)
    dots_c3 = make_depth_dots(points_for_label(display_data_3d, 2), ORANGE_C)
    all_left_dots = VGroup(*dots_c1, *dots_c2, *dots_c3)
    corner_walls.set_z_index(-3)
    z_axis_3d.set_z_index(1)
    VGroup(x_axis_3d, y_axis_3d).set_z_index(6)
    corner_spine.set_z_index(7)

    # Group and position on the left
    left_plot_body = VGroup(corner_walls, z_axis_3d, pca_plane, all_left_dots, x_axis_3d, y_axis_3d, corner_spine, plane_label)
    plot_3d = VGroup(left_plot_body)
    plot_3d.move_to(LEFT * 3.6 + DOWN * 0.2)

    # Add 2D text labels positioned at the wall-corner axis endpoints.
    x_lbl = Text("x", font_size=15, color=GRAY_TEXT).next_to(x_axis_3d.get_end(), RIGHT, buff=0.05)
    y_lbl = Text("y", font_size=15, color=GRAY_TEXT).next_to(y_axis_3d.get_end(), DL, buff=0.04)
    z_lbl = Text("z", font_size=15, color=GRAY_TEXT).next_to(z_axis_3d.get_end(), UP, buff=0.05)
    axes_labels = VGroup(x_lbl, y_lbl, z_lbl)
    axes_labels.set_z_index(8)
    axes_labels.move_to(axes_labels.get_center() + (plot_3d.get_center() - left_plot_body.get_center()))

    lbl_left_title = Text("Before PCA (3D space)", font_size=18, color=NAVY, weight=BOLD)
    lbl_left_title.next_to(plot_3d, UP, buff=0.4)

    lbl_left_status = Text("High-dimensional structure", font_size=18, color=GRAY_TEXT)
    lbl_left_status.next_to(plot_3d, DOWN, buff=0.4)

    # ── Middle PCA Arrow ────────────────────────────────────────────────
    pca_arrow = Arrow(LEFT * 0.75, RIGHT * 0.75, color=TEAL, stroke_width=6, buff=0)
    pca_arrow.move_to(DOWN * 0.2)
    pca_text = Text("PCA", font_size=20, color=TEAL, weight=BOLD)
    pca_text.next_to(pca_arrow, UP, buff=0.1)
    pca_subtext = Text("project", font_size=14, color=GRAY_TEXT)
    pca_subtext.next_to(pca_arrow, DOWN, buff=0.08)

    # ── Right Half: After PCA (2D space) ───────────────────────────────
    x_pad = 0.45
    y_pad = 0.45
    x_min, x_max = scores[:, 0].min() - x_pad, scores[:, 0].max() + x_pad
    y_min, y_max = scores[:, 1].min() - y_pad, scores[:, 1].max() + y_pad
    axes_right_group = make_light_axes(
        x_range=[x_min, x_max, 1],
        y_range=[y_min, y_max, 1],
        x_length=4.15,
        y_length=3.05,
        x_label="PC₁",
        y_label="PC₂"
    )
    axes_right_group.move_to(RIGHT * 3.6 + DOWN * 0.2)
    axes_right = axes_right_group[0]

    lbl_right_title = Text("After PCA (2D projection)", font_size=18, color=NAVY, weight=BOLD)
    lbl_right_title.next_to(axes_right_group, UP, buff=0.25)

    origin_marker = Dot(axes_right.c2p(0, 0), radius=0.025, color=GRAY_TEXT).set_opacity(0.65)
    pc1_line = DashedLine(
        axes_right.c2p(x_min + 0.1, 0),
        axes_right.c2p(x_max - 0.1, 0),
        dash_length=0.12,
        stroke_width=1.5,
        color=LIGHT_GRAY,
    )
    pc2_line = DashedLine(
        axes_right.c2p(0, y_min + 0.1),
        axes_right.c2p(0, y_max - 0.1),
        dash_length=0.12,
        stroke_width=1.5,
        color=LIGHT_GRAY,
    )
    projection_grid = VGroup(pc1_line, pc2_line, origin_marker)

    def make_projection_dots(points, color):
        dots = VGroup()
        for x, y in points:
            dot = Dot(axes_right.c2p(x, y), radius=0.062, color=color)
            dot.set_fill(color, opacity=0.88)
            dot.set_stroke(WHITE, width=1.2, opacity=0.95)
            dots.add(dot)
        return dots

    def make_cluster_ellipse(points, color):
        cov = np.cov(points.T)
        vals, vecs = np.linalg.eigh(cov)
        order = vals.argsort()[::-1]
        vals = vals[order]
        vecs = vecs[:, order]
        mean = points.mean(axis=0)
        unit_x = np.array([1.0, 0.0])
        unit_y = np.array([0.0, 1.0])
        x_unit_len = np.linalg.norm(axes_right.c2p(*(mean + unit_x)) - axes_right.c2p(*mean))
        y_unit_len = np.linalg.norm(axes_right.c2p(*(mean + unit_y)) - axes_right.c2p(*mean))
        ellipse = Ellipse(
            width=2.9 * np.sqrt(vals[0]) * x_unit_len,
            height=2.9 * np.sqrt(vals[1]) * y_unit_len,
            color=color,
            stroke_width=2,
            fill_color=color,
            fill_opacity=0.08,
        )
        angle = np.arctan2(vecs[1, 0] * y_unit_len, vecs[0, 0] * x_unit_len)
        ellipse.rotate(angle)
        ellipse.move_to(axes_right.c2p(*mean))
        return ellipse

    c1_pca = points_for_label(scores, 0)
    c2_pca = points_for_label(scores, 1)
    c3_pca = points_for_label(scores, 2)
    cluster_ellipses = VGroup(
        make_cluster_ellipse(c1_pca, BLUE_C),
        make_cluster_ellipse(c2_pca, GREEN_C),
        make_cluster_ellipse(c3_pca, ORANGE_C),
    )

    dots_c1_pca = make_projection_dots(c1_pca, BLUE_C)
    dots_c2_pca = make_projection_dots(c2_pca, GREEN_C)
    dots_c3_pca = make_projection_dots(c3_pca, ORANGE_C)
    all_right_dots = VGroup(*dots_c1_pca, *dots_c2_pca, *dots_c3_pca)

    lbl_right_status = Text("Same structure, cleaner coordinates", font_size=17, color=GREEN_C)
    lbl_right_status.next_to(axes_right_group, DOWN, buff=0.25)
    dimension_note = VGroup(
        Text("3D coordinates", font_size=15, color=GRAY_TEXT),
        Arrow(LEFT * 0.35, RIGHT * 0.35, color=TEAL, stroke_width=3, buff=0),
        Text("(PC₁, PC₂)", font_size=15, color=TEAL, weight=BOLD),
    ).arrange(RIGHT, buff=0.12)
    dimension_note.next_to(pca_subtext, DOWN, buff=0.12)

    # ── Bullets ───────────────────────────────────────────────────────
    bullets = make_bullet_list([
        "PCA finds the 2D plane that keeps the most variance",
        "Each 3D point is rewritten as two coordinates: PC₁ and PC₂",
    ], font_size=20)
    bullets.to_edge(DOWN, buff=0.4)

    # ── Animations ────────────────────────────────────────────────────
    # 1. Show left side (Before PCA 3D space)
    slide.play(
        Create(corner_axes),
        FadeIn(corner_walls),
        FadeIn(corner_spine),
        FadeIn(pca_plane),
        FadeIn(plane_label, shift=UP * 0.08),
        FadeIn(axes_labels),
        FadeIn(lbl_left_title, shift=DOWN * 0.1),
        run_time=0.8
    )
    slide.play(
        LaggedStart(*[FadeIn(dot, scale=0.5) for dot in all_left_dots], lag_ratio=0.03),
        run_time=1.2
    )
    slide.play(FadeIn(lbl_left_status, shift=UP * 0.15), run_time=0.5)
    slide.wait(0.5)

    # 2. Show middle PCA arrow
    slide.play(
        GrowArrow(pca_arrow),
        FadeIn(pca_text, shift=UP * 0.1),
        FadeIn(pca_subtext, shift=UP * 0.05),
        run_time=0.8,
    )
    slide.play(FadeIn(dimension_note, shift=UP * 0.06), run_time=0.45)
    slide.wait(0.3)

    # 3. Show right side (After PCA 2D space)
    slide.play(
        Create(axes_right_group),
        FadeIn(projection_grid),
        FadeIn(lbl_right_title, shift=DOWN * 0.1),
        run_time=0.8
    )
    slide.play(FadeIn(cluster_ellipses), run_time=0.45)
    slide.play(
        LaggedStart(
            *[
                TransformFromCopy(left_dot, right_dot, path_arc=-25 * DEGREES)
                for left_dot, right_dot in zip(all_left_dots, all_right_dots)
            ],
            lag_ratio=0.018,
        ),
        run_time=1.6
    )
    slide.play(FadeIn(lbl_right_status, shift=UP * 0.15), run_time=0.5)
    slide.wait(0.5)

    # 4. Show bullets
    slide.play(
        LaggedStart(*[Write(b) for b in bullets], lag_ratio=0.4),
        run_time=1.0
    )
    slide.wait(1.0)

    slide.next_slide()
