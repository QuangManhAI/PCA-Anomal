"""
Shared helpers and color constants for the PCA Anomaly Detection lecture.
"""
from manim import *
import numpy as np

# ── Color Constants ──────────────────────────────────────────────────────
LIGHT_BG = "#F8FAFC"
NAVY = "#0F172A"
TEAL = "#0F766E"
BLUE_C = "#2563EB"
GREEN_C = "#16A34A"
ORANGE_C = "#EA580C"
RED_C = "#DC2626"
PURPLE_C = "#7C3AED"
GRAY_TEXT = "#334155"
LIGHT_GRAY = "#CBD5E1"


# ── Helper Functions ─────────────────────────────────────────────────────

def make_title(text, subtitle=None):
    """Create a styled slide title with optional subtitle."""
    title = Text(text, font_size=44, color=NAVY, weight=BOLD)
    title.to_edge(UP, buff=0.5)
    if subtitle:
        sub = Text(subtitle, font_size=28, color=TEAL)
        sub.next_to(title, DOWN, buff=0.3)
        return VGroup(title, sub)
    return VGroup(title)


def make_bullet_list(items, font_size=28, color=GRAY_TEXT, font="Arial"):
    """Create a vertical bullet-point list."""
    bullets = VGroup()
    for item in items:
        dot = Text("•", font_size=font_size, color=TEAL, font=font, disable_ligatures=True)
        txt = Text(item, font_size=font_size, color=color, font=font, disable_ligatures=True)
        txt.next_to(dot, RIGHT, buff=0.2)
        row = VGroup(dot, txt)
        bullets.add(row)
    bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    return bullets


def make_light_axes(x_range, y_range, x_length, y_length, x_label="", y_label=""):
    """Create axes styled for the light theme."""
    axes = Axes(
        x_range=x_range,
        y_range=y_range,
        x_length=x_length,
        y_length=y_length,
        axis_config={
            "color": GRAY_TEXT,
            "stroke_width": 2,
            "include_tip": True,
            "tip_length": 0.15,
            "tip_width": 0.1,
        },
    )
    labels = VGroup()
    if x_label:
        xl = Text(x_label, font_size=22, color=GRAY_TEXT)
        xl.next_to(axes.x_axis, RIGHT, buff=0.15)
        labels.add(xl)
    if y_label:
        yl = Text(y_label, font_size=22, color=GRAY_TEXT)
        yl.next_to(axes.y_axis, UP, buff=0.15)
        labels.add(yl)
    return VGroup(axes, labels)


def make_scatter_points(axes, points, color=BLUE_C, radius=0.06):
    """Create scatter dots from a list of (x, y) tuples."""
    dots = VGroup()
    for x, y in points:
        dot = Dot(axes.c2p(x, y), radius=radius, color=color)
        dots.add(dot)
    return dots


def make_principal_arrow(axes, start, end, color=ORANGE_C, stroke_width=4):
    """Create a principal component arrow on axes."""
    arrow = Arrow(
        axes.c2p(*start), axes.c2p(*end),
        color=color,
        stroke_width=stroke_width,
        buff=0,
        max_tip_length_to_length_ratio=0.08,
    )
    return arrow


def make_flowchart(labels, box_width=2.0, box_height=0.6, font_size=18):
    """Create a horizontal flowchart with boxes and arrows."""
    boxes = VGroup()
    arrows = VGroup()

    for i, label in enumerate(labels):
        rect = RoundedRectangle(
            width=box_width, height=box_height,
            corner_radius=0.1,
            stroke_color=TEAL,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=0.9,
        )
        txt = Text(label, font_size=font_size, color=NAVY)
        txt.move_to(rect.get_center())
        box = VGroup(rect, txt)
        boxes.add(box)

    boxes.arrange(RIGHT, buff=0.4)

    for i in range(len(boxes) - 1):
        arr = Arrow(
            boxes[i].get_right(), boxes[i + 1].get_left(),
            color=GRAY_TEXT, stroke_width=2, buff=0.05,
            max_tip_length_to_length_ratio=0.3,
        )
        arrows.add(arr)

    return VGroup(boxes, arrows)


