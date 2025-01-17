import streamlit as st


# --- PAGE SETUP ---
about_page = st.Page(
    page='views/about_me.py',
    title='About Me',
    icon=':material/brush:',
    default=True
)

gal1 = st.Page(
    page='views/gal.py',
    title= 'Black & White',
    icon= ':material/palette:'
)

gal2 = st.Page(
    page='views/gal2.py',
    title= 'Illustration',
    icon= ':material/palette:'
)

gal3 = st.Page(
    page='views/gal3.py',
    title= 'Mixed-Media',
    icon= ':material/palette:'
)

store = st.Page(
    page='views/store.py',
    title= 'Store',
    icon= ':material/sell:'
)

pg = st.navigation({
    'Info': [about_page],
    'Galleries': [gal1, gal2, gal3]
})

#--- SHARED ON ALL PAGES ---
st.sidebar.text('Amy Holysz, 2025.')

pg.run()
