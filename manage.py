import streamlit as st
import pandas as pd
import csv

df2 = pd.read_csv("./regist.csv")
st.table(df2)
#st.data_editor(df2)

lastno = df2.iloc[-1, 0]

delrow = st.selectbox('削除するNo', list(range(1, lastno+1)))
del_btn = st.button('削除')

delrow2 = delrow - 1

if del_btn:
    #droped_df = df2.drop(delrow2) # まずは*行目だけを削除！
    #st.table(droped_df)
    droped_df = df2.drop(delrow2) # まずは*行目だけを削除！
    st.table(droped_df)
    df3 = droped_df.reset_index(drop=True)
    df3.to_csv("./regist.csv", index=False, header=True, encoding='utf-8') #file saveS
