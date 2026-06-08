Please create a complete Manim-Slides lecture in English with the topic:

“PCA and Anomaly Detection — From Variance, Covariance, and Eigenvalues to Detecting Outliers”

The goal of this lecture is to explain:

* What PCA is.
* Why PCA belongs to unsupervised learning.
* The intuition behind variance, covariance, and the covariance matrix.
* The role of eigenvalues and eigenvectors in PCA.
* The step-by-step PCA algorithm.
* How PCA works on images.
* What anomaly detection is.
* How PCA reconstruction error can be used for anomaly detection.

Technical requirements:

* Use Manim-Slides.
* Create one main class named `PCAAnomalyDeck(Slide)`.
* Each slide must end with `self.next_slide()`.
* The whole project should be in one Python file.
* The lecture content shown on screen must be in English.
* Use clean, readable, and editable code.
* Use helper functions where appropriate.
* Do not depend on the internet.
* If image data is needed, either use a simple generated matrix image or try `sklearn.datasets.load_digits()` with a safe fallback if sklearn is unavailable.
* Use `Text`, `MathTex`, `VGroup`, `Axes`, `Dot`, `Arrow`, `Line`, `Rectangle`, `SurroundingRectangle`, `NumberPlane`, and other suitable Manim objects.
* Avoid text overflow.
* Prefer geometric and visual explanation over long paragraphs.
* Use a 16:9 layout suitable for 1920x1080 rendering.

Theme and visual style:

* Use a light theme.
* Background color: white or soft off-white, for example `#F8FAFC`.
* Main text: dark gray or black.
* Slide titles: navy or teal.
* Normal data points: blue or green.
* Principal component / PC1: orange or teal.
* PC2: purple or gray.
* Anomaly points: red.
* Formulas must be large, clear, and readable.
* Animations should be smooth and not too chaotic.
* Use animations such as `FadeIn`, `FadeOut`, `Write`, `Create`, `Transform`, `ReplacementTransform`, `LaggedStart`, and `GrowArrow`.

Use these color constants:

```python
LIGHT_BG = "#F8FAFC"
NAVY = "#0F172A"
TEAL = "#0F766E"
BLUE = "#2563EB"
GREEN = "#16A34A"
ORANGE = "#EA580C"
RED = "#DC2626"
PURPLE = "#7C3AED"
GRAY_TEXT = "#334155"
LIGHT_GRAY = "#CBD5E1"
```

The lecture should contain around 16 slides.

Slide 1 — Title

Title:
“PCA and Anomaly Detection”

Subtitle:
“From Variance, Covariance, and Eigenvalues to Detecting Outliers”

Visual:

* A light theme background.
* A 2D scatter cloud.
* A translucent ellipse showing the data distribution.
* A long arrow showing the main principal direction.

Animation:

* Fade in the title.
* Fade in the subtitle.
* Create the scatter points.
* Grow the principal direction arrow.

Speaker note:
“In this lecture, we will build the intuition behind PCA and then use it for anomaly detection through reconstruction error.”

Slide 2 — What is PCA?

Title:
“What is PCA?”

On-screen content:

* `PCA = Principal Component Analysis`
* `Finds the directions of maximum variance`
* `Reduces dimensionality while preserving important information`

Visual:

* Left side: short bullet list.
* Right side: a 2D scatter plot stretched along a diagonal direction.
* Show original axes `x_1`, `x_2`.
* Show new axes `PC_1`, `PC_2`.

Animation:

* Show the scatter points.
* Show the original axes.
* Show `PC_1` and `PC_2`.
* Highlight `PC_1` as the most important direction.

Speaker note:
“PCA does not randomly remove features. It finds a smarter coordinate system for the data.”

Slide 3 — Why is PCA Unsupervised Learning?

Title:
“Why is PCA Unsupervised?”

On-screen content:

* `Supervised learning: uses X and y`
* `Unsupervised learning: uses only X`
* `PCA does not need labels`
* `PCA learns the internal structure of data`

Visual:

* Two boxes:

  * `Supervised Learning`
  * `Unsupervised Learning`
* In the supervised box: `X -> y`
* In the unsupervised box: `X -> structure`
* Place `PCA` under the unsupervised learning box.

Animation:

