# Hydrogen Storage Optimization Web App (Streamlit)
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Page Configuration ---
st.set_page_config(page_title="Underground Hydrogen Storage Optimization", layout="wide")

# --- Custom Styles ---
st.markdown("""
    <style>
        .main-title {
            background-color: #b2521c;
            color: white;
            padding: 1rem;
            font-size: 2rem;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .h2-icon {
            font-size: 2.5rem;
            font-weight: bold;
            color: white;
            margin-right: 1rem;
        }
        .footer {
            background-color: #b2521c;
            color: white;
            padding: 0.75rem;
            text-align: center;
            font-size: 1rem;
        }
        .footer b {
            font-weight: bold;
        }
        .output-card {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        .low-risk { background-color: #d4edda; color: #155724; }
        .moderate-risk { background-color: #fff3cd; color: #856404; }
        .high-risk { background-color: #f8d7da; color: #721c24; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="main-title"><span class="h2-icon">H<sub>2</sub></span>Underground Hydrogen Storage Optimization</div>', unsafe_allow_html=True)

# --- Sidebar Inputs ---
st.sidebar.header("Input Parameters")
pressure = st.sidebar.slider("Injection Pressure (MPa)", 1.0, 10.0, 5.0, step=0.1)
formation = st.sidebar.selectbox("Formation Type", ["Depleted Gas Field", "Salt Cavern"])

thermal_cycling = st.sidebar.checkbox("Thermal Cycling")
if thermal_cycling:
    delta_T = st.sidebar.number_input("ΔT (°C):", value=25)
    cycles = st.sidebar.number_input("Cycles:", value=1)
else:
    delta_T = 0
    cycles = 1

# --- Prediction Model ---
def predict(pressure, formation, delta_T=0, cycles=1):
    if formation == "Depleted Gas Field":
        stress = 0.21 * pressure + 0.3 * pressure**2
        displacement = 0.0015 * pressure + 0.0001 * pressure**2
    else:
        stress = 0.18 * pressure + 0.2 * pressure**2
        displacement = 0.001 * pressure + 0.00005 * pressure**2

    alpha = 3.5e-5
    thermal_strain = alpha * delta_T * cycles
    stress += stress * thermal_strain
    displacement += displacement * thermal_strain

    if stress > 6.5 or displacement > 0.015:
        risk = "High"
    elif stress > 5.5 or displacement > 0.012:
        risk = "Moderate"
    else:
        risk = "Low"

    return stress, displacement, risk

stress, displacement, risk = predict(pressure, formation, delta_T, cycles)

# --- Outputs ---
st.subheader("Outputs")

if risk == "High":
    risk_class = "high-risk"
elif risk == "Moderate":
    risk_class = "moderate-risk"
else:
    risk_class = "low-risk"

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="output-card {risk_class}"><b>Stress:</b> {stress:.2f} MPa</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="output-card {risk_class}"><b>Displacement:</b> {displacement*1000:.2f} mm</div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="output-card {risk_class}"><b>Risk Level:</b> {risk.upper()}</div>', unsafe_allow_html=True)

# --- Graphs ---
st.subheader("System Response")
pressures = np.linspace(1, 10, 100)
stresses = []
disps = []

for p in pressures:
    s, d, _ = predict(p, formation, delta_T, cycles)
    stresses.append(s)
    disps.append(d * 1000)

fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].plot(pressures, stresses, label="Stress")
ax[0].axvline(pressure, color='gray', linestyle='--')
ax[0].set_title("Stress vs Injection Pressure")
ax[0].set_xlabel("Pressure (MPa)")
ax[0].set_ylabel("Stress (MPa)")
ax[0].grid()

ax[1].plot(pressures, disps, color='orange', label="Displacement")
ax[1].axvline(pressure, color='gray', linestyle='--')
ax[1].set_title("Displacement vs Injection Pressure")
ax[1].set_xlabel("Pressure (MPa)")
ax[1].set_ylabel("Displacement (mm)")
ax[1].grid()

st.pyplot(fig)

# --- Footer ---
st.markdown('<div class="footer">Developed by <b>Mohammed Farhan Jameel</b> | UT Energy Week 2025</div>', unsafe_allow_html=True)


