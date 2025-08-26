import os
import re
import numpy as np
import cv2
import streamlit as st

# === 複数フォルダのリスト ===
folders = [
    "/Users/nemo/学研画像/adc",
    "/Users/nemo/学研画像/dwi",
    "/Users/nemo/学研画像/flair",
    "/Users/nemo/学研画像/swi",
    "/Users/nemo/学研画像/tof"
]

# 数字を考慮したソート関数
def sorted_nicely(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

st.title("画像viewer")

# === フォルダごとにスライダーと画像を配置 ===
for folder in folders:
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg','.jpeg','.png'))]
    files = sorted_nicely(files)

    if not files:
        st.warning(f"⚠️ フォルダ {folder} にJPEGがありません")
        continue

    # 画像を読み込み & 正規化
    images = []
    for f in files:
        img = cv2.imread(os.path.join(folder, f), cv2.IMREAD_GRAYSCALE)
        arr = img.astype(float)
        arr = (arr - arr.min()) / (arr.max() - arr.min())
        images.append(arr)

    images = np.array(images)

    # === フォルダ名を見出しにして表示 ===
    st.subheader(f"{os.path.basename(folder)}")

    # スライダー
    idx = st.slider(
        f"Slice ({os.path.basename(folder)})",
        0, len(images)-1, 0,
        key=f"slider_{os.path.basename(folder)}"  # ← key をつけるのがポイント！
    )

    # 表示（forループの中に入れる）
    st.image(
        images[idx],
        caption=f"Slice {idx}",
        use_container_width=True,
        clamp=True
    )