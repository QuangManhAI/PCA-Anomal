from manim import *
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from helpers import *
from slide_17_pca_notebook_code import (
    make_code_block,
    make_section_title,
    play_code_grid,
    play_image_output,
)


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
GAUSSIAN_DISTRIBUTION_IMAGE = os.path.join(PROJECT_ROOT, "output_gaussian_distribution.png")
GAUSSIAN_ANOMALY_IMAGE = os.path.join(PROJECT_ROOT, "output_gaussian_anomaly.png")


def build(slide):
    # Slide A: imports and Gaussian parameter estimation.
    clear_slide(slide)
    title = make_section_title(
        "Gaussian Notebook Code",
        "Fit mean and full covariance from the same PCA data",
    )

    import_code = """
import numpy as np
import matplotlib.pyplot as plt
"""
    estimate_code = """
def estimate_gaussian_parameters(X):
    mu = np.mean(X, axis=0)
    covariance_matrix = np.cov(X, rowvar=False)
    return mu, covariance_matrix
"""

    body = VGroup(
        make_code_block(import_code, "Cell 0: Import", width=7.8, height=1.25, font_size=14.0),
        make_code_block(estimate_code, "Cell 1: Estimate mu and covariance", width=7.8, height=1.95, font_size=14.0),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    body.next_to(title, DOWN, buff=0.42)
    play_code_grid(slide, title, body)

    # Slide B: Gaussian probability.
    clear_slide(slide)
    title = make_section_title(
        "Gaussian Notebook Code",
        "Convert each 2D point into a probability density",
    )

    pdf_code = """
def gaussian_pdf(X, mu, covariance_matrix):
    n_features = X.shape[1]
    covariance_matrix = covariance_matrix + 1e-8 * np.eye(n_features)

    centered = X - mu
    inverse_covariance = np.linalg.inv(covariance_matrix)
    determinant = np.linalg.det(covariance_matrix)

    coefficient = 1 / np.sqrt(((2 * np.pi) ** n_features) * determinant)
    exponent = np.einsum("ij,jk,ik->i", centered, inverse_covariance, centered)
    probabilities = coefficient * np.exp(-0.5 * exponent)
    return probabilities
"""

    body = make_code_block(pdf_code, "Cell 2: Multivariate Gaussian PDF", width=11.3, height=5.0, font_size=11.7)
    body.next_to(title, DOWN, buff=0.30)
    play_code_grid(slide, title, VGroup(body))

    play_image_output(
        slide,
        "Gaussian Notebook Output",
        "Cell 3 visualizes normal probability and anomaly tails",
        GAUSSIAN_DISTRIBUTION_IMAGE,
        "The center has high probability; the far tails have low probability.",
    )

    # Slide C: prediction rule.
    clear_slide(slide)
    title = make_section_title(
        "Gaussian Notebook Code",
        "Low probability means anomaly",
    )

    predict_code = """
def predict_anomalies(probabilities, epsilon):
    return probabilities < epsilon
"""

    body = make_code_block(predict_code, "Cell 4: Predict", width=7.2, height=1.70, font_size=15.0)
    body.next_to(title, DOWN, buff=0.55)
    play_code_grid(slide, title, VGroup(body))

    # Slide D: same training data as PCA.
    clear_slide(slide)
    title = make_section_title(
        "Gaussian Notebook Code",
        "Use the same correlated 2D dataset as PCA",
    )

    train_code = """
# Use the same correlated 2D dataset as the PCA notebook
rng = np.random.default_rng(42)

n_points = 40
pc1 = rng.normal(0, 2.0, size=n_points)
pc2 = rng.normal(0, 0.45, size=n_points)

theta = np.deg2rad(35)
R = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)],
])

X = np.column_stack([pc1, pc2]) @ R.T
X[:5]
"""

    body = make_code_block(train_code, "Cell 5: Same PCA dataset", width=10.8, height=5.25, font_size=12.3)
    body.next_to(title, DOWN, buff=0.28)
    play_code_grid(slide, title, VGroup(body))

    # Slide E: same anomalies as PCA.
    clear_slide(slide)
    title = make_section_title(
        "Gaussian Notebook Code",
        "Add the same anomaly points",
    )

    anomaly_code = """
# Add the same obvious anomalies used in the PCA notebook
anomalies = np.array([
    [1.2, -3.0],
    [2.0, -2.5],
    [-1.4, 2.7],
])

X_with_anomalies = np.vstack([X, anomalies])
true_labels = np.array([0] * len(X) + [1] * len(anomalies))

X_with_anomalies.shape
"""

    body = make_code_block(anomaly_code, "Cell 6: Same anomaly points", width=9.8, height=4.40, font_size=13.0)
    body.next_to(title, DOWN, buff=0.32)
    play_code_grid(slide, title, VGroup(body))

    # Slide F: fit and score.
    clear_slide(slide)
    title = make_section_title(
        "Gaussian Notebook Code",
        "Fit Gaussian, score points, flag low probability",
    )

    fit_code = """
# Fit Gaussian on normal data, then score all points
mu, covariance_matrix = estimate_gaussian_parameters(X)

normal_probabilities = gaussian_pdf(X, mu, covariance_matrix)
all_probabilities = gaussian_pdf(X_with_anomalies, mu, covariance_matrix)

epsilon = normal_probabilities.min() * 0.8
predicted_anomaly = predict_anomalies(all_probabilities, epsilon)

print("mu:", mu)
print("covariance matrix:\\n", covariance_matrix)
print("epsilon:", epsilon)
print("predicted anomalies:", np.where(predicted_anomaly)[0])
print("true anomalies:", np.where(true_labels == 1)[0])
"""

    body = make_code_block(fit_code, "Cell 7: Fit and predict", width=11.2, height=5.55, font_size=11.5)
    body.next_to(title, DOWN, buff=0.24)
    play_code_grid(slide, title, VGroup(body))

    play_image_output(
        slide,
        "Gaussian Notebook Output",
        "Cell 8 plots Gaussian anomaly detection on the same PCA dataset",
        GAUSSIAN_ANOMALY_IMAGE,
        "Blue points are normal; red points are low-probability Gaussian anomalies.",
    )
