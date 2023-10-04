import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
# フォントの設定
font = FontProperties(fname='/Library/Fonts/Arial Unicode.ttf')
import matplotlib as mpl
# 日本語対応フォントに設定（例：IPAexGothic）
mpl.rcParams['font.family'] = 'IPAexGothic'
import seaborn as sns
from datetime import datetime

# アプリのタイトル
st.title("個人支出管理")
# アプリの説明文章
st.subheader(':memo:支出をグラフにして可視化するアプリ')

# データの取得
df = pd.read_csv("支出管理.csv")
# データ型の変換
df['date'] = pd.to_datetime(df['date'])

# 年と月を選択して表を表示させる
years = sorted(df["date"].dt.year.unique())
months = [i for i in range(1, 13)]
# サイドバーで年と月を選択
select_year = st.sidebar.selectbox("年を選択してください", years)
select_month = st.sidebar.selectbox("月を選択してください", months)
# 選んだ年と月のデータフレームを抽出し、データフレームとして表示
filtered_df = df[(df["date"].dt.month == select_month) & (df["date"].dt.year == select_year)]  

# 月の日付ごとの支出の総金額
# plt.figure(figsize=(12, 6))
# plt.bar(filtered_df["date"], height=filtered_df["amount"])
# plt.title(f"{select_year}年{select_month}月の支出")
# plt.xlabel("日付")
# plt.ylabel("金額")
# plt.xticks(rotation=45)
# plt.tight_layout()
# st.pyplot(plt)
st.bar_chart(filtered_df, x="date", y="amount", use_container_width=True)

# カテゴリー毎のデータフレーム作成
sum_df = filtered_df.groupby("category")["amount"].sum().reset_index().sort_values(by="amount", ascending=False)
# カラーマップと色の長さを指定
cmap = plt.get_cmap("Paired")
colors = [cmap(i) for i in range(len(sum_df["category"]))]

# カテゴリー毎の棒グラ
mpl.rcParams['font.family'] = 'IPAexGothic'
plt.figure(figsize=(12, 6))
bars = plt.bar(x="category", height="amount", data=sum_df, color=colors)
plt.title("カテゴリー毎の支出", fontproperties=font, fontsize=25)
plt.xlabel("カテゴリー", fontproperties=font, fontsize=15)
plt.ylabel("金額", fontproperties=font, fontsize=15)
# 各棒の上に数値を表示
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom')  # va: 垂直方向の位置

st.pyplot(plt, use_container_width=True)

# Matplotlibで円グラフを作成
mpl.rcParams['font.family'] = 'IPAexGothic'
labels = sum_df["category"].value_counts().index
sizes = sum_df["amount"].sort_values(ascending=False)
fig, ax = plt.subplots()
ax.pie(sizes, 
    labels=labels, 
    autopct=lambda p: '{:.1f}%'.format(p) if p > 5 else '', 
    startangle=90, 
    rotatelabels=True,
    counterclock=False,
    colors=colors)
ax.axis('equal')
plt.title("支出(カテゴリー割合)", fontproperties=font, y=1.2)
# アスペクト比を保持
plt.axis('equal')
st.pyplot(fig)
plt.show()

st.write("月支出の詳細")
data = st.dataframe(filtered_df, use_container_width=True, hide_index=True)

max_amount_row = filtered_df[filtered_df['amount'] == filtered_df['amount'].max()]
min_amount_row = filtered_df[filtered_df['amount'] == filtered_df['amount'].min()]

# 月の最大金値、最小値、平均値、中央値
st.bar_chart(filtered_df, x="date", y="amount")
st.write(f"{select_year}年{select_month}月の最大金額は、¥{filtered_df['amount'].max():,.0f}")
st.dataframe(max_amount_row)
st.write(f"{select_year}年{select_month}月の最小金額は、¥{filtered_df['amount'].min():,.0f}")
st.dataframe(min_amount_row)
st.write(f"{select_year}年{select_month}月の1日の平均値は、¥{filtered_df['amount'].mean():,.0f}")
st.write(f"{select_year}年{select_month}月の1日の中央値は、¥{filtered_df['amount'].median():,.0f}")
