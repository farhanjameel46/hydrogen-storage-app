
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Page Setup ---
st.set_page_config(page_title="Hydrogen Storage Predictor", layout="wide")
st.title("Underground Hydrogen Storage Optimization")
st.markdown("A predictive tool for evaluating geomechanical response to hydrogen injection in salt caverns and depleted gas fields.")

# --- Sidebar Inputs ---
st.sidebar.header("Input Parameters")
pressure = st.sidebar.slider("Injection Pressure (MPa)", 1.0, 10.0, 5.0, step=0.1)
formation = st.sidebar.selectbox("Formation Type", ["Depleted Gas Field", "Salt Cavern"])

st.sidebar.markdown("---")
thermal_cycle = st.sidebar.checkbox("Include Thermal Cycling Effect?")
if thermal_cycle:
    delta_T = st.sidebar.slider("Temperature Swing (°C)", 1, 100, 25)
    cycles = st.sidebar.slider("Cycle Duration (days)", 1, 30, 1)
else:
    delta_T = 0
    cycles = 1

# --- Prediction Model ---
def predict(pressure, formation, delta_T=0, cycles=1):
    if formation == "Depleted Gas Field":
        stress = 0.21 * pressure + 0.3 * pressure**2
        displacement = 0.0015 * pressure + 0.0001 * pressure**2
    else:  # Salt Cavern
        stress = 0.18 * pressure + 0.2 * pressure**2
        displacement = 0.001 * pressure + 0.00005 * pressure**2

    # Add thermal effect
    alpha = 3.5e-5  # thermal expansion coefficient
    thermal_strain = alpha * delta_T * cycles
    stress += stress * thermal_strain
    displacement += displacement * thermal_strain

    # Risk level
    if stress > 6.5 or displacement > 0.015:
        risk = "High"
    elif stress > 5.5 or displacement > 0.012:
        risk = "Moderate"
    else:
        risk = "Low"

    return stress, displacement, risk

# --- Prediction Output ---
stress, displacement, risk = predict(pressure, formation, delta_T, cycles)

col1, col2 = st.columns(2)
with col1:
    st.metric("Predicted Stress", f"{stress:.2f} MPa")
    st.metric("Risk Level", risk)
with col2:
    st.metric("Predicted Displacement", f"{displacement*1000:.2f} mm")
    if risk == "High":
        st.error("Warning: High risk of caprock damage.")
    elif risk == "Moderate":
        st.warning("Moderate risk – monitor closely.")
    else:
        st.success("Low mechanical risk.")

# --- Plotting Section ---
st.markdown("### Response Curves")
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

# Footer
st.markdown("---")
st.caption("Developed by Mohammed Farhan Jameel | UT Energy Week 2025")
