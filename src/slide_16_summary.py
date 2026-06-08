from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ────────────────────────────────────────────────────────────
    title = make_title("Summary")

    # ── Bullet list ──────────────────────────────────────────────────────
    bullets = make_bullet_list([
        "PCA = dimensionality reduction method",
        "PCA is unsupervised (no labels needed)",
        "Based on variance, covariance, eigenvalues",
        "Eigenvectors = principal directions",
        "Eigenvalues = importance of directions",
        "PCA can compress and reconstruct images",
        "Reconstruction error → anomaly detection",
    ], font_size=26)
    bullets.next_to(title, DOWN, buff=0.45)
    bullets.to_edge(LEFT, buff=1.0)

    # ── Final flowchart ──────────────────────────────────────────────────
    flowchart = make_flowchart(
        ["Variance", "Covariance\nMatrix", "Eigen\nDecomp.", "PCA", "Projection", "Anomaly\nDetection"],
        box_width=1.8,
        font_size=14,
    )
    flowchart.scale(0.8)
    flowchart.to_edge(DOWN, buff=1.2)

    # ── Thank you text ───────────────────────────────────────────────────
    thank_you = Text("Thank you!", font_size=48, color=TEAL, weight=BOLD)
    thank_you.to_edge(DOWN, buff=0.3)

    # ── Animations ───────────────────────────────────────────────────────
    slide.play(FadeIn(title), run_time=0.7)

    # Bullets: LaggedStart
    slide.play(
        LaggedStart(*[FadeIn(b, shift=LEFT * 0.3) for b in bullets], lag_ratio=0.12),
        run_time=1.8,
    )

    # Flowchart
    boxes = flowchart[0]
    arrows = flowchart[1]
    slide.play(
        LaggedStart(*[FadeIn(b, scale=0.8) for b in boxes], lag_ratio=0.1),
        run_time=1.2,
    )
    slide.play(
        LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1),
        run_time=0.8,
    )

    # Thank you
    slide.play(FadeIn(thank_you, scale=0.6), run_time=1.0)

    slide.next_slide()
