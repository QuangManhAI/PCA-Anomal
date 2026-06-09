"""
PCA and Anomaly Detection — Manim-Slides Lecture
=================================================
Main entry point that imports all 17 slides and builds
the complete presentation deck.

Render with:
    manim render -qh --fps 60 src/main.py PCAAnomalyDeck

Export video with manim-slides:
    manim-slides render -qh src/main.py PCAAnomalyDeck
    manim-slides convert PCAAnomalyDeck output.mp4
"""

from manim import *
from manim_slides import Slide
import sys
import os

# Ensure src directory is in the path
sys.path.insert(0, os.path.dirname(__file__))

from helpers import LIGHT_BG

# Import all slide modules
from slide_01_title import build as build_slide_01
from slide_02_what_is_pca import build as build_slide_02
from slide_03_unsupervised import build as build_slide_03
from slide_04_eigen_process import build as build_slide_04_process
from slide_04_intuition import build as build_slide_04
from slide_05_variance import build as build_slide_05
from slide_06_covariance import build as build_slide_06
from slide_07_cov_matrix import build as build_slide_07
from slide_08_eigen import build as build_slide_08
from slide_09_algorithm import build as build_slide_09
from slide_10_projection import build as build_slide_10
from slide_11_pca_images import build as build_slide_11
from slide_12_reconstruction import build as build_slide_12
from slide_13_anomaly_intro import build as build_slide_13
from slide_14_pca_anomaly import build as build_slide_14
from slide_15_full_example import build as build_slide_15
from slide_16_summary import build as build_slide_16


class PCAAnomalyDeck(Slide):
    """Complete PCA and Anomaly Detection lecture deck."""

    def construct(self):
        # Set light theme background (wrap in ManimColor for manim-slides compat)
        self.camera.background_color = ManimColor(LIGHT_BG)

        # Build all 17 slides in order
        build_slide_01(self)
        build_slide_02(self)
        build_slide_03(self)
        build_slide_04_process(self)
        build_slide_04(self)
        build_slide_05(self)
        build_slide_06(self)
        build_slide_07(self)
        build_slide_08(self)
        build_slide_09(self)
        build_slide_10(self)
        build_slide_11(self)
        build_slide_12(self)
        build_slide_13(self)
        build_slide_14(self)
        build_slide_15(self)
        build_slide_16(self)
