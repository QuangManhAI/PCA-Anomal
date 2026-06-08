from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def _make_vector_column(n, cell_size=0.18, colors=None):
    """Create a vertical column of small squares representing a vector."""
    col = VGroup()
    for i in range(n):
        c = colors[i] if colors is not None else LIGHT_GRAY
        sq = Square(
            side_length=cell_size,
            fill_color=c,
            fill_opacity=0.9,
            stroke_width=0.5,
            stroke_color=LIGHT_GRAY,
        )
        sq.move_to([0, -i * cell_size, 0])
        col.add(sq)
    col.move_to(ORIGIN)
    return col


def build(slide):
    clear_slide(slide)

    # ── Title ─────────────────────────────────────────────────────────────
    title = make_title("PCA on Images")
    slide.play(FadeIn(title), run_time=0.8)

    # ── Explanation bullets ───────────────────────────────────────────────
    bullets = make_bullet_list([
        "A grayscale image = matrix of pixels",
        "Flatten into a long vector",
        "PCA compresses to k dimensions",
    ], font_size=24)
    bullets.next_to(title, DOWN, buff=0.35)

    slide.play(FadeIn(bullets, shift=UP * 0.2), run_time=0.8)

    # ── Formula ───────────────────────────────────────────────────────────
    formula = MathTex(
        r"\text{image}\in\mathbb{R}^{h\times w}",
        r"\quad\Rightarrow\quad",
        r"x\in\mathbb{R}^{hw}",
        r"\quad\Rightarrow\quad",
        r"z\in\mathbb{R}^{k}",
        font_size=30, color=NAVY,
    )
    formula.next_to(bullets, DOWN, buff=0.35)

    slide.play(Write(formula), run_time=1.0)
    slide.wait(0.3)

    # ── Visual pipeline ──────────────────────────────────────────────────
    # 1. Original 8x8 grid  (diagonal gradient pattern)
    pattern = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            pattern[i, j] = (i + j) / 14.0  # diagonal gradient 0..1
    # Add a simple "cross" to make it look like a digit
    pattern[3, :] = np.clip(pattern[3, :] + 0.3, 0, 1)
    pattern[:, 3] = np.clip(pattern[:, 3] + 0.3, 0, 1)
    pattern = np.clip(pattern, 0, 1)

    original_grid = make_image_grid(pattern, cell_size=0.28)
    original_label = Text("Original 8×8", font_size=18, color=GRAY_TEXT)

    # 2. Flattened vector (64 cells, shown as a tall thin column — show 16 representative cells)
    flat_vals = pattern.flatten()
    flat_colors = []
    for v in flat_vals:
        g = int((1 - v) * 255)
        flat_colors.append(f"#{g:02x}{g:02x}{g:02x}")
    # Show only 16 cells + ellipsis visual for compactness
    vec_short = _make_vector_column(16, cell_size=0.14, colors=flat_colors[:16])
    # Add dots to indicate continuation
    dots_txt = MathTex(r"\vdots", font_size=24, color=GRAY_TEXT)
    dots_txt.next_to(vec_short, DOWN, buff=0.08)
    vector_group = VGroup(vec_short, dots_txt)
    vector_label = Text("Vector (64)", font_size=18, color=GRAY_TEXT)

    # 3. Compressed vector (10 cells)
    compressed_colors = [TEAL] * 10
    compressed_vec = _make_vector_column(10, cell_size=0.14, colors=compressed_colors)
    compressed_label = Text("Compressed (10)", font_size=18, color=GRAY_TEXT)

    # 4. Reconstructed 8x8 grid (blurred version)
    recon = pattern.copy()
    # Simple blur: average with neighbors
    kernel = np.array([[0, 1, 0], [1, 4, 1], [0, 1, 0]]) / 8.0
    padded = np.pad(recon, 1, mode="edge")
    blurred = np.zeros_like(recon)
    for i in range(8):
        for j in range(8):
            blurred[i, j] = np.sum(padded[i:i+3, j:j+3] * kernel)
    blurred = np.clip(blurred, 0, 1)
    recon_grid = make_image_grid(blurred, cell_size=0.28)
    recon_label = Text("Reconstructed", font_size=18, color=GRAY_TEXT)

    # ── Arrange pipeline horizontally ─────────────────────────────────────
    arrow1 = Arrow(ORIGIN, RIGHT * 0.9, color=GRAY_TEXT, stroke_width=2, buff=0)
    arrow2 = Arrow(ORIGIN, RIGHT * 0.9, color=GRAY_TEXT, stroke_width=2, buff=0)
    arrow3 = Arrow(ORIGIN, RIGHT * 0.9, color=GRAY_TEXT, stroke_width=2, buff=0)

    pipeline = VGroup(
        original_grid, arrow1, vector_group, arrow2, compressed_vec, arrow3, recon_grid
    )
    pipeline.arrange(RIGHT, buff=0.4)
    pipeline.next_to(formula, DOWN, buff=0.45)

    # Ensure it fits on screen
    if pipeline.get_width() > 13:
        pipeline.scale(13 / pipeline.get_width())

    # Position labels under each element
    original_label.next_to(original_grid, DOWN, buff=0.15)
    vector_label.next_to(vector_group, DOWN, buff=0.15)
    compressed_label.next_to(compressed_vec, DOWN, buff=0.15)
    recon_label.next_to(recon_grid, DOWN, buff=0.15)

    labels = VGroup(original_label, vector_label, compressed_label, recon_label)

    # ── Animate pipeline left to right ────────────────────────────────────
    slide.play(FadeIn(original_grid, shift=UP * 0.3), FadeIn(original_label), run_time=0.7)
    slide.play(GrowArrow(arrow1), run_time=0.4)
    slide.play(FadeIn(vector_group, shift=UP * 0.3), FadeIn(vector_label), run_time=0.7)
    slide.play(GrowArrow(arrow2), run_time=0.4)
    slide.play(FadeIn(compressed_vec, shift=UP * 0.3), FadeIn(compressed_label), run_time=0.7)
    slide.play(GrowArrow(arrow3), run_time=0.4)
    slide.play(FadeIn(recon_grid, shift=UP * 0.3), FadeIn(recon_label), run_time=0.7)
    slide.wait(0.5)

    slide.next_slide()
