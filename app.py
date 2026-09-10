import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

# ページ全体の基本設定
st.set_page_config(
    page_title="ゴルフクラブ スペック＆重心フロー分析ツール",
    page_icon="⛳",
    layout="wide",
)

st.title("⛳ ゴルフクラブ スペック＆全体重心フロー管理ツール")
st.write(
    "1W〜ウェッジまでの長さ・総重量・全体の重心位置（グリップエンドからの釣り合い点）を入力し、重量および重心フローの相関関係を可視化します。"
)

# -----------------------------------------------------------------------------
# 1. 初期セッティングデータ（1W〜56°：全体重心長を追加）
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
# 2. サイドバーでのファイル操作
# -----------------------------------------------------------------------------
st.sidebar.header("📂 データ操作 / 管理")
uploaded_file = st.sidebar.file_uploader(
    "CSVファイルを読み込む", type=["csv"]
)

if uploaded_file is not None:
    df_input = pd.read_csv(uploaded_file)
else:
    df_input = pd.DataFrame(default_data)

# -----------------------------------------------------------------------------
# 3. 画面レイアウト（GUI入力欄 & 複数グラフ表示）
# -----------------------------------------------------------------------------
col_editor, col_chart = st.columns([1, 1.2])

with col_editor:
    st.subheader("📋 スペック入力・編集")
    st.info(
        "💡 「全体重心長(mm)」（グリップエンドからの釣り合い点）を入力・更新できます。"
    )

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

    # CSV保存機能
    csv_data = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="💾 現在のセッティングをCSVで保存",
        data=csv_data,
        file_name="golf_club_full_cg_specs.csv",
        mime="text/csv",
    )

    # LocalStorage保存機能
    if st.button("🌐 ブラウザ（LocalStorage）に保存"):
        json_str = edited_df.to_json(orient="records")
        save_js = f"""
        <script>
            localStorage.setItem('golf_club_cg_flow_v2', '{json_str}');
            alert('全体重心長含むデータをブラウザに保存しました！');
        </script>
        """
        components.html(save_js, height=0)

with col_chart:
    st.subheader("📊 多次元スペック分析グラフ")

    if not edited_df.empty:
        plot_df = edited_df.dropna(subset=["長さ(inch)", "総重量(g)"])

        # タブによるグラフ切り替え（全体重心長を追加）
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "⚖️ 総重量フロー",
                "📐 全体重心長フロー",
                "🎯 CG垂線交点長",
                "🪵 シャフト重量",
            ]
        )

        # 【TAB 1】 総重量フロー（2次曲線モデル）
        with tab1:
            fig1 = px.scatter(
                plot_df,
                x="長さ(inch)",
                y="総重量(g)",
                text="番手",
                hover_data=["モデル", "全体重心長(mm)"],
            )

            if len(plot_df) >= 3:
                x_data = plot_df["長さ(inch)"].values
                y_data = plot_df["総重量(g)"].values
                coefs = np.polyfit(x_data, y_data, 2)
                x_curve = np.linspace(x_data.min(), x_data.max(), 100)
                y_curve = np.polyval(coefs, x_curve)

                fig1.add_trace(
                    go.Scatter(
                        x=x_curve,
                        y=y_curve,
                        mode="lines",
                        name="理論2次曲線",
                        line=dict(color="red", width=2, dash="dash"),
                    )
                )

            fig1.update_xaxes(
                autorange="reversed", title="クラブの長さ (inch)"
            )
            fig1.update_yaxes(title="クラブ総重量 (g)")
            fig1.update_traces(
                selector=dict(mode="markers+text"),
                textposition="top center",
                marker=dict(size=12, color="#1F497D", symbol="circle"),
            )
            fig1.update_layout(
                margin=dict(l=20, r=20, t=30, b=20), height=450
            )
            st.plotly_chart(fig1, use_container_width=True)

        # 【TAB 2】 グリップエンド〜全体重心長フロー
        with tab2:
            if "全体重心長(mm)" in plot_df.columns:
                fig2 = px.scatter(
                    plot_df,
                    x="長さ(inch)",
                    y="全体重心長(mm)",
                    text="番手",
                    hover_data=["モデル", "総重量(g)"],
                )

                if len(plot_df) >= 3:
                    x_data = plot_df["長さ(inch)"].values
                    y_cg = plot_df["全体重心長(mm)"].values
                    coefs_cg = np.polyfit(x_data, y_cg, 1)  # 1次直線
                    x_curve_cg = np.linspace(x_data.min(), x_data.max(), 100)
                    y_curve_cg = np.polyval(coefs_cg, x_curve_cg)

                    fig2.add_trace(
                        go.Scatter(
                            x=x_curve_cg,
                            y=y_curve_cg,
                            mode="lines",
                            name="理想重心直線",
                            line=dict(color="orange", width=2, dash="dot"),
                        )
                    )

                fig2.update_xaxes(
                    autorange="reversed", title="クラブの長さ (inch)"
                )
                fig2.update_yaxes(
                    title="グリップエンド〜全体重心長 (mm) [平衡点]"
                )
                fig2.update_traces(
                    selector=dict(mode="markers+text"),
                    textposition="top center",
                    marker=dict(size=12, color="#D9534F", symbol="square"),
                )
                fig2.update_layout(
                    margin=dict(l=20, r=20, t=30, b=20), height=450
                )
                st.plotly_chart(fig2, use_container_width=True)

        # 【TAB 3】 ヘッドCG垂線交点長
        with tab3:
            if "CG垂線交点長(mm)" in plot_df.columns:
                fig3 = px.scatter(
                    plot_df,
                    x="長さ(inch)",
                    y="CG垂線交点長(mm)",
                    text="番手",
                    hover_data=["モデル", "総重量(g)"],
                )

                fig3.update_xaxes(
                    autorange="reversed", title="クラブの長さ (inch)"
                )
                fig3.update_yaxes(
                    title="グリップエンド〜ヘッドCG垂線交点長 (mm)"
                )
                fig3.update_traces(
                    selector=dict(mode="markers+text"),
                    textposition="top center",
                    marker=dict(size=12, color="#2E8B57", symbol="diamond"),
                )
                fig3.update_layout(
                    margin=dict(l=20, r=20, t=30, b=20), height=450
                )
                st.plotly_chart(fig3, use_container_width=True)

        # 【TAB 4】 シャフト重量
        with tab4:
            if "シャフト重量(g)" in plot_df.columns:
                fig4 = px.bar(
                    plot_df,
                    x="番手",
                    y="シャフト重量(g)",
                    text="シャフト重量(g)",
                    hover_data=["長さ(inch)", "モデル"],
                    color="シャフト重量(g)",
                    color_continuous_scale="Blues",
                )
                fig4.update_traces(textposition="outside")
                fig4.update_layout(
                    margin=dict(l=20, r=20, t=30, b=20),
                    height=450,
                    showlegend=False,
                )
                st.plotly_chart(fig4, use_container_width=True)

        st.info(
            "ℹ️ **注記:** 長さはグリップエンドからヘッドCG heightのシャフト側延長との交点までの長さ。"
            "不明なら1Wはクラブ長より -1.1 inch、FWは -0.8 inch、UTは -0.75 inch、"
            "アイアンは -0.65 inch、ウェッジは無視"
        )
    else:
        st.warning("データが入力されていません。")