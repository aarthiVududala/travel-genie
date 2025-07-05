import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

# ------------------- Page Config -------------------
st.set_page_config(page_title="🌍 Travel Genie", layout="centered")
st.title("🌍 AI Travel Genie")
st.write("Get personalized travel destination recommendations based on your preferences and budget! ✨")

# ------------------- Load Data -------------------
@st.cache_data
def load_destinations():
    return pd.read_csv("destinations.csv")

dest_df = load_destinations()

# ------------------- User Inputs -------------------
region = st.selectbox("🌐 Choose your preferred region:", dest_df["region"].unique())
interest = st.selectbox("🎯 Pick your travel interest:", dest_df["interest"].unique())
budget = st.slider("💰 What's your budget (USD)?", 100, 10000, 2000, step=100)

# ------------------- Filter Matching Destinations -------------------
matching = dest_df[
    (dest_df["region"] == region) &
    (dest_df["interest"] == interest) &
    (dest_df["cost"].astype(float) <= budget)
]

# ------------------- Recommendation Logic -------------------
if not matching.empty:
    best = matching.sort_values("cost").iloc[0]
    
    with st.spinner("🔍 Finding the best destination for you..."):
        time.sleep(1.5)

    st.success(f"🏝️ Your top match: **{best['destination']}**")
    st.markdown(f"**📍 Region:** {best['region']}")
    st.markdown(f"**💸 Estimated Cost:** ${best['cost']}")
    st.markdown(f"**🎯 Best For:** {best['interest']}")
    st.markdown(f"**📅 Best Month:** {best['month']}")
    st.markdown(f"**⛅ Weather:** {best['weather']}")

else:
    st.warning("😢 No perfect match found. Try changing your budget or interest!")

# ------------------- Graph -------------------
st.markdown("---")
st.subheader("📈 Monthly Cost Trend")

if "month" in dest_df.columns:
    cost_df = dest_df.copy()
    cost_df["month"] = cost_df["month"].fillna("Unknown")
    month_data = cost_df.groupby("month")["cost"].mean()

    fig, ax = plt.subplots()
    ax.plot(month_data.index, month_data.values, marker='o', color='green')
    ax.set_title("Average Travel Cost by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Avg Cost (USD)")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("📅 Monthly cost data not available.")

# ------------------- Footer -------------------
st.markdown("---")
st.markdown("Crafted with wanderlust by the AI Travel Genie ✨ #SummerOfAI")
