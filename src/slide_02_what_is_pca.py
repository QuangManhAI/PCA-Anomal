from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ───────────────────────────────────────────────────────────
    title_group = make_title("What is PCA? The Big Picture")
    slide.play(FadeIn(title_group, shift=DOWN * 0.3), run_time=0.6)

    # ── Flow diagram (horizontal) ───────────────────────────────────────
    labels = [
        "Data",
        "Variance &\nCovariance",
        "Covariance\nMatrix Σ",
        "Eigen-\ndecomposition",
        "PC₁, PC₂, ..."
    ]
    flowchart = make_flowchart(labels, box_width=2.2, box_height=0.8, font_size=15)
    flowchart.next_to(title_group, DOWN, buff=0.45)
    
    boxes = flowchart[0]
    arrows = flowchart[1]
    
    flowchart_anims = []
    for i in range(len(boxes)):
        flowchart_anims.append(FadeIn(boxes[i], shift=RIGHT * 0.2))
        if i < len(arrows):
            flowchart_anims.append(Create(arrows[i]))
            
    slide.play(LaggedStart(*flowchart_anims, lag_ratio=0.25), run_time=1.8)

    # ── Key Insight (Transformation) ──────────────────────────────────
    left_formula = MathTex(
        r"\Sigma = \begin{bmatrix} \sigma_{x}^2 & \sigma_{xy} \\ \sigma_{yx} & \sigma_{y}^2 \end{bmatrix}",
        font_size=30, color=NAVY
    )
    left_lbl = Text("Matrix (many numbers)", font_size=16, color=GRAY_TEXT)
    left_box = VGroup(left_formula, left_lbl).arrange(DOWN, buff=0.15)

    arr1 = MathTex(r"\longrightarrow", font_size=36, color=TEAL)

    mid_formula = MathTex(r"A\vec{v} = \lambda\vec{v}", font_size=36, color=NAVY)
    mid_lbl = Text("Eigendecomposition", font_size=16, color=GRAY_TEXT)
    mid_box = VGroup(mid_formula, mid_lbl).arrange(DOWN, buff=0.15)

    arr2 = MathTex(r"\longrightarrow", font_size=36, color=TEAL)

    right_formula = MathTex(r"\vec{v},\; \lambda", font_size=36, color=TEAL)
    right_lbl = Text("Vector v⃗ + Scalar λ", font_size=16, color=GRAY_TEXT)
    right_sub = Text("Dimensionality Reduction!", font_size=16, color=TEAL, weight=BOLD)
    right_box = VGroup(right_formula, right_lbl, right_sub).arrange(DOWN, buff=0.12)

    insight_group = VGroup(left_box, arr1, mid_box, arr2, right_box).arrange(RIGHT, buff=0.45)
    insight_group.next_to(flowchart, DOWN, buff=0.55)

    slide.play(
        FadeIn(left_box, shift=UP * 0.2),
        run_time=0.6
    )
    slide.play(
        Create(arr1),
        FadeIn(mid_box, shift=UP * 0.2),
        run_time=0.8
    )
    slide.play(
        Create(arr2),
        FadeIn(right_box, shift=UP * 0.2),
        run_time=0.8
    )

    # ── Bullets ───────────────────────────────────────────────────────
    bullets = make_bullet_list([
        "Matrix A is reduced to directions (eigenvectors v⃗) and scaling factors (eigenvalues λ)",
        "This reduction is the core mathematical engine of PCA dimensionality reduction",
    ], font_size=20)
    bullets.next_to(insight_group, DOWN, buff=0.5)
    
    slide.play(
        LaggedStart(*[Write(b) for b in bullets], lag_ratio=0.4),
        run_time=1.0
    )
    slide.wait(1.0)

    slide.next_slide()
