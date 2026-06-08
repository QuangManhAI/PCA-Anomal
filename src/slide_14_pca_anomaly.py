from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *


def build(slide):
    clear_slide(slide)

    # ── Title ────────────────────────────────────────────────────────────
    title = make_title("PCA-Based Anomaly Detection")

    # ── Pipeline flowchart ───────────────────────────────────────────────
    pipeline = make_flowchart(
        ["Normal\nData", "Fit\nPCA", "Reconstruct\nInput", "Compute\nError", "Compare\nThreshold"],
        box_width=2.0,
        font_size=16,
    )
    pipeline.scale(0.85)
    pipeline.next_to(title, DOWN, buff=0.45)

    # ── Formula ──────────────────────────────────────────────────────────
    formula = MathTex(
        r"\text{If } \|x - \hat{x}\|_2^2 > \tau, \quad \text{then } x \text{ is an anomaly}",
        font_size=32,
        color=NAVY,
    )
    formula.next_to(pipeline, DOWN, buff=0.45)

    # ── Bar chart ────────────────────────────────────────────────────────
    errors = [0.15, 0.22, 0.18, 0.25, 0.95, 0.20]
    threshold = 0.5
    bar_chart = make_error_bar_chart(errors, threshold, bar_width=0.5)
    bar_chart.scale(0.75)
    bar_chart.next_to(formula, DOWN, buff=0.45)
    bar_chart.shift(LEFT * 0.5)

    # Separate out bars, threshold line, and tau label for animation
    bars_group = bar_chart[0]       # VGroup of (bar, label) pairs
    th_line = bar_chart[1]          # DashedLine
    th_label = bar_chart[2]         # MathTex tau

    # ── Explanation bullets ──────────────────────────────────────────────
    explanation = make_bullet_list([
        "Normal samples → reconstructed well",
        "Anomalous samples → reconstructed poorly",
    ], font_size=22)
    explanation.next_to(bar_chart, DOWN, buff=0.4)

    # ── Animations ───────────────────────────────────────────────────────
    slide.play(FadeIn(title), run_time=0.7)

    # Flowchart: LaggedStart boxes then arrows
    boxes = pipeline[0]   # boxes VGroup
    arrows = pipeline[1]  # arrows VGroup
    slide.play(
        LaggedStart(*[FadeIn(b, scale=0.8) for b in boxes], lag_ratio=0.15),
        run_time=1.2,
    )
    slide.play(
        LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15),
        run_time=0.8,
    )

    # Formula
    slide.play(Write(formula), run_time=1.0)

    # Bar chart
    slide.play(
        LaggedStart(*[FadeIn(b, shift=UP * 0.3) for b in bars_group], lag_ratio=0.1),
        run_time=1.0,
    )
    slide.play(Create(th_line), FadeIn(th_label), run_time=0.7)

    # Flash the red bar (5th bar, index 4)
    red_bar_rect = bars_group[4][0]  # the Rectangle of bar index 4
    slide.play(
        Indicate(red_bar_rect, color=RED_C, scale_factor=1.15),
        run_time=0.7,
    )

    # Explanation
    slide.play(
        LaggedStart(*[FadeIn(b, shift=LEFT * 0.3) for b in explanation], lag_ratio=0.2),
        run_time=0.8,
    )

    slide.next_slide()
