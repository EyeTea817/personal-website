import streamlit as st

st.header('Poker Statistics 🃏')

col1, col2, col3, col4 = st.columns(4, gap='large')
with col1:
    st.metric('Total Entries', '1,524')
    st.metric('Average Stake', '$17.55')
    st.metric('Total Staked', '$34,125')
    st.metric('Total Cashes', '$44,598')
    st.write('\n\n\n\n')
    cont = st.container(border=True)
    with cont:
        st.write('\n\n\n\n')
        st.metric('Biggest Win', '$8,110')
        st.caption('November 7, 2022\n\n\n\n$100 Sunday Special')
with col2:
    st.metric('Wins', '33')
    st.metric('Final Tables', '150')
with col3:
    st.metric('Lifetime Profit', '$7,188')
    st.metric('Average Profit', '$3.70')
with col4:
    st.metric('Total ROI', '19.2%')
    st.metric('Average ROI', '20.2%')

st.write(f'Last updates: 17 January 2025')
