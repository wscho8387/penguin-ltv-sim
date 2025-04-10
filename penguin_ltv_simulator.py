import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Penguin Glide - LTV 시뮬레이터", layout="centered")

st.title("🐧 Penguin Glide Festival - LTV 기반 수익 시뮬레이터")

st.markdown("### 📥 주요 지표 입력")

# User Inputs
cpi = st.number_input("CPI (Cost per Install)", value=0.20, step=0.01)
d1 = st.slider("D1 Retention (%)", 0, 100, 15) / 100
d7 = st.slider("D7 Retention (%)", 0, 100, 6) / 100
d30 = st.slider("D30 Retention (%)", 0, 100, 3) / 100
sessions_per_day = st.slider("일평균 세션 수", 1, 20, 8)
ads_per_session = st.slider("세션당 광고 시청 수", 0.0, 5.0, 2.5)
ecpm = st.number_input("광고 eCPM ($)", value=10.0, step=0.5)
iap_conversion = st.slider("IAP 전환율 (%)", 0.0, 10.0, 1.5) / 100
avg_iap = st.number_input("평균 결제 금액 ($)", value=4.5)

# Retention curve modeling (log-linear decay)
days = np.arange(1, 31)
ret_curve = d1 * (1 - (np.log(days) / np.log(30))) * (d30 / d1)
ret_curve = np.clip(ret_curve, d30, d1)

# IAA Revenue
daily_iaa = sessions_per_day * ads_per_session * (ecpm / 1000)
ltv_iaa = np.sum(ret_curve * daily_iaa)

# IAP Revenue
ltv_iap = iap_conversion * avg_iap

# Final LTV
total_ltv = ltv_iaa + ltv_iap
roas = total_ltv / cpi * 100

st.markdown("### 💰 시뮬레이션 결과")
st.metric("📈 총 LTV (28일)", f"${total_ltv:.3f}")
st.metric("💡 ROAS", f"{roas:.1f}%")
st.metric("IAA vs IAP", f"${ltv_iaa:.3f} / ${ltv_iap:.3f}")

# Plot
st.markdown("### 📊 일별 LTV 누적 곡선")
cum_ltv = np.cumsum(ret_curve * daily_iaa)
fig, ax = plt.subplots()
ax.plot(days, cum_ltv, label="IAA LTV (누적)")
ax.axhline(y=ltv_iaa, color="gray", linestyle="--", alpha=0.5)
ax.set_xlabel("Day")
ax.set_ylabel("LTV ($)")
ax.set_title("LTV 누적 곡선 (IAA 기준)")
st.pyplot(fig)

st.markdown("---")
st.caption("📌 이 시뮬레이터는 Penguin Glide Festival의 가정 기반 KPI를 분석하기 위한 도구입니다.")
