from manim import *
import html
import io
import keyword
import tokenize
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from helpers import *

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
PCA_OUTPUT_IMAGE = os.path.join(PROJECT_ROOT, "output_1.png")
ANOMALY_OUTPUT_IMAGE = os.path.join(PROJECT_ROOT, "output_2.png")


TOKEN_COLORS = {
    "keyword": "#2563EB",
    "function": "#D97706",
    "builtin": "#059669",
    "name": "#111827",
    "comment": "#0E7490",
    "string": "#DC2626",
    "number": "#16A34A",
    "operator": "#4B5563",
}


def escape_code(text):
    return html.escape(text).replace(" ", "&#160;")


def make_markup_text(text, font_size, color, bold=False):
    weight = ' font_weight="bold"' if bold else ""
    return MarkupText(
        f'<span foreground="{color}"{weight}>{escape_code(text)}</span>',
        font="Arial",
        font_size=font_size,
    )


def python_to_markup(code):
    parts = []
    previous_end = (1, 0)
    previous_name = None
    builtin_names = {"print", "len", "range"}

    tokens = tokenize.generate_tokens(io.StringIO(code).readline)
    for tok in tokens:
        token_type = tok.type
        token_text = tok.string
        start = tok.start
        end = tok.end

        if token_type in {tokenize.ENCODING, tokenize.ENDMARKER}:
            continue

        row_gap = start[0] - previous_end[0]
        if row_gap:
            parts.append("\n" * row_gap)
            parts.append("&#160;" * start[1])
        else:
            parts.append("&#160;" * max(0, start[1] - previous_end[1]))

        color = TOKEN_COLORS["name"]
        if token_type == tokenize.COMMENT:
            color = TOKEN_COLORS["comment"]
        elif token_type == tokenize.STRING:
            color = TOKEN_COLORS["string"]
        elif token_type == tokenize.NUMBER:
            color = TOKEN_COLORS["number"]
        elif token_type == tokenize.OP:
            color = TOKEN_COLORS["operator"]
        elif token_type == tokenize.NAME:
            if keyword.iskeyword(token_text):
                color = TOKEN_COLORS["keyword"]
            elif previous_name == "def":
                color = TOKEN_COLORS["function"]
            elif token_text in builtin_names:
                color = TOKEN_COLORS["builtin"]

        parts.append(f'<span foreground="{color}">{escape_code(token_text)}</span>')
        previous_end = end
        if token_type == tokenize.NAME:
            previous_name = token_text
        elif token_type not in {tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT}:
            previous_name = None

    return "".join(parts)


def make_code_block(code, label, width=5.7, height=2.25, font_size=13):
    title = make_markup_text(label, font_size=16, color="#0F766E", bold=True)
    code_mob = MarkupText(
        python_to_markup(code.strip()),
        font="Menlo",
        font_size=font_size,
        line_spacing=0.62,
    )
    if code_mob.width > width - 0.34:
        code_mob.scale_to_fit_width(width - 0.34)
    if code_mob.height > height - 0.34:
        code_mob.scale_to_fit_height(height - 0.34)

    frame = RoundedRectangle(
        width=max(width, code_mob.width + 0.34),
        height=max(height, code_mob.height + 0.34),
        corner_radius=0.10,
        fill_color=WHITE,
        fill_opacity=0.94,
        stroke_color=LIGHT_GRAY,
        stroke_width=1,
    )
    code_mob.move_to(frame.get_center())
    code_mob.align_to(frame, LEFT).shift(RIGHT * 0.17)
    block = VGroup(frame, code_mob)
    return VGroup(title, block).arrange(DOWN, aligned_edge=LEFT, buff=0.08)


def make_section_title(text, subtitle=None):
    title = make_markup_text(text, font_size=34, color="#111827", bold=True)
    title.to_edge(UP, buff=0.42)
    if subtitle is None:
        return VGroup(title)
    sub = make_markup_text(subtitle, font_size=18, color="#4B5563")
    sub.next_to(title, DOWN, buff=0.14)
    return VGroup(title, sub)


def play_code_grid(slide, title, blocks):
    slide.play(FadeIn(title), run_time=0.5)
    slide.play(
        LaggedStart(*[FadeIn(block, shift=UP * 0.12) for block in blocks], lag_ratio=0.14),
        run_time=1.15,
    )
    slide.wait(0.4)
    slide.next_slide()


