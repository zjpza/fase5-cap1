"""Gera `arquitetura_ir_alem.png` (e .svg) com layout espaçado.

Pipeline: ESP32 (Wokwi) -> Wi-Fi -> API FastAPI -> Pipeline sklearn -> Resposta Serial.
"""
from __future__ import annotations

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Paleta (caixas) - cores suaves com borda mais escura
BOXES = {
    "esp32":   {"fc": "#D7F5DD", "ec": "#2E8B57"},  # verde
    "wifi":    {"fc": "#FCF3CF", "ec": "#C9A227"},  # amarelo
    "api":     {"fc": "#CFE8FB", "ec": "#2A6FB0"},  # azul
    "pipe":    {"fc": "#E4D4F4", "ec": "#7B4FB0"},  # roxo
    "resp":    {"fc": "#FBD4D4", "ec": "#B03A3A"},  # vermelho
}
NODES = [
    ("esp32", 14, 72, 24, 28,
     ["ESP32 (Wokwi)", "", "DHT22: T + UR", "Sensor de chuva (ADC)", "", "q = f(T, UR)"]),
    ("wifi",  44, 72, 20, 18,
     ["Wi-Fi", "", "HTTP POST JSON"]),
    ("api",   74, 72, 24, 24,
     ["API FastAPI", "(Issue #3)", "", "POST /predict", "GET /health"]),
    ("pipe",  104, 72, 22, 28,
     ["Pipeline sklearn", "", "health_classifier.pkl", "",
      "RandomForestClassifier", "+ ColumnTransformer"]),
    ("resp",  104, 22, 24, 24,
     ["Resposta no Serial", "", '"Saudável" / "Não Saudável"', "", "(confiança)"]),
]

# Setas: (de, para, label, offset_label_y, estilo)
EDGES = [
    ("esp32", "wifi",  "{crop, precipitation,\nspecific_humidity,\nrelative_humidity, temperature}", 0.10),
    ("wifi",  "api",   None, 0.0),
    ("api",  "pipe",  "features PT-BR", 0.10),
    ("pipe", "resp",  "health | confidence", 0.0),
]


def draw_node(ax, key, cx, cy, w, h, lines, fontsize=10.5):
    style = BOXES[key]
    box = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.6,rounding_size=2.2",
        linewidth=2.0, facecolor=style["fc"], edgecolor=style["ec"],
    )
    ax.add_patch(box)
    # Texto centralizado, multilinha, com respiro vertical
    ax.text(cx, cy, "\n".join(lines), ha="center", va="center",
            fontsize=fontsize, color="#1a1a1a", linespacing=1.7)
    return (cx, cy, w, h)


def edge_points(nodes, frm, to):
    """Pontos de borda para a seta (sai da lateral direita, entra na lateral esquerda)."""
    fx, fy, fw, fh = nodes[frm]
    tx, ty, tw, th = nodes[to]
    if abs(fy - ty) < 1e-6:  # mesmo nivel: horizontal direita -> esquerda
        return (fx + fw / 2, fy), (tx - tw / 2, ty)
    # descida vertical: sai do fundo do no origem, entra no topo do destino
    return (fx, fy - fh / 2), (tx, ty + th / 2)


def main():
    fig, ax = plt.subplots(figsize=(18, 9.5), dpi=150)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Titulo (centralizado no novo xlim 0..120)
    ax.text(60, 95,
            'Arquitetura — Ir Além Opção 1: ESP32 (Wokwi) → API → Classificador de Saúde',
            ha="center", va="center", fontsize=15, fontweight="bold", color="#111")
    placed = {}
    for key, cx, cy, w, h, lines in NODES:
        placed[key] = draw_node(ax, key, cx, cy, w, h, lines)

    for frm, to, label, dy in EDGES:
        (x0, y0), (x1, y1) = edge_points(placed, frm, to)
        arrow = FancyArrowPatch(
            (x0, y0), (x1, y1),
            arrowstyle="-|>", mutation_scale=22,
            linewidth=1.8, color="#333", shrinkA=2, shrinkB=2,
        )
        ax.add_patch(arrow)
        if label:
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + dy * 10
            ax.text(mx, my, label, ha="center", va="center", fontsize=9.5,
                    color="#222", linespacing=1.5,
                    bbox=dict(boxstyle="round,pad=0.35", fc="white",
                              ec="#bbb", alpha=0.9))

    plt.subplots_adjust(left=0.02, right=0.98, top=0.96, bottom=0.04)
    fig.savefig("arquitetura_ir_alem.png", dpi=150, bbox_inches="tight",
                facecolor="white")
    fig.savefig("arquitetura_ir_alem.svg", bbox_inches="tight", facecolor="white")
    print("OK: arquitetura_ir_alem.png + .svg gerados")


if __name__ == "__main__":
    main()