from manim import *
from manim_slides import Slide
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


LABEL_FONT = "Arial"


def label_text(text, font_size=22, color=GRAY_TEXT, weight=NORMAL):
    return Text(
        text,
        font=LABEL_FONT,
        font_size=font_size,
        color=color,
        weight=weight,
        disable_ligatures=True,
    )


def phrase_text(text, font_size=26, color=GRAY_TEXT):
    return Tex(text, font_size=font_size, color=color)


def build(slide):
    clear_slide(slide)

    # ── Data for the geometric transformation ───────────────────────────
    matrix_a = np.array([[1.25, 0.65], [0.35, 1.55]])
    eigvals, eigvecs = np.linalg.eig(matrix_a)
    eig_idx = int(np.argmax(np.real(eigvals)))
    eigval = float(np.real(eigvals[eig_idx]))
    eigvec = np.real(eigvecs[:, eig_idx])
    eigvec = eigvec / np.linalg.norm(eigvec)
    if eigvec[0] < 0:
        eigvec = -eigvec

    # ── Title ───────────────────────────────────────────────────────────
    title = label_text("2x2 Matrices and Eigenvectors", font_size=42, color=NAVY, weight=BOLD)
    title.to_edge(UP, buff=0.36)

    # ── Left: Oxy plane, unit square, transformed parallelogram ─────────
    axes = Axes(
        x_range=[-2.2, 3.3, 1],
        y_range=[-1.7, 3.2, 1],
        x_length=5.6,
        y_length=4.15,
        axis_config={
            "color": GRAY_TEXT,
            "stroke_width": 1.7,
            "include_tip": True,
            "tip_length": 0.13,
            "tip_width": 0.08,
            "include_ticks": False,
        },
    )
    axes.move_to(LEFT * 3.35 + UP * 0.28)
    x_label = label_text("x", font_size=20, color=GRAY_TEXT).next_to(axes.x_axis, RIGHT, buff=0.08)
    y_label = label_text("y", font_size=20, color=GRAY_TEXT).next_to(axes.y_axis, UP, buff=0.08)
    axes.set_opacity(0.48)
    x_label.set_opacity(0.62)
    y_label.set_opacity(0.62)
    axes_group = VGroup(axes, x_label, y_label)

    square_pts = [np.array([0, 0]), np.array([1, 0]), np.array([1, 1]), np.array([0, 1])]
    transformed_pts = [matrix_a @ p for p in square_pts]
    ae1 = matrix_a @ np.array([1.0, 0.0])
    ae2 = matrix_a @ np.array([0.0, 1.0])

    unit_square = Polygon(
        *[axes.c2p(*p) for p in square_pts],
        stroke_color=LIGHT_GRAY,
        stroke_width=2,
        fill_color=LIGHT_GRAY,
        fill_opacity=0.08,
    )
    parallelogram = Polygon(
        *[axes.c2p(*p) for p in transformed_pts],
        stroke_color=TEAL,
        stroke_width=3,
        fill_color=TEAL,
        fill_opacity=0.14,
    )
    transformed_x_axis = Arrow(
        axes.c2p(0, 0),
        axes.c2p(*(2.55 * ae1 / np.linalg.norm(ae1))),
        color=TEAL,
        stroke_width=3.2,
        buff=0,
        max_tip_length_to_length_ratio=0.08,
    )
    transformed_y_axis = Arrow(
        axes.c2p(0, 0),
        axes.c2p(*(2.35 * ae2 / np.linalg.norm(ae2))),
        color=TEAL,
        stroke_width=3.2,
        buff=0,
        max_tip_length_to_length_ratio=0.08,
    )
    transformed_y_axis.set_opacity(0.82)
    transformed_x_label = MathTex(r"A\vec{e}_1", font_size=20, color=TEAL)
    transformed_x_label.move_to(axes.c2p(2.65, 0.28))
    transformed_y_label = MathTex(r"A\vec{e}_2", font_size=20, color=TEAL)
    transformed_y_label.move_to(axes.c2p(0.58, 2.78))
    square_label = phrase_text("Unit square", font_size=25, color=GRAY_TEXT)
    square_label.move_to(axes.c2p(0.52, -0.36))
    square_label_bg = BackgroundRectangle(square_label, color=WHITE, fill_opacity=0.8, buff=0.04)
    para_label = phrase_text("Parallelogram after $A$", font_size=20, color=TEAL)
    para_label.move_to(axes.c2p(1.72, 2.42))

    transform_note = phrase_text(
        r"Unit square $\rightarrow$ parallelogram after transformation",
        font_size=25,
        color=NAVY,
    )
    transform_note.next_to(axes_group, DOWN, buff=0.22)
    transform_note.align_to(axes_group, LEFT)

    # ── One ordinary vector example, kept subtle to avoid clutter ───────
    ordinary_v = np.array([-0.85, 0.65])
    ordinary_arrow = Arrow(
        axes.c2p(0, 0),
        axes.c2p(*ordinary_v),
        color=BLUE_C,
        stroke_width=3,
        buff=0,
        max_tip_length_to_length_ratio=0.12,
    ).set_opacity(0.62)

    normal_label = phrase_text("One ordinary vector", font_size=20, color=BLUE_C)
    normal_label.move_to(axes.c2p(-1.18, 2.75))
    normal_label_bg = BackgroundRectangle(normal_label, color=WHITE, fill_opacity=0.84, buff=0.05)

    # ── Eigenvector: same line, different length ────────────────────────
    line_len = 2.35
    eig_line = DashedLine(
        axes.c2p(*(line_len * eigvec)),
        axes.c2p(*(-line_len * eigvec)),
        color=GRAY_TEXT,
        stroke_width=2,
        dash_length=0.1,
    ).set_opacity(0.75)

    v_end = 0.72 * eigvec
    av_end = matrix_a @ v_end
    eig_arrow = Arrow(
        axes.c2p(0, 0),
        axes.c2p(*v_end),
        color=PURPLE_C,
        stroke_width=5,
        buff=0,
        max_tip_length_to_length_ratio=0.14,
    )
    eig_after_arrow = Arrow(
        axes.c2p(0, 0),
        axes.c2p(*av_end),
        color=RED_C,
        stroke_width=6,
        buff=0,
        max_tip_length_to_length_ratio=0.08,
    )

    eig_label = MathTex(r"\vec{v}", font_size=25, color=PURPLE_C)
    eig_label.next_to(eig_arrow.get_end(), DOWN, buff=0.06)
    eig_after_label = MathTex(r"A\vec{v}=\lambda\vec{v}", font_size=25, color=RED_C)
    eig_after_label.next_to(eig_after_arrow.get_end(), UR, buff=0.08)
    eig_after_label_bg = BackgroundRectangle(eig_after_label, color=WHITE, fill_opacity=0.86, buff=0.05)

    eigen_caption = phrase_text(
        "Eigenvector: same direction, different length",
        font_size=20,
        color=PURPLE_C,
    )
    eigen_caption.move_to(axes.c2p(0.88, -1.47))
    eigen_caption_bg = BackgroundRectangle(eigen_caption, color=WHITE, fill_opacity=0.86, buff=0.05)

    # ── Right: formula panel ────────────────────────────────────────────
    formula_box = RoundedRectangle(
        width=4.35,
        height=4.35,
        corner_radius=0.12,
        stroke_color=TEAL,
        stroke_width=2,
        fill_color=WHITE,
        fill_opacity=0.82,
    )
    formula_box.move_to(RIGHT * 3.65 + UP * 0.7)

    formula = MathTex(r"A\vec{v}=\lambda\vec{v}", font_size=42, color=NAVY)
    formula.next_to(formula_box.get_top(), DOWN, buff=0.28)

    def definition_row(symbol_tex, meaning, color=NAVY):
        symbol = MathTex(symbol_tex, font_size=24, color=color)
        meaning_text = label_text(meaning, font_size=14, color=GRAY_TEXT)
        row = VGroup(symbol, meaning_text).arrange(RIGHT, buff=0.16)
        return row

    definitions = VGroup(
        definition_row(r"A", "2x2 transformation matrix", TEAL),
        definition_row(r"\vec{v}", "eigenvector", PURPLE_C),
        definition_row(r"\lambda", "stretch / shrink / flip factor", TEAL),
        definition_row(r"A\vec{v}", "vector after transformation", RED_C),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
    definitions.next_to(formula, DOWN, buff=0.32)
    definitions.align_to(formula_box, LEFT).shift(RIGHT * 0.34)

    key_points = VGroup(
        phrase_text("No change of direction", font_size=24, color=TEAL),
        phrase_text("Only stretch / shrink / flip", font_size=24, color=TEAL),
        phrase_text("A special direction of the matrix", font_size=24, color=TEAL),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
    key_points.next_to(definitions, DOWN, buff=0.32)
    key_points.align_to(definitions, LEFT)

    machine_note = VGroup(
        phrase_text("A 2x2 matrix is not a square shape.", font_size=23, color=NAVY),
        phrase_text("It transforms the whole Oxy plane.", font_size=23, color=GRAY_TEXT),
        phrase_text("The teal axes show where the basis moves.", font_size=23, color=TEAL),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    machine_note.next_to(formula_box, DOWN, buff=0.18)
    machine_note.align_to(formula_box, LEFT)

    # ── Bottom: PCA connection ──────────────────────────────────────────
    pca_box = RoundedRectangle(
        width=11.9,
        height=0.78,
        corner_radius=0.12,
        stroke_color=LIGHT_GRAY,
        stroke_width=1.2,
        fill_color=LIGHT_BG,
        fill_opacity=0.95,
    )
    pca_box.to_edge(DOWN, buff=0.26)
    pca_text = VGroup(
        phrase_text("In PCA, $A$ is the covariance matrix.", font_size=22, color=NAVY),
        phrase_text("Eigenvectors become the principal directions.", font_size=22, color=GRAY_TEXT),
        phrase_text("Eigenvalues tell which directions matter more.", font_size=22, color=GRAY_TEXT),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.02)
    pca_text.move_to(pca_box.get_center())

    # ── Animation flow ──────────────────────────────────────────────────
    slide.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
    slide.play(Create(axes_group), Create(unit_square), FadeIn(square_label_bg), FadeIn(square_label), run_time=0.8)
    slide.play(
        TransformFromCopy(unit_square, parallelogram),
        Transform(axes.x_axis, transformed_x_axis),
        Transform(axes.y_axis, transformed_y_axis),
        Transform(x_label, transformed_x_label),
        Transform(y_label, transformed_y_label),
        FadeIn(para_label),
        FadeIn(transform_note),
        run_time=1.05,
    )
    slide.play(
        GrowArrow(ordinary_arrow),
        FadeIn(normal_label_bg),
        FadeIn(normal_label),
        run_time=0.8,
    )
    slide.play(Create(eig_line), FadeIn(eigen_caption_bg), FadeIn(eigen_caption), run_time=0.6)
    slide.play(GrowArrow(eig_arrow), FadeIn(eig_label), run_time=0.55)
    slide.play(
        TransformFromCopy(eig_arrow, eig_after_arrow),
        FadeIn(eig_after_label_bg),
        FadeIn(eig_after_label),
        run_time=0.8,
    )
    slide.play(
        FadeIn(formula_box),
        Write(formula),
        FadeIn(definitions, shift=UP * 0.08),
        run_time=0.9,
    )
    slide.play(FadeIn(key_points, shift=UP * 0.1), FadeIn(machine_note, shift=UP * 0.08), run_time=0.7)
    slide.play(FadeIn(pca_box), FadeIn(pca_text, shift=UP * 0.08), run_time=0.7)
    slide.wait(1.0)

    slide.next_slide()


class Matrix2x2EigenSlide(Slide):
    def construct(self):
        self.camera.background_color = ManimColor(LIGHT_BG)
        build(self)
