import streamlit as st
import pandas as pd

# 設定網頁標題
st.set_page_config(page_title="FIRDI-L 資料查詢系統", layout="wide")

st.title("🍎 FIRDI-L 食材進貨資料查詢系統")

# 讀取 CSV 資料
try:
    df = pd.read_csv("ING-003.csv")
    
    # 側邊欄：篩選功能
    st.sidebar.header("篩選條件")
    
    # 搜尋食材
    search_term = st.sidebar.text_input("搜尋食材名稱", "")
    
    # 篩選產地
    origins = ["全部"] + sorted(df["產地"].unique().tolist())
    selected_origin = st.sidebar.selectbox("篩選產地", origins)
    
    # 篩選供應商
    suppliers = ["全部"] + sorted(df["供應商"].unique().tolist())
    selected_supplier = st.sidebar.selectbox("篩選供應商", suppliers)

    # 進行資料過濾
    filtered_df = df.copy()
    if search_term:
        filtered_df = filtered_df[filtered_df["食材"].str.contains(search_term, na=False)]
    if selected_origin != "全部":
        filtered_df = filtered_df[filtered_df["產地"] == selected_origin]
    if selected_supplier != "全部":
        filtered_df = filtered_df[filtered_df["供應商"] == selected_supplier]

    # 顯示數據統計
    col1, col2, col3 = st.columns(3)
    col1.metric("總項目數", len(df))
    col2.metric("目前顯示數量", len(filtered_df))
    col3.metric("產地總數", len(df["產地"].unique()))

    # 顯示資料表格
    st.subheader("📊 資料列表")
    st.dataframe(filtered_df, use_container_width=True)

    # 簡單的視覺化：各產地佔比
    st.subheader("📈 產地分佈圖")
    origin_counts = filtered_df["產地"].value_counts()
    st.bar_chart(origin_counts)

except Exception as e:
    st.error(f"讀取資料時發生錯誤: {e}")
    st.info("請確認 ING-003.csv 檔案是否存在且格式正確。")
