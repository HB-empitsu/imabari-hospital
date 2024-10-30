import pandas as pd
from streamlit_folium import st_folium

import folium
import streamlit as st

st.set_page_config(
    page_title="今治市の医療機関", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None
)
st.title("今治市の医療機関")


@st.cache_data()
def load_data():
    df = pd.read_csv(st.secrets["url"], dtype={"ID": str})

    df["color"] = "blue"
    df["color"] = df["color"].mask(df["救急"] > 0, "red")

    return df


df = load_data()

option = [
    "救急",
    "内科",
    "小児科",
    "感染症内科",
    "血液内科",
    "糖尿病内科",
    "糖尿病・内分泌内科",
    "脳神経内科",
    "呼吸器内科",
    "循環器内科",
    "消化器内科",
    "胃腸内科",
    "腎臓内科",
    "肝臓内科",
    "神経内科",
    "外科",
    "脳神経外科",
    "循環器外科",
    "心臓血管外科",
    "消化器外科",
    "胃腸外科",
    "肛門外科",
    "整形外科",
    "形成外科",
    "産婦人科",
    "眼科",
    "耳鼻いんこう科",
    "皮膚科",
    "皮膚泌尿器科",
    "泌尿器科",
    "精神科",
    "心療内科",
    "歯科",
    "歯科口腔外科",
    "小児歯科",
    "アレルギー科",
    "リウマチ科",
    "リハビリテーション科",
    "放射線科",
    "病理診断科",
    "麻酔科",
]

# ストリームリットセレクトボックスの作成
chois = st.multiselect("診療科目を選択してください", option, max_selections=3, placeholder="選んでください")


filtered_df = df[df[chois].all(axis=1)].copy() if chois else df.copy()


st.subheader("医療機関")

st.dataframe(
    filtered_df[["名称", "住所", "電話番号", "URL", "診療科目名"]],
    column_config={
        "URL": st.column_config.LinkColumn("リンク"),
    },
    hide_index=True,
    use_container_width=True,
)

st.subheader("地図表示")

df_map = filtered_df[["名称", "住所", "電話番号", "診療科目名", "緯度", "経度", "URL", "color"]]

m = folium.Map(
    location=[df_map["緯度"].mean(), df_map["経度"].mean()],
    tiles="https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png",
    attr='&copy; <a href="https://maps.gsi.go.jp/development/ichiran.html">国土地理院</a>',
    zoom_start=12,
)

for _, r in df_map.iterrows():
    folium.Marker(
        location=[r["緯度"], r["経度"]],
        popup=folium.Popup(
            f'<p><a href="{r["URL"]}" target="_blank">{r["名称"]}</a></p><p>{r["住所"]}</p><p>{r["電話番号"]}</p>',
            max_width=300,
        ),
        tooltip=r["名称"],
        icon=folium.Icon(color=r["color"]),
    ).add_to(m)

# マップをストリームリットに表示
st_data = st_folium(m, use_container_width=True, returned_objects=[])
