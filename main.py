import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

st.title("Streamlit 超入門")
st.write("DataFrame")

df = pd.read_csv("収入支出管理表.csv")

st.write(df)

st.dataframe(df, width=100, height=100)

st.table()


"""
# 見出し1
## 見出し2
### 見出し3

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

あいうえお
```
"""

if st.checkbox("Show Image"):
    img = Image.open("かめさん.png")
    st.image(img, caption="イケダジョブズ", use_column_width=True)


option = st.sidebar.selectbox("あなたの趣味は何ですか??", options=["作家", "野球", "フットサル", "プログラミング"])
f"あなたの好きな趣味は、{option}です"


text = st.sidebar.text_input("あなたは何歳ですか?")
f"あなたの年齢は、{text}歳です"


condition = st.sidebar.slider("あなたの今日の調子は??:sunglasses:", min_value=1, max_value=10, step=2)
st.write(condition)


latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f"Iteration {i + 1}")
    bar.progress(i + 1)
    time.sleep(0.1)


"Done!!"