* Show both boxes.
* Show `X -> y` for supervised learning.
* Show `X -> structure` for unsupervised learning.
* Move or fade in PCA inside the unsupervised learning box.

Speaker note:
“PCA belongs to unsupervised learning because it does not use target labels. It only looks at the input data and learns its structure.”

Slide 4 — Simple Intuition: Height and Weight

Title:
“Simple Intuition: Height and Weight”

On-screen content:

* `x = height`
* `y = weight`
* `Taller people often tend to weigh more`
* `2D data can mostly vary along one main direction`

Visual:

* A 2D scatter plot.
* Points lie roughly along an upward diagonal.
* A principal direction arrow along the diagonal.
* Text: `2D -> 1D representation`

Animation:

* Show the points gradually.
* Draw the main direction arrow.
* Project several points onto the main direction.

Speaker note:
“Even though the data lives in two dimensions, most of its variation may happen along only one main direction.”

Slide 5 — Variance

Title:
“Variance: How Spread Out is the Data?”

Formula using MathTex:

```latex
\mathrm{Var}(X)=\frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})^2
```

On-screen explanation:

* `Small variance: points are close together`
* `Large variance: points are spread out`
* `PCA prefers directions with large variance`

Visual:

* Two horizontal number lines.
* Top row: points close together, labeled `Small variance`.
* Bottom row: points spread out, labeled `Large variance`.
* Show the mean on each number line.
* Show distances from points to the mean.

Animation:

* Show the mean.
* Draw distance lines from points to the mean.
* Highlight squared distances.

Speaker note:
“Variance measures how much the data spreads. PCA searches for directions where the variance is maximized.”

Slide 6 — Covariance

Title:
“Covariance: How Two Variables Move Together”

Formula using MathTex:

```latex
\mathrm{Cov}(X,Y)=\frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})
```

On-screen explanation:

* `Positive covariance: variables increase together`
* `Negative covariance: one increases while the other decreases`
* `Near-zero covariance: weak linear relationship`

Visual:
Create three small scatter plots:

1. Positive covariance: upward trend.
2. Negative covariance: downward trend.
3. Near-zero covariance: random circular cloud.

Animation:

* Show the three plots one by one.
* Add labels:

  * `Positive`
  * `Negative`
  * `Near zero`

Speaker note:
“Covariance tells us how two variables change together. PCA uses covariance to understand the shape and orientation of the data.”

Slide 7 — Covariance Matrix

Title:
“Covariance Matrix”

Formula using MathTex:

```latex
\Sigma=
\begin{bmatrix}
\mathrm{Var}(x_1) & \mathrm{Cov}(x_1,x_2) \\
\mathrm{Cov}(x_2,x_1) & \mathrm{Var}(x_2)
\end{bmatrix}
```

On-screen explanation:

* `Diagonal entries: variances`
* `Off-diagonal entries: covariances`
* `The covariance matrix describes the shape of the data`

Visual:

* Show a large covariance matrix in the center.
* Highlight diagonal entries with a soft color.
* Highlight off-diagonal entries with another soft color.
* Add short labels pointing to diagonal and off-diagonal parts.

Animation:

* Write the matrix.
* Highlight the diagonal.
* Highlight the off-diagonal terms.
* Fade in the explanation text.

Speaker note:
“The covariance matrix summarizes both the spread of each feature and the relationship between features.”

Slide 8 — Eigenvalues and Eigenvectors

Title:
“Eigenvalues and Eigenvectors”

Formula using MathTex:

```latex
A\vec{v}=\lambda\vec{v}
```

On-screen explanation:

* `A: covariance matrix`
* `\vec{v}: eigenvector, a special direction`
* `\lambda: eigenvalue, the amount of variance along that direction`

Visual:

* A scatter cloud shaped like an ellipse.
* Two perpendicular arrows:

  * `PC_1`: long arrow.
  * `PC_2`: shorter arrow.
* `PC_1` should be highlighted.

Animation:

* Show the formula.
* Transform or fade from the covariance matrix idea into the ellipse.
* Draw `PC_1`.
* Draw `PC_2`.
* Highlight `PC_1` because it has the larger eigenvalue.

Speaker note:
“In PCA, eigenvectors become the principal directions, and eigenvalues tell us how important those directions are.”

Slide 9 — PCA Algorithm

Title:
“PCA Algorithm”