def make_flowchart_vertical(labels, box_width=4.5, box_height=0.55, font_size=20):
    """Create a vertical flowchart with boxes and arrows."""
    boxes = VGroup()
    arrows = VGroup()

    for label in labels:
        rect = RoundedRectangle(
            width=box_width, height=box_height,
            corner_radius=0.1,
            stroke_color=TEAL,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=0.9,
        )
        txt = Text(label, font_size=font_size, color=NAVY)
        txt.move_to(rect.get_center())
        box = VGroup(rect, txt)
        boxes.add(box)

    boxes.arrange(DOWN, buff=0.35)

    for i in range(len(boxes) - 1):
        arr = Arrow(
            boxes[i].get_bottom(), boxes[i + 1].get_top(),
            color=GRAY_TEXT, stroke_width=2, buff=0.05,
            max_tip_length_to_length_ratio=0.4,
        )
        arrows.add(arr)

    return VGroup(boxes, arrows)


def make_image_grid(matrix, cell_size=0.25, color_map=True):
    """Create a pixel grid from a numpy matrix.
    Values should be in [0, 1] range. 0=white, 1=black for light theme.
    """
    rows, cols = matrix.shape
    grid = VGroup()
    for i in range(rows):
        for j in range(cols):
            val = float(matrix[i, j])
            # Interpolate from white to dark
            gray = int((1 - val) * 255)
            hex_color = f"#{gray:02x}{gray:02x}{gray:02x}"
            cell = Square(
                side_length=cell_size,
                fill_color=hex_color,
                fill_opacity=1.0,
                stroke_width=0.5,
                stroke_color=LIGHT_GRAY,
            )
            cell.move_to([j * cell_size, -i * cell_size, 0])
            grid.add(cell)
    grid.move_to(ORIGIN)
    return grid


def make_error_bar_chart(errors, threshold, bar_width=0.5, bar_spacing=0.3):
    """Create a simple bar chart of reconstruction errors with a threshold line."""
    chart = VGroup()
    bars = VGroup()
    max_err = max(max(errors), threshold) * 1.2

    for i, err in enumerate(errors):
        height = (err / max_err) * 3.0
        color = RED_C if err > threshold else BLUE_C
        bar = Rectangle(
            width=bar_width, height=height,
            fill_color=color, fill_opacity=0.8,
            stroke_color=color, stroke_width=1,
        )
        bar.move_to([i * (bar_width + bar_spacing), height / 2, 0])
        label = Text(f"{err:.2f}", font_size=16, color=GRAY_TEXT)
        label.next_to(bar, UP, buff=0.1)
        bars.add(VGroup(bar, label))

    chart.add(bars)

    # Threshold line
    th_height = (threshold / max_err) * 3.0
    total_width = len(errors) * (bar_width + bar_spacing)
    th_line = DashedLine(
        start=[-bar_width, th_height, 0],
        end=[total_width, th_height, 0],
        color=RED_C, stroke_width=2, dash_length=0.15,
    )
    th_label = MathTex(r"\tau", font_size=28, color=RED_C)
    th_label.next_to(th_line, RIGHT, buff=0.15)
    chart.add(th_line, th_label)

    chart.move_to(ORIGIN)
    return chart


def clear_slide(slide):
    """Fade out all current mobjects on the slide."""
    if slide.mobjects:
        slide.play(FadeOut(*slide.mobjects), run_time=0.5)


def generate_correlated_data(n=30, angle_deg=30, spread=0.3, seed=42):
    """Generate 2D correlated data along a given angle."""
    rng = np.random.default_rng(seed)
    angle = np.radians(angle_deg)
    t = rng.normal(0, 1.5, n)
    noise = rng.normal(0, spread, n)
    x = t * np.cos(angle) - noise * np.sin(angle)
    y = t * np.sin(angle) + noise * np.cos(angle)
    return list(zip(x.tolist(), y.tolist()))
