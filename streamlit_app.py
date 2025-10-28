# Dreamy Blue Star Poster — Streamlit (matplotlib only)
# Author: You :)
# Description: Generate dreamy, low-saturation blue star posters with soft shadows,
# gradient background, stardust, and aurora glow. Everything is rendered via matplotlib.

import random, math, colorsys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.transforms import Affine2D
import streamlit as st

# -------------------- 配色：低饱和度梦幻蓝系 --------------------
def pastel_blue_palette(k=10, hue_center=0.58, hue_spread=0.07,
                        s_range=(0.10, 0.24), l_range=(0.78, 0.90)):
    cols = []
    hues = np.linspace(hue_center - hue_spread, hue_center + hue_spread, k, endpoint=True)
    hues = (hues + np.random.uniform(-0.01, 0.01, size=k)) % 1.0
    for h in hues:
        s = np.random.uniform(*s_range)
        l = np.random.uniform(*l_range)
        r, g, b = colorsys.hls_to_rgb(h, l, s)   # colorsys: H,L,S
        cols.append((r, g, b))
    return cols

# -------------------- 五角星形状 --------------------
def star_shape(center=(0.5, 0.5), r_outer=0.25, r_inner=None, points=5, rotation=0):
    if r_inner is None:
        r_inner = r_outer * 0.4
    angles = np.linspace(0, 2 * math.pi, points * 2, endpoint=False) + rotation
    radii  = np.array([r_outer if i % 2 == 0 else r_inner for i in range(points * 2)])
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return np.column_stack((x, y))

# -------------------- 背景（渐变/纯色 可切换） --------------------
def draw_background(ax, mode="gradient",
                    top_color=(0.93, 0.96, 0.985),
                    bottom_color=(0.77, 0.86, 0.95),
                    solid_color=(0.95, 0.97, 0.985)):
    if mode == "solid":
        ax.set_facecolor(solid_color)
        return
    # 垂直渐变
    ax.set_facecolor((1,1,1,0))
    grad = np.linspace(0, 1, 800)
    grad = np.vstack([grad, grad])
    cmap = LinearSegmentedColormap.from_list("dreamy_blue", [top_color, bottom_color])
    ax.imshow(grad.T, extent=[0,1,0,1], origin='lower', cmap=cmap, zorder=0, aspect='auto')

# -------------------- 极光柔光（半透明高斯云） --------------------
def add_aurora(ax, n=4,
               hue_center=0.58, hue_spread=0.10,
               alpha_range=(0.06, 0.14),
               size_range=((0.25, 0.55), (0.12, 0.35))):
    for _ in range(n):
        # 颜色：同样是低饱和蓝青/蓝紫
        h = (hue_center + np.random.uniform(-hue_spread, hue_spread)) % 1.0
        s = np.random.uniform(0.06, 0.16)
        l = np.random.uniform(0.82, 0.92)
        col = colorsys.hls_to_rgb(h, l, s)

        # 生成二维高斯
        rx = np.random.uniform(*size_range[0])
        ry = np.random.uniform(*size_range[1])
        cx, cy = np.random.uniform(0.05,0.95), np.random.uniform(0.10,0.90)
        theta  = np.random.uniform(0, np.pi)

        # 在局部网格上画高斯，再通过仿射变换旋转/缩放/平移
        res = 250
        x = np.linspace(-1, 1, res)
        y = np.linspace(-1, 1, res)
        X, Y = np.meshgrid(x, y)
        G = np.exp(-( (X**2)/(2*0.35**2) + (Y**2)/(2*0.9**2) ))  # 椭圆拉伸
        A = (G - G.min())/(G.max()-G.min()+1e-9)
        alpha = np.random.uniform(*alpha_range)

        trans = (Affine2D()
                 .scale(rx, ry)
                 .rotate(theta)
                 .translate(cx, cy) + ax.transData)

        ax.imshow(A, extent=[-1,1,-1,1], origin='lower',
                  transform=trans, zorder=1,
                  cmap=LinearSegmentedColormap.from_list("a", [(1,1,1,0), (*col,1)]),
                  alpha=alpha, interpolation='bilinear')

# -------------------- 星尘（小亮点） --------------------
def add_stardust(ax, n_points=400):
    xs = np.random.uniform(0,1,n_points)
    ys = np.random.uniform(0,1,n_points)
    sizes = np.random.uniform(2, 9, n_points)  # 点大小
    alphas = np.random.uniform(0.08, 0.35, n_points)
    # 白/淡蓝随机
    cols = np.ones((n_points,4))
    cols[:, :3] = np.array([0.97, 0.98, 1.0])
    cols[:, 3] = alphas
    ax.scatter(xs, ys, s=sizes, c=cols, marker='o', linewidths=0, zorder=2)

