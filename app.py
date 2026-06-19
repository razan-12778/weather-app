import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ===== الصفحة =====
st.set_page_config(
    page_title="Saudi Weather Pro",
    page_icon="🌤️",
    layout="wide"
)

# ===== تصميم =====
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fafc, #eef2ff);
    text-align: center;
}

h1, h2, h3 {
    text-align: center;
    color: #111827;
}

[data-testid="metric-container"]{
    background: white;
    border-radius: 16px;
    padding: 14px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# ===== عنوان =====
st.title("🇸🇦🌤️ Saudi Weather ")

# ===== بيانات =====
cities = ["الرياض","جدة","مكة","المدينة","الدمام","أبها","تبوك","جازان"]

lat = [24.7136,21.4858,21.3891,24.5247,26.4207,18.2465,28.3835,16.8892]
lon = [46.6753,39.1925,39.8579,39.5692,50.0888,42.5117,36.5662,42.5510]

df = pd.DataFrame({
    "المدينة": cities,
    "lat": lat,
    "lon": lon,
    "الحرارة": np.random.randint(20, 45, len(cities)),
    "الرطوبة": np.random.randint(20, 90, len(cities)),
    "الرياح": np.random.randint(5, 40, len(cities)),
    "الأمطار": np.random.randint(0, 100, len(cities)),
    "الغبار": np.random.randint(20, 180, len(cities))
})

# ===== اختيار المدينة =====
selected_city = st.sidebar.selectbox("🌍 اختر المدينة", cities)
city = df[df["المدينة"] == selected_city].iloc[0]

st.subheader(f"📍 الطقس في {selected_city}")

# ===== بطاقات =====
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("🌡️ الحرارة", f"{city['الحرارة']}°C")
c2.metric("💧 الرطوبة", f"{city['الرطوبة']}%")
c3.metric("💨 الرياح", f"{city['الرياح']} km/h")
c4.metric("🌧️ الأمطار", f"{city['الأمطار']}%")
c5.metric("🌫️ الغبار", f"{city['الغبار']}")

st.divider()

# ===== خريطة =====
st.subheader("🗺️ خريطة السعودية")

fig_map = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    size="الحرارة",
    color="الحرارة",
    hover_name="المدينة",
    color_continuous_scale="Turbo",
    zoom=4,
    mapbox_style="open-street-map"
)

st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# ===== توقعات الأسبوع =====
st.subheader("📅 توقعات الأسبوع")

days = ["السبت","الأحد","الاثنين","الثلاثاء","الأربعاء","الخميس","الجمعة"]

forecast = pd.DataFrame({
    "اليوم": days,
    "الحرارة": np.random.randint(20, 45, 7),
    "الأمطار": np.random.randint(0, 100, 7),
    "الرياح": np.random.randint(5, 40, 7)
})

# ===== رسومات جنب بعض =====
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(
        forecast,
        x="اليوم",
        y="الحرارة",
        markers=True,
        color_discrete_sequence=["#ef4444"],
        title="🌡️ الحرارة خلال الأسبوع"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(
        forecast,
        x="اليوم",
        y="الأمطار",
        color="الأمطار",
        color_continuous_scale="Blues",
        title="🌧️ الأمطار"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ===== رسومات ثانية جنب بعض =====
col3, col4 = st.columns(2)

with col3:
    fig3 = px.area(
        forecast,
        x="اليوم",
        y="الرياح",
        color_discrete_sequence=["#10b981"],
        title="🌬️ الرياح"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.bar(
        df,
        x="المدينة",
        y="الحرارة",
        color="الحرارة",
        color_continuous_scale="Plasma",
        title="🌡️ حرارة المدن"
    )
    st.plotly_chart(fig4, use_container_width=True)

# ===== الغبار (لوحده تحت) =====
st.subheader("🌫️ مؤشر الغبار")

fig5 = px.scatter(
    df,
    x="المدينة",
    y="الغبار",
    size="الغبار",
    color="الغبار",
    color_continuous_scale="OrRd",
    title="توزيع الغبار"
)

st.plotly_chart(fig5, use_container_width=True)

# ===== جدول =====
st.subheader("📋 بيانات المدن")
st.dataframe(df, use_container_width=True)

# ===== تحديث =====
if st.button("🔄 تحديث البيانات"):
    st.rerun()
