from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ─────────────────────────────────────────────────────────────
    title = make_title("Reconstruction Error")
    slide.play(FadeIn(title), run_time=0.8)

    # ── Three formulas ────────────────────────────────────────────────────
    f1 = MathTex(r"z = W^\top x", font_size=36, color=NAVY)
    f2 = MathTex(r"\hat{x} = Wz = WW^\top x", font_size=36, color=NAVY)
    f3 = MathTex(
        r"\mathrm{error}(x) = \|x - \hat{x}\|_2^2",
        font_size=36, color=RED_C,
    )
    formulas = VGroup(f1, f2, f3).arrange(DOWN, buff=0.3)
    formulas.next_to(title, DOWN, buff=0.4)

    slide.play(Write(f1), run_time=0.7)
    slide.play(Write(f2), run_time=0.7)
    slide.play(Write(f3), run_time=0.7)
    slide.wait(0.3)

    # ── 8×8 grids: Original / Reconstructed / Error ───────────────────────

    # Original pattern — cross + gradient
    original = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            original[i, j] = (i + j) / 14.0
    original[3, :] = np.clip(original[3, :] + 0.35, 0, 1)
    original[:, 3] = np.clip(original[:, 3] + 0.35, 0, 1)
    original = np.clip(original, 0, 1)

    # Reconstructed — blurred version
    kernel = np.array([[0, 1, 0], [1, 4, 1], [0, 1, 0]]) / 8.0
    padded = np.pad(original, 1, mode="edge")
    recon = np.zeros_like(original)
    for i in range(8):
        for j in range(8):
            recon[i, j] = np.sum(padded[i:i+3, j:j+3] * kernel)
    recon = np.clip(recon, 0, 1)

    # Error — absolute difference, mapped to red intensity
    diff = np.abs(original - recon)
    max_diff = diff.max() if diff.max() > 0 else 1.0
    diff_norm = diff / max_diff  # normalize to [0, 1]

    # Build grids
    grid_original = make_image_grid(original, cell_size=0.25)
    grid_recon = make_image_grid(recon, cell_size=0.25)

    # Error grid — use red tones instead of grayscale
    error_grid = VGroup()
    for i in range(8):
        for j in range(8):
            val = float(diff_norm[i, j])
            # Interpolate from white (#ffffff) to red (#dc2626)
            r = int(255 - val * (255 - 0xDC))
            g = int(255 - val * (255 - 0x26))
            b = int(255 - val * (255 - 0x26))
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            cell = Square(
                side_length=0.25,
                fill_color=hex_color,
                fill_opacity=1.0,
                stroke_width=0.5,
                stroke_color=LIGHT_GRAY,
            )
            cell.move_to([j * 0.25, -i * 0.25, 0])
            error_grid.add(cell)
    error_grid.move_to(ORIGIN)

    # Labels
    lbl_orig = Text("Original", font_size=20, color=GRAY_TEXT)
    lbl_recon = Text("Reconstructed", font_size=20, color=GRAY_TEXT)
    lbl_error = Text("Error", font_size=20, color=RED_C)

    # Column layout
    col1 = VGroup(lbl_orig, grid_original).arrange(DOWN, buff=0.2)
    col2 = VGroup(lbl_recon, grid_recon).arrange(DOWN, buff=0.2)
    col3 = VGroup(lbl_error, error_grid).arrange(DOWN, buff=0.2)

    minus_sign = MathTex("-", font_size=36, color=GRAY_TEXT)
    equals_sign = MathTex("=", font_size=36, color=GRAY_TEXT)

    grids_row = VGroup(col1, minus_sign, col2, equals_sign, col3)
    grids_row.arrange(RIGHT, buff=0.5)
    grids_row.next_to(formulas, DOWN, buff=0.45)

    # Ensure it fits on screen
    if grids_row.get_width() > 13:
        grids_row.scale(13 / grids_row.get_width())

    # Animate grids
    slide.play(FadeIn(col1, shift=UP * 0.2), run_time=0.7)
    slide.play(FadeIn(minus_sign), run_time=0.3)
    slide.play(FadeIn(col2, shift=UP * 0.2), run_time=0.7)
    slide.play(FadeIn(equals_sign), run_time=0.3)
    slide.play(FadeIn(col3, shift=UP * 0.2), run_time=0.7)
    slide.wait(0.3)

    # ── Error value ───────────────────────────────────────────────────────
    mse = float(np.mean(diff ** 2))
    error_text = Text(f"Error = {mse:.4f}", font_size=28, color=GREEN_C)
    error_text.next_to(grids_row, DOWN, buff=0.3)
    slide.play(FadeIn(error_text, scale=1.2), run_time=0.6)

    # ── Explanation bullets ───────────────────────────────────────────────
    explanation = make_bullet_list([
        "Small error → matches PCA structure",
        "Large error → may be unusual",
    ], font_size=22)
    explanation.next_to(error_text, DOWN, buff=0.3)

    # Ensure bullets stay on screen
    if explanation.get_bottom()[1] < -3.7:
        explanation.shift(UP * (abs(explanation.get_bottom()[1]) - 3.5))

    slide.play(FadeIn(explanation, shift=UP * 0.2), run_time=0.8)
    slide.wait(0.5)

    slide.next_slide()
