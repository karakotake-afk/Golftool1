import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

# ページ全体の基本設定
st.set_page_config(
    page_title="ゴルフクラブ 重量・長さフロー分析ツール",
    page_icon="⛳",
    layout="wide",
)

st.title("⛳ ゴルフクラブ 重量・長さフロー管理ツール")
st.write(
    "1Wと特定の番手（5I / 9I / PW / 最短クラブ）の2点を通る基準線を引いて、セッティング全体のフローバランスを検証します。"
)

# -----------------------------------------------------------------------------
# 1. 初期セッティングデータ
# -----------------------------------------------------------------------------
default_data = [
    {
        "No": 1,
        "番手": "1W",
        "モデル": "TSR2",
        "長さ(inch)": 45.25,
        "総重量(g)": 308.0,
        "シャフト重量(g)": 60.0,
        "全体重心長(mm)": 880.0,
        "CG垂線交点長(mm)": 1120.0,
    },
    {
        "No": 2,
        "番手": "3W",
        "モデル": "TSR2",
        "長さ(inch)": 43.00,
        "総重量(g)": 326.0,
        "シャフト重量(g)": 65.0,
        "全体重心長(mm)": 835.0,
        "CG垂線交点長(mm)": 1060.0,
    },
    {
        "No": 3,
        "番手": "5W",
        "モデル": "TSR2",
        "長さ(inch)": 42.50,
        "総重量(g)": 332.0,
        "シャフト重量(g)": 67.0,
        "全体重心長(mm)": 825.0,
        "CG垂線交点長(mm)": 1045.0,
    },
    {
        "No": 4,
        "番手": "4U",
        "モデル": "TSR2 Utility",
        "長さ(inch)": 39.50,
        "総重量(g)": 362.0,
        "シャフト重量(g)": 91.0,
        "全体重心長(mm)": 768.0,
        "CG垂線交点長(mm)": 970.0,
    },
    {
        "No": 5,
        "番手": "5I",
        "モデル": "T100S",
        "長さ(inch)": 38.00,
        "総重量(g)": 408.0,
        "シャフト重量(g)": 105.0,
        "全体重心長(mm)": 740.0,
        "CG垂線交点長(mm)": 935.0,
    },
    {
        "No": 6,
        "番手": "6I",
        "モデル": "T100S",
        "長さ(inch)": 37.50,
        "総重量(g)": 415.0,
        "シャフト重量(g)": 105.0,
        "全体重心長(mm)": 730.0,
        "CG垂線交点長(mm)": 922.0,
    },
    {
        "No": 7,
        "番手": "7I",
        "モデル": "T100S",
        "長さ(inch)": 37.00,
        "総重量(g)": 422.0,
        "シャフト重量(g)": 105.0,
        "全体重心長(mm)": 720.0,
        "CG垂線交点長(mm)": 910.0,
    },
    {
        "No": 8,
        "番手": "8I",
        "モデル": "T100S",
        "長さ(inch)": 36.50,
        "総重量(g)": 430.0,
        "シャフト重量(g)": 105.0,
        "全体重心長(mm)": 710.0,
        "CG垂線交点長(mm)": 897.0,
    },
    {
        "No": 9,
        "番手": "9I",
        "モデル": "T100S",
        "長さ(inch)": 36.00,
        "総重量(g)": 438.0,
        "シャフト重量(g)": 105.0,
        "全体重心長(mm)": 700.0,
        "CG垂線交点長(mm)": 885.0,
    },
    {
        "No": 10,
        "番手": "PW",
        "モデル": "T100S",
        "長さ(inch)": 35.75,
        "総重量(g)": 446.0,
        "シャフト重量(g)": 105.0,
        "全体重心長(mm)": 695.0,
        "CG垂線交点長(mm)": 878.0,
    },
    {
        "No": 11,
        "番手": "50°",
        "モデル": "Vokey SM9",
        "長さ(inch)": 35.50,
        "総重量(g)": 453.0,
        "シャフト重量(g)": 105.0,
        "全体重心長(mm)": 690.0,
        "CG垂線交点長(mm)": 872.0,
    },
    {
        "No": 12,
        "番手": "56°",
        "モデル": "Vokey SM9",
        "長さ(inch)": 35.25,
        "総重量(g)": 460.0,
        "シャフト重量(g)": 105.0,
        "全体重心長(mm)": 685.0,
        "CG垂線交点長(mm)": 865.0,
    },
]

# -----------------------------------------------------------------------------
# 2. サイドバーでの操作・設定
# -----------------------------------------------------------------------------
st.sidebar.header("📂 データ操作 / 設定")

uploaded_file = st.sidebar.file_uploader(
    "CSVファイルを読み込む", type=["csv"]
)

if uploaded_file is not None:
    df_input = pd.read_csv(uploaded_file)
else:
    df_input = pd.DataFrame(default_data)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 基準線の対象番手選択")
st.sidebar.caption("1W固定。もう一つの基準となるポイントを選択してください。")

# -----------------------------------------------------------------------------
# 3. 画面レイアウト（GUI入力欄 & グラフ）
# -----------------------------------------------------------------------------
col_editor, col_chart = st.columns([1, 1.2])