# -------------------- 主绘制 --------------------
def draw_star_poster(seed=None, n_stars=14, bg_mode="gradient",
                     fig_size=(7,10), title_on=True):
    # 随机：不传 seed 就每次不同；也可以传整数复现
    if seed is not None and seed != "":
        try:
            seed_val = int(seed)
        except:
            seed_val = None
    else:
        seed_val = None

    if seed_val is not None:
        random.seed(seed_val); np.random.seed(seed_val)
    else:
        random.seed(); np.random.seed(None)

    fig = plt.figure(figsize=fig_size)
    ax = plt.gca()
    ax.set_aspect('equal')
    ax.axis('off')

    # 背景
    draw_background(ax, mode=bg_mode)

    # 极光柔光 + 星尘（先铺氛围）
    add_aurora(ax, n=np.random.randint(3,6))
    add_stardust(ax, n_points=np.random.randint(280, 480))

    # 颜色池（全是低饱和淡蓝）
    palette = pastel_blue_palette(12)

    # 五角星 + 柔和阴影
    for i in range(n_stars):
        cx, cy = np.random.uniform(0.07, 0.93), np.random.uniform(0.08, 0.92)
        # 大中小层次
        if i < 3:
            size = np.random.uniform(0.17, 0.25)
        elif i < 8:
            size = np.random.uniform(0.11, 0.17)
        else:
            size = np.random.uniform(0.07, 0.11)

        rotation = np.random.uniform(0, 2*np.pi)
        coords = star_shape(center=(cx, cy), r_outer=size, rotation=rotation)

        # 阴影（轻微移位 + 柔和透明）
        shadow = Polygon(coords - np.array([0.012, 0.012]),
                         closed=True, facecolor=(0.2,0.25,0.35), alpha=0.12,
                         edgecolor='none', zorder=3)
        ax.add_patch(shadow)

        # 主体星星
        color = random.choice(palette)
        alpha = np.random.uniform(0.26, 0.72)
        star = Polygon(coords, closed=True, facecolor=color, alpha=alpha,
                       edgecolor='none', zorder=4)
        ax.add_patch(star)

        # 轻微柔光描边（可选，增加梦幻感）
        glow = Polygon(coords*1.01 - (coords.mean(axis=0)-np.array([cx,cy]))*0.01,
                       closed=True, facecolor=(1,1,1), alpha=0.1,
                       edgecolor='none', zorder=5)
        ax.add_patch(glow)

    if title_on:
        ax.text(0.06, 0.955, "Generative Poster", fontsize=18, weight='bold',
                color=(0.15,0.18,0.22), transform=ax.transAxes, zorder=6)
        ax.text(0.06, 0.915, "Week 9 • Arts & Advanced Big Data", fontsize=11,
                color=(0.25,0.30,0.36), transform=ax.transAxes, zorder=6)

    ax.set_xlim(0,1); ax.set_ylim(0,1)
    plt.tight_layout()
    return fig

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="Dreamy Blue Star Poster", page_icon="⭐", layout="centered")
st.title("Dreamy Blue Star Poster ⭐")
st.caption("Matplotlib only · stars + soft shadows + gradient background + stardust + aurora glow")

with st.sidebar:
    st.header("Controls")
    n_stars = st.slider("Number of stars", 5, 40, 14, 1)
    bg_mode = st.selectbox("Background", ["gradient", "solid"], index=0)
    title_on = st.toggle("Show title", value=True)
    fig_w = st.slider("Figure width (inches)", 4.0, 10.0, 7.0, 0.5)
    fig_h = st.slider("Figure height (inches)", 6.0, 14.0, 10.0, 0.5)
    seed = st.text_input("Seed (leave blank for random)", value="")
    rerun = st.button("🔀 Randomize now")

# Draw figure
fig = draw_star_poster(seed=seed if seed != "" else None,
                       n_stars=n_stars, bg_mode=bg_mode,
                       fig_size=(fig_w, fig_h), title_on=title_on)

st.pyplot(fig, clear_figure=True, use_container_width=False)

# Download the figure
import io
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0.05)
st.download_button("⬇️ Download PNG (300 DPI)", data=buf.getvalue(), file_name="dreamy_star_poster.png", mime="image/png")