def play_image_output(slide, title_text, subtitle, image_path, caption):
    clear_slide(slide)
    title = make_section_title(title_text, subtitle)
    image = ImageMobject(image_path)
    image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bicubic"])
    image.scale_to_fit_width(8.7)
    image.scale_to_fit_height(5.25)
    image.next_to(title, DOWN, buff=0.24)

    caption_text = make_markup_text(caption, font_size=17, color="#374151")
    caption_text.next_to(image, DOWN, buff=0.16)

    slide.play(FadeIn(title), run_time=0.5)
    slide.play(FadeIn(image, shift=UP * 0.12), FadeIn(caption_text), run_time=0.85)
    slide.wait(0.4)
    slide.next_slide()


def build(slide):
    # Slide A: imports and PCA core functions.
    clear_slide(slide)
    title = make_section_title(
        "PCA Notebook Code",
        "Setup, centering, covariance, eigendecomposition",
    )

    import_code = """
import numpy as np
"""
    center_code = """
def compute_center(X):
    means = np.mean(X, axis=0)
    X_centered = X - means
    return X_centered, means
"""
    cov_code = """
def compute_covariance_matrix(X_centered):
    n_samples = X_centered.shape[0]
    covariance_matrix = np.dot(X_centered.T, X_centered) / (n_samples - 1)
    return covariance_matrix
"""
    eigen_code = """
def eigendecompose_covariance_matrix(covariance_matrix):
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    return eigenvalues, eigenvectors
"""

    core_blocks = VGroup(
        VGroup(
            make_code_block(import_code, "Cell 0: Import", width=5.4, height=0.95, font_size=14),
            make_code_block(center_code, "Cell 1: Center data", width=5.4, height=1.72),
            make_code_block(cov_code, "Cell 2: Covariance matrix", width=5.4, height=1.95),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20),
        make_code_block(eigen_code, "Cell 3: Eigen decomposition", width=6.35, height=4.9, font_size=12.5),
    ).arrange(RIGHT, aligned_edge=UP, buff=0.45)
    core_blocks.next_to(title, DOWN, buff=0.32)
    play_code_grid(slide, title, core_blocks)

    # Slide B: choose components and project.
    clear_slide(slide)
    title = make_section_title("PCA Notebook Code", "Select components and project centered data")

    select_code = """
def select_top_k_components(eigenvalues, eigenvectors, k):
    top_k_eigenvalues = eigenvalues[:k]
    top_k_eigenvectors = eigenvectors[:, :k]
    return top_k_eigenvalues, top_k_eigenvectors
"""
    project_code = """
def project_data(X_centered, top_k_eigenvectors):
    projected_data = np.dot(X_centered, top_k_eigenvectors)
    return projected_data
"""
    pca_code = """
def pca(X, k):
    X_centered, means = compute_center(X)
    covariance_matrix = compute_covariance_matrix(X_centered)
    eigenvalues, eigenvectors = eigendecompose_covariance_matrix(covariance_matrix)
    top_k_eigenvalues, top_k_eigenvectors = select_top_k_components(eigenvalues, eigenvectors, k)
    projected_data = project_data(X_centered, top_k_eigenvectors)
    return projected_data, top_k_eigenvalues, top_k_eigenvectors
"""

    body = VGroup(
        make_code_block(select_code, "Cell 4: Select top-k", width=8.2, height=2.05, font_size=14.0),
        make_code_block(project_code, "Cell 5: Project", width=8.2, height=1.85, font_size=14.0),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
    body.next_to(title, DOWN, buff=0.36)
    body.shift(RIGHT * 0.15)
    play_code_grid(slide, title, body)

    # Slide C: PCA wrapper.
    clear_slide(slide)
    title = make_section_title("PCA Notebook Code", "Cell 6 wraps the PCA pipeline")

    body = make_code_block(
        pca_code,
        "Cell 6: PCA wrapper",
        width=11.75,
        height=4.85,
        font_size=12.5,
    )
    body.next_to(title, DOWN, buff=0.35)
    play_code_grid(slide, title, VGroup(body))

    # Slide D: generate demo data.
    clear_slide(slide)
    title = make_section_title("PCA Notebook Code", "Create a small correlated 2D dataset")

    data_code = """
# Create a small 2D correlated dataset
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

    body = make_code_block(
        data_code,
        "Cell 7: Demo data",
        width=10.75,
        height=5.35,
        font_size=13.0,
    )
    body.next_to(title, DOWN, buff=0.30)
    play_code_grid(slide, title, VGroup(body))

    # Slide E: run PCA and inspect variance.
    clear_slide(slide)
    title = make_section_title("PCA Notebook Code", "Run PCA and inspect explained variance")

    run_code = """
# Run PCA
Z1, eigenvalues_1d, W1 = pca(X, k=1)
Z2, eigenvalues_2d, W2 = pca(X, k=2)

X_centered, means = compute_center(X)
cov_matrix = compute_covariance_matrix(X_centered)
all_eigenvalues, all_eigenvectors = eigendecompose_covariance_matrix(cov_matrix)
explained_variance_ratio = all_eigenvalues / all_eigenvalues.sum()

print("X shape:", X.shape)
print("Z1 shape:", Z1.shape)
print("Z2 shape:", Z2.shape)
print("covariance matrix:\\n", cov_matrix)
print("eigenvalues:", all_eigenvalues)
print("explained variance ratio:", explained_variance_ratio)
"""
    body = make_code_block(
        run_code,
        "Cell 8: Run PCA",
        width=11.75,
        height=5.35,
        font_size=11.8,
    )
    body.next_to(title, DOWN, buff=0.30)
    play_code_grid(slide, title, VGroup(body))

    play_image_output(
        slide,
        "PCA Notebook Output",
        "Principal directions learned from the correlated 2D data",
        PCA_OUTPUT_IMAGE,
        "PC1 captures the main spread; PC2 captures the small leftover direction.",
    )

    # Slide F: reconstruct data and add anomalies.
    clear_slide(slide)
    title = make_section_title("PCA Notebook Code", "Reconstruct data and prepare anomaly points")

    reconstruct_code = """
def reconstruct_data(Z, W, means):
    return Z @ W.T + means
"""
    error_code = """
def reconstruct_error(X, X_reconstructed):
    errors = np.sum((X - X_reconstructed) ** 2, axis=1)
    return errors
"""
    anomaly_data_code = """
# Add a few obvious anomalies away from the main PCA direction
anomalies = np.array([
    [1.2, -3.0],
    [2.0, -2.5],
    [-1.4, 2.7],
])

X_with_anomalies = np.vstack([X, anomalies])
true_labels = np.array([0] * len(X) + [1] * len(anomalies))

X_with_anomalies.shape
"""
    body = VGroup(
        VGroup(
            make_code_block(reconstruct_code, "Cell 10: Reconstruct", width=5.4, height=1.55),
            make_code_block(error_code, "Cell 11: Error", width=5.4, height=1.65),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28),
        make_code_block(anomaly_data_code, "Cell 12: Add anomalies", width=6.25, height=4.15, font_size=12.2),
    ).arrange(RIGHT, aligned_edge=UP, buff=0.5)
    body.next_to(title, DOWN, buff=0.35)
    play_code_grid(slide, title, body)

    # Slide G: fit normal PCA and score all points.
    clear_slide(slide)
    title = make_section_title("PCA Notebook Code", "Score anomalies with reconstruction error")

    anomaly_score_code = """
# PCA anomaly detection using reconstruction error
# Fit PCA on normal data, then score all points.
k = 1

X_centered_normal, normal_mean = compute_center(X)
normal_cov = compute_covariance_matrix(X_centered_normal)
normal_eigenvalues, normal_eigenvectors = eigendecompose_covariance_matrix(normal_cov)
_, W_anomaly = select_top_k_components(normal_eigenvalues, normal_eigenvectors, k)

X_all_centered = X_with_anomalies - normal_mean
Z_all = project_data(X_all_centered, W_anomaly)
X_reconstructed = reconstruct_data(Z_all, W_anomaly, normal_mean)
errors = reconstruct_error(X_with_anomalies, X_reconstructed)

normal_errors = errors[:len(X)]
threshold = normal_errors.max() * 1.2
predicted_anomaly = errors > threshold

print("threshold:", threshold)
print("errors:", errors)
print("predicted anomaly:", predicted_anomaly)
"""
    body = make_code_block(
        anomaly_score_code,
        "Cell 13: Fit normal PCA, reconstruct, threshold",
        width=12.05,
        height=5.55,
        font_size=11.4,
    )
    body.next_to(title, DOWN, buff=0.30)
    play_code_grid(slide, title, VGroup(body))

    play_image_output(
        slide,
        "PCA Notebook Output",
        "Anomaly result from reconstruction error",
        ANOMALY_OUTPUT_IMAGE,
        "Points far from the learned PC1 direction get large reconstruction error.",
    )
