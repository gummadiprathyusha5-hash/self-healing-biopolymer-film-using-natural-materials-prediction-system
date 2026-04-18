import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Self-Healing Film Predictor", layout="wide")

st.title("🧪 Self-Healing Biopolymer Film Predictor")

# Sidebar inputs
st.sidebar.header("Material Composition (%)")

chitosan = st.sidebar.slider("Chitosan %", 0, 100, 30)
gelatin = st.sidebar.slider("Gelatin %", 0, 100, 20)
starch = st.sidebar.slider("Starch %", 0, 100, 20)
aloe = st.sidebar.slider("Aloe Vera %", 0, 100, 10)
glycerol = st.sidebar.slider("Glycerol %", 0, 100, 10)

st.sidebar.header("Environment Conditions")

temperature = st.sidebar.number_input("Temperature (°C)", 0, 100, 40)
humidity = st.sidebar.number_input("Humidity (%)", 0, 100, 60)
ph = st.sidebar.number_input("pH Level", 0.0, 14.0, 6.5)

damage = st.selectbox("Damage Type", ["Scratch", "Cut", "Crack"])

def calculate_efficiency(chitosan, gelatin, starch, aloe, glycerol, temperature, humidity):
    efficiency = 60

    if chitosan > 30:
        efficiency += 10
    if aloe > 10:
        efficiency += 8
    if 35 <= temperature <= 45:
        efficiency += 10
    if humidity > 70:
        efficiency -= 5

    return efficiency


def find_best_combination(temperature, humidity):
    best_score = -1
    best_mix = None

    # try many combinations (kept small so it runs fast)
    for chitosan in range(20, 51, 5):
        for gelatin in range(10, 41, 5):
            for starch in range(10, 41, 5):
                aloe = 10
                glycerol = 10

                total = chitosan + gelatin + starch + aloe + glycerol

                if total == 100:
                    score = calculate_efficiency(
                        chitosan, gelatin, starch, aloe, glycerol,
                        temperature, humidity
                    )

                    if score > best_score:
                        best_score = score
                        best_mix = (chitosan, gelatin, starch, aloe, glycerol)

    return best_mix, best_score

if st.button("Predict Film Performance"):

    # --- Logic ---
    efficiency = 60

    if chitosan > 30:
        efficiency += 10

    if aloe > 10:
        efficiency += 8

    if 35 <= temperature <= 45:
        efficiency += 10

    if humidity > 70:
        efficiency -= 5

    # Strength
    strength = "Medium"
    if chitosan > 40:
        strength = "High"
    if starch > 40:
        strength = "Low"

    # Biodegradability
    biodegradability = "Moderate"
    if starch > 30:
        biodegradability = "Fast"
    if chitosan > 40:
        biodegradability = "Slow"

    # --- Results ---
    st.subheader("📊 Prediction Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Healing Efficiency", f"{efficiency}%")
    col2.metric("Strength", strength)
    col3.metric("Biodegradability", biodegradability)

    # --- Chart ---
    st.subheader("📈 Material Composition")

    data = {
        "Material": ["Chitosan", "Gelatin", "Starch", "Aloe", "Glycerol"],
        "Percentage": [chitosan, gelatin, starch, aloe, glycerol]
    }

    df = pd.DataFrame(data)

    fig, ax = plt.subplots()
    ax.bar(df["Material"], df["Percentage"])
    ax.set_ylabel("Percentage")
    ax.set_title("Composition Distribution")

    st.pyplot(fig)

    # --- Suggestion ---
    st.subheader("💡 Suggestion")

    if efficiency < 80:
        st.warning("Increase Chitosan or Aloe vera to improve healing.")
    else:
        st.success("Good composition! High healing efficiency.")
    
    st.subheader("🧠 Best Suggested Composition")
    best_mix, best_score = find_best_combination(temperature, humidity)

    if best_mix:
        c, g, s, a, gl = best_mix
        st.success(f"""
        Chitosan: {c}%  
        Gelatin: {g}%  
        Starch: {s}%  
        Aloe: {a}%  
        Glycerol: {gl}%  

        Predicted Efficiency: {best_score}%
        """)