On-screen flowchart:

1. `Center or standardize the data`
2. `Compute the covariance matrix`
3. `Find eigenvalues and eigenvectors`
4. `Sort eigenvalues in descending order`
5. `Choose the top k principal components`
6. `Project the data onto the new space`

Visual:

* A horizontal flowchart with six boxes.
* Arrows between boxes.

Animation:

* Show each box one by one.
* Highlight the whole pipeline at the end.

Speaker note:
“PCA reduces dimensionality by building a new coordinate system based on the variance structure of the data.”

Slide 10 — Projection

Title:
“Projection: Reducing Dimensionality”

Formula using MathTex:

```latex
Z=XW
```

On-screen explanation:

* `X: original data matrix`
* `W: matrix of selected principal components`
* `Z: lower-dimensional representation`

Visual:

* A 2D scatter plot.
* A line showing `PC_1`.
* Several points projected orthogonally onto `PC_1`.
* Below the plot, show a 1D line with projected points.

Animation:

* Project each point onto `PC_1`.
* Transform the 2D representation into the 1D representation.

Speaker note:
“Once we have the principal components, we project the original data onto them. This gives us a lower-dimensional representation.”

Slide 11 — PCA on Images

Title:
“PCA on Images”

On-screen content:

* `A grayscale image is a matrix of pixel values`
* `An h \times w image can be flattened into a vector of h \cdot w dimensions`
* `PCA can compress this vector into k dimensions`

Formula using MathTex:

```latex
\text{image}\in\mathbb{R}^{h\times w}
\quad\Rightarrow\quad
x\in\mathbb{R}^{hw}
\quad\Rightarrow\quad
z\in\mathbb{R}^{k},\; k\ll hw
```

Visual:

* A small 8x8 image grid.
* Arrow to a vector of length 64.
* Arrow to a compressed vector of length 10.
* Arrow to a reconstructed image grid.

Animation:

* Flatten the image grid into a vector.
* Compress the vector.
* Reconstruct the image grid.

Speaker note:
“An image is just numerical data. PCA can compress the image by keeping only the most important directions of variation.”

Slide 12 — Reconstruction Error

Title:
“Reconstruction Error”

Formulas using MathTex:

```latex
z=W^\top x
```

```latex
\hat{x}=Wz=WW^\top x
```

```latex
\mathrm{error}(x)=\|x-\hat{x}\|_2^2
```

On-screen explanation:

* `x: original input`
* `\hat{x}: reconstructed input`
* `Small error: the input matches the learned PCA structure`
* `Large error: the input may be unusual`

Visual:

* Three columns:

  1. `Original`
  2. `Reconstructed`
  3. `Error`
* Use one normal example with a small error.

Animation:

* Show the original image or point.
* Show the reconstructed version.
* Show the difference.
* Display the reconstruction error value.

Speaker note:
“Reconstruction error measures how much information is lost after projecting and reconstructing the data.”

Slide 13 — What is Anomaly Detection?

Title:
“What is Anomaly Detection?”

On-screen content:

* `An anomaly is a data point that is significantly different from most normal data`
* Examples:

  * `Fraudulent transaction`
  * `Sensor failure`
  * `Corrupted image`
  * `Ship moving on an unusual route`

Visual:

* A dense cluster of normal blue points.
* One or two red points far away from the cluster.

Animation:

* Show normal points.
* Show red anomaly points.
* Draw a warning circle around the anomaly.

Speaker note:
“Anomaly detection aims to find unusual samples. In many cases, labels are unavailable, so it is often treated as an unsupervised learning problem.”

Slide 14 — PCA-Based Anomaly Detection

Title:
“PCA-Based Anomaly Detection”

Pipeline on screen:
`Normal Data -> Fit PCA -> Reconstruct Input -> Compute Reconstruction Error -> Compare with Threshold`

Formula using MathTex:

```latex
\text{If } \|x-\hat{x}\|_2^2>\tau,\quad \text{then } x \text{ is an anomaly}
```

On-screen explanation:

* `PCA learns the structure of normal data`
* `Normal samples are reconstructed well`
* `Anomalous samples are reconstructed poorly`

Visual:

* Flowchart of the pipeline.
* A small bar chart of reconstruction errors.
* A red horizontal threshold line.
* Bars below threshold: normal.
* Bar above threshold: anomaly.