with col_editor:
    st.subheader("📋 スペック入力・編集")

    edited_df = st.data_editor(
        df_input,
        num_rows="dynamic",
        column_config={
            "長さ(inch)": st.column_config.NumberColumn(
                format="%.2f", min_value=30.0, max_value=50.0
            ),
            "総重量(g)": st.column_config.NumberColumn(
                format="%d", min_value=200, max_value=600
            ),
            "全体重心長(mm)": st.column_config.NumberColumn(
                format="%.1f", min_value=500.0, max_value=1200.0
            ),
            "シャフト重量(g)": st.column_config.NumberColumn(
                format="%.1f", min_value=40.0, max_value=150.0
            ),
            "CG垂線交点長(mm)": st.column_config.NumberColumn(
                format="%.1f", min_value=700.0, max_value=1300.0
            ),
        },
        use_container_width=True,
    )

    csv_data = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="💾 現在のセッティングをCSVで保存",
        data=csv_data,
        file_name="golf_club_flow_data.csv",
        mime="text/csv",
    )

    if st.button("🌐 ブラウザ（LocalStorage）に保存"):
        json_str = edited_df.to_json(orient="records")
        save_js = f"""
        <script>
            localStorage.setItem('golf_club_flow_2p', '{json_str}');
            alert('データをブラウザに保存しました！');
        </script>
        """
        components.html(save_js, height=0)

with col_chart:
    st.subheader("📊 重量フロー分析グラフ")

    if not edited_df.empty:
        plot_df = edited_df.dropna(
            subset=["長さ(inch)", "総重量(g)"]
        ).copy()

        # 1Wと候補番手（5I, 9I, PW, 一番短いクラブ）の検出
        w1_row = plot_df[plot_df["番手"] == "1W"]

        # 一番短いクラブ（長さの最小値を持つ行）を判定
        shortest_idx = plot_df["長さ(inch)"].idxmin()
        shortest_club_name = plot_df.loc[shortest_idx, "番手"]

        # 選択肢のリストを作成
        target_options = []
        if "5I" in plot_df["番手"].values:
            target_options.append("5I")
        if "9I" in plot_df["番手"].values:
            target_options.append("9I")
        if "PW" in plot_df["番手"].values:
            target_options.append("PW")

        # 「一番短いクラブ」ラベルの追加（重複防止）
        shortest_label = f"一番短いクラブ ({shortest_club_name})"
        if shortest_label not in target_options:
            target_options.append(shortest_label)

        # サイドバーで対象を選択
        selected_target_label = st.sidebar.radio(
            "1Wと繋ぐ選択肢:", target_options
        )

        # 選択された実際の番手名を特定
        if "一番短いクラブ" in selected_target_label:
            selected_target = shortest_club_name
        else:
            selected_target = selected_target_label

        target_row = plot_df[plot_df["番手"] == selected_target]

        # 散布図作成
        fig = px.scatter(
            plot_df,
            x="長さ(inch)",
            y="総重量(g)",
            text="番手",
            hover_data=["モデル", "シャフト重量(g)"],
        )

        # 2点を通る直線（1W と 選択された番手）の計算と表示
        if not w1_row.empty and not target_row.empty:
            x1 = w1_row["長さ(inch)"].values[0]
            y1 = w1_row["総重量(g)"].values[0]
            x2 = target_row["長さ(inch)"].values[0]
            y2 = target_row["総重量(g)"].values[0]

            if x1 != x2:
                # 2点を通る直線の傾き (slope) と切片 (intercept)
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - slope * x1

                # 全データの範囲をカバーする直線のX座標を設定
                x_range = np.linspace(
                    plot_df["長さ(inch)"].min(), plot_df["長さ(inch)"].max(), 100
                )
                y_range = slope * x_range + intercept

                # 直線を描画
                fig.add_trace(
                    go.Scatter(
                        x=x_range,
                        y=y_range,
                        mode="lines",
                        name=f"基準線 (1W - {selected_target})",
                        line=dict(color="red", width=2, dash="dash"),
                    )
                )

                # 基準となる2つの点をハイライト表示
                fig.add_trace(
                    go.Scatter(
                        x=[x1, x2],
                        y=[y1, y2],
                        mode="markers",
                        name="基準2点",
                        marker=dict(size=16, color="red", symbol="circle-open"),
                        showlegend=False,
                    )
                )

        # 軸反転設定
        fig.update_xaxes(autorange="reversed", title="クラブの長さ (inch)")
        fig.update_yaxes(title="クラブ総重量 (g)")

        fig.update_traces(
            selector=dict(mode="markers+text"),
            textposition="top center",
            marker=dict(size=12, color="#1F497D", symbol="circle"),
            textfont=dict(size=11, family="Arial", color="black"),
        )

        fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            height=500,
            hovermode="closest",
            showlegend=True,
        )

        st.plotly_chart(fig, use_container_width=True)

        # 注記メッセージの表示
        st.info(
            "ℹ️ **注記:** 長さはグリップエンドからヘッドCG heightのシャフト側延長との交点までの長さ。"
            "不明なら1Wはクラブ長より -1.1 inch、FWは -0.8 inch、UTは -0.75 inch、"
            "アイアンは -0.65 inch、ウェッジは無視"
        )
    else:
        st.warning("データが入力されていません。")