"""Generate architecture and flow diagrams for the NASA Image Puller README."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ---------------------------------------------------------------------------
# Style constants
# ---------------------------------------------------------------------------
BG_COLOR = "#0d1117"
CARD_COLOR = "#161b22"
BORDER_COLOR = "#30363d"
ACCENT_BLUE = "#58a6ff"
ACCENT_GREEN = "#3fb950"
ACCENT_ORANGE = "#d29922"
ACCENT_RED = "#f85149"
ACCENT_PURPLE = "#bc8cff"
TEXT_COLOR = "#e6edf3"
TEXT_DIM = "#8b949e"
ARROW_COLOR = "#58a6ff"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "Arial", "Helvetica", "DejaVu Sans"],
    "text.color": TEXT_COLOR,
    "axes.facecolor": BG_COLOR,
    "figure.facecolor": BG_COLOR,
})


def rounded_box(ax, x, y, w, h, label, sublabel=None, color=ACCENT_BLUE,
                fontsize=11, sublabel_size=8):
    """Draw a rounded rectangle with a label and optional sublabel."""
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.12",
        facecolor=CARD_COLOR,
        edgecolor=color,
        linewidth=1.8,
    )
    ax.add_patch(box)
    ax.text(x, y + (0.06 if sublabel else 0), label,
            ha="center", va="center", fontsize=fontsize,
            fontweight="bold", color=color, zorder=5)
    if sublabel:
        ax.text(x, y - 0.14, sublabel,
                ha="center", va="center", fontsize=sublabel_size,
                color=TEXT_DIM, style="italic", zorder=5)


def arrow(ax, x1, y1, x2, y2, color=ARROW_COLOR, style="-|>"):
    """Draw a curved arrow between two points."""
    a = FancyArrowPatch(
        (x1, y1), (x2, y2),
        connectionstyle="arc3,rad=0.0",
        arrowstyle=style,
        color=color,
        linewidth=1.6,
        mutation_scale=14,
        zorder=3,
    )
    ax.add_patch(a)


# ========================================================================
# 1. Architecture diagram
# ========================================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.set_xlim(-0.5, 4.5)
ax.set_ylim(-0.5, 3.5)
ax.axis("off")

ax.text(2.0, 3.25, "Architecture Overview", ha="center", va="center",
        fontsize=16, fontweight="bold", color=TEXT_COLOR)

# Boxes
rounded_box(ax, 0.6, 2.2, 1.0, 0.7, "main.py", "entry point", ACCENT_GREEN)
rounded_box(ax, 2.0, 2.2, 1.1, 0.7, "input_handler", "prompts & scoring", ACCENT_BLUE)
rounded_box(ax, 3.5, 2.2, 1.2, 0.7, "connection_handler", "API & downloads", ACCENT_ORANGE)
rounded_box(ax, 2.0, 0.8, 1.0, 0.7, "globals", "config & errors", ACCENT_PURPLE)

# External
rounded_box(ax, 0.6, 0.8, 1.0, 0.55, "User (CLI)", None, TEXT_DIM, fontsize=10)
rounded_box(ax, 3.5, 0.8, 1.0, 0.55, "NASA APOD\nAPI", None, ACCENT_RED, fontsize=10)

# Arrows
arrow(ax, 1.15, 2.2, 1.40, 2.2)       # main -> input_handler
arrow(ax, 2.60, 2.2, 2.85, 2.2)       # input_handler -> connection_handler
arrow(ax, 2.0, 1.85, 2.0, 1.20)       # globals up
arrow(ax, 0.6, 1.85, 0.6, 1.12)       # user -> main
arrow(ax, 3.5, 1.85, 3.5, 1.12)       # connection_handler -> nasa api
arrow(ax, 1.10, 1.95, 1.55, 1.20, color=ACCENT_PURPLE, style="-|>")  # main -> globals
arrow(ax, 2.90, 1.95, 2.45, 1.20, color=ACCENT_PURPLE, style="-|>")  # conn -> globals

fig.tight_layout(pad=0.5)
fig.savefig("docs/images/architecture.png", dpi=180, bbox_inches="tight",
            facecolor=BG_COLOR, edgecolor="none")
plt.close(fig)
print("Saved docs/images/architecture.png")

# ========================================================================
# 2. Pipeline / flow diagram
# ========================================================================
fig, ax = plt.subplots(figsize=(10, 3.5))
ax.set_xlim(-0.3, 5.3)
ax.set_ylim(-0.2, 2.0)
ax.axis("off")

ax.text(2.5, 1.8, "Query Pipeline", ha="center", va="center",
        fontsize=16, fontweight="bold", color=TEXT_COLOR)

steps = [
    ("Prompt\nUser", ACCENT_GREEN),
    ("Build\nAPI URL", ACCENT_BLUE),
    ("Fetch\nAPOD Data", ACCENT_ORANGE),
    ("Score &\nRank", ACCENT_PURPLE),
    ("Download\nImages", ACCENT_RED),
]

xs = np.linspace(0.3, 4.7, len(steps))
y = 0.75

for i, (label, color) in enumerate(steps):
    rounded_box(ax, xs[i], y, 0.85, 0.7, label, color=color, fontsize=10)
    if i < len(steps) - 1:
        arrow(ax, xs[i] + 0.48, y, xs[i + 1] - 0.48, y)

# Step numbers
for i, x in enumerate(xs):
    ax.text(x, y - 0.55, f"Step {i + 1}", ha="center", va="center",
            fontsize=8, color=TEXT_DIM)

fig.tight_layout(pad=0.5)
fig.savefig("docs/images/pipeline.png", dpi=180, bbox_inches="tight",
            facecolor=BG_COLOR, edgecolor="none")
plt.close(fig)
print("Saved docs/images/pipeline.png")

# ========================================================================
# 3. Scoring visualisation (simulated)
# ========================================================================
fig, ax = plt.subplots(figsize=(8, 4))

# Simulated scoring data for a query about "nebula"
entries = [
    "Crab Nebula Mosaic", "Horsehead Nebula", "Orion Deep Field",
    "Mars Opposition", "Saturn's Rings", "Andromeda Galaxy",
    "Solar Eclipse", "ISS Transit", "Lunar Surface", "Eagle Nebula"
]
scores = [14, 11, 7, 2, 1, 5, 0, 0, 1, 12]

# Sort by score descending
pairs = sorted(zip(scores, entries), reverse=True)
scores_s = [p[0] for p in pairs]
entries_s = [p[1] for p in pairs]

colors = []
for i, s in enumerate(scores_s):
    if i == 0:
        colors.append(ACCENT_GREEN)
    elif i == 1:
        colors.append(ACCENT_BLUE)
    else:
        colors.append(BORDER_COLOR)

bars = ax.barh(range(len(entries_s)), scores_s, color=colors, edgecolor="none", height=0.65)
ax.set_yticks(range(len(entries_s)))
ax.set_yticklabels(entries_s, fontsize=9, color=TEXT_COLOR)
ax.invert_yaxis()
ax.set_xlabel("Relevance Score (word matches)", fontsize=10, color=TEXT_DIM)
ax.set_title("Query Scoring Example: \"nebula\"", fontsize=13, fontweight="bold",
             color=TEXT_COLOR, pad=12)

# Annotate top 2
ax.text(scores_s[0] + 0.3, 0, "image1.jpg", va="center", fontsize=9,
        color=ACCENT_GREEN, fontweight="bold")
ax.text(scores_s[1] + 0.3, 1, "image2.jpg", va="center", fontsize=9,
        color=ACCENT_BLUE, fontweight="bold")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_color(BORDER_COLOR)
ax.spines["left"].set_color(BORDER_COLOR)
ax.tick_params(colors=TEXT_DIM, which="both")
ax.set_facecolor(BG_COLOR)
fig.set_facecolor(BG_COLOR)

fig.tight_layout(pad=1.0)
fig.savefig("docs/images/scoring_example.png", dpi=180, bbox_inches="tight",
            facecolor=BG_COLOR, edgecolor="none")
plt.close(fig)
print("Saved docs/images/scoring_example.png")