Animation:

* Show the pipeline step by step.
* Show the error bars.
* Draw the threshold line.
* Highlight the bar above the threshold.

Speaker note:
“If the reconstruction error is larger than the threshold, we classify the sample as an anomaly.”

Slide 15 — Full Example

Title:
“Complete Example: From PCA to Anomaly Detection”

Part A: 2D data

* Normal points lie close to a diagonal structure.
* One anomaly lies far from the structure.
* PCA learns `PC_1` from normal data.
* Normal point reconstruction error is small.
* Anomaly reconstruction error is large.

Part B: image data

* A normal digit-like image is reconstructed well.
* A noisy or random image is reconstructed poorly.

Visual:

* Left side: 2D scatter plot with `PC_1` and one red anomaly.
* Right side: image original/reconstructed comparison.

Animation:

* Show normal data.
* Draw `PC_1`.
* Project a normal point.
* Project an anomaly point.
* Show small error versus large error.
* Then show image reconstruction comparison.

Speaker note:
“This is the whole idea: PCA learns the main structure of normal data. A sample that does not follow this structure will have a high reconstruction error.”

Slide 16 — Summary

Title:
“Summary”

On-screen bullets:

* `PCA is a dimensionality reduction method`
* `PCA is unsupervised because it does not require labels`
* `PCA is based on variance, covariance, eigenvalues, and eigenvectors`
* `Eigenvectors define principal directions`
* `Eigenvalues measure the importance of those directions`
* `PCA can compress and reconstruct images`
* `Reconstruction error can be used for anomaly detection`

Final diagram:
`Variance / Covariance -> Covariance Matrix -> Eigenvalues / Eigenvectors -> PCA -> Projection / Reconstruction -> Anomaly Detection`

Animation:

* Show bullets one by one.
* Show the final diagram at the end.

Speaker note:
“If you remember one sentence: PCA finds a smarter coordinate system for the data, and reconstruction error tells us when a new sample does not fit that structure.”

Helper function requirements:
Please create helper functions when suitable:

```python
def make_title(text, subtitle=None):
    ...

def make_bullet_list(items, font_size=30):
    ...

def make_light_axes(x_label, y_label):
    ...

def make_scatter_points(points, color=BLUE):
    ...

def make_principal_axes(center, angle, length1, length2):
    ...

def make_covariance_plots():
    ...

def make_flowchart(labels):
    ...

def make_image_grid(matrix, cell_size=0.25):
    ...

def make_error_bar_chart(errors, threshold):
    ...

def clear_slide(self):
    ...
```

Formula requirements:
Use clear LaTeX strings inside `MathTex`.

Required formulas:

```latex
\mathrm{Var}(X)=\frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})^2
```

```latex
\mathrm{Cov}(X,Y)=\frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})
```

```latex
\Sigma=
\begin{bmatrix}
\mathrm{Var}(x_1) & \mathrm{Cov}(x_1,x_2) \\
\mathrm{Cov}(x_2,x_1) & \mathrm{Var}(x_2)
\end{bmatrix}
```

```latex
A\vec{v}=\lambda\vec{v}
```

```latex
Z=XW
```

```latex
z=W^\top x
```

```latex
\hat{x}=Wz=WW^\top x
```

```latex
\mathrm{error}(x)=\|x-\hat{x}\|_2^2
```

```latex
\text{If } \|x-\hat{x}\|_2^2>\tau,\quad \text{then } x \text{ is an anomaly}
```

Code quality requirements:

* The final code must run as a Manim-Slides deck.
* Use `self.camera.background_color = LIGHT_BG`.
* Make sure all formulas and text fit within the frame.
* Use `.scale()`, `.to_edge()`, `.arrange()`, `.next_to()`, and `.move_to()` carefully.
* Avoid very long text blocks.
* Use visual diagrams and animations instead of heavy paragraphs.
* Use safe fallbacks if optional dependencies are unavailable.
* Make the deck visually polished in light theme.

Expected output:
A complete, runnable Manim-Slides Python file that teaches PCA and PCA-based anomaly detection in English, with clear LaTeX formulas, clean code, good layout, and smooth animations.

read it and implement code in /src 1 slide have 1 .py file. main is import and run. export video 1080p 60fps