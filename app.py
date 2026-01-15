import streamlit as st
import matplotlib.pyplot as plt

# Make 3 blank lines
for i in range(3):
    st.write('')

st.write("Hi, this website will help you estimate your monthly energy cost and see appliance usage estimate.")

# Choose the input mode
mode = st.radio("Select input method:", ["Total monthly energy usage", "Appliance hours"])

# Total kWh mode
if mode == "Total monthly energy usage":
    monthly_kwh = st.number_input(
        "Enter your estimated total monthly energy usage (kWh):",
        min_value=0.0,
        value=500.0
    )
    rate = st.number_input(
        "Enter your electricity rate ($/kWh):",
        min_value=0.0,
        value=0.20
    )
    monthly_cost = monthly_kwh * rate

    # Assume appliances breakdown percentages
    appliances_percentage = {
        "AC/HVAC": 0.40,
        "Fridge": 0.10,
        "Lighting": 0.15,
        "Electronics": 0.23,
        "Washer/Dryer": 0.12
    }
    appliance_energy = {appliance: monthly_kwh * percentage for appliance, percentage in appliances_percentage.items()}

# Appliance hours mode
else:
    rate = st.number_input(
        "Enter your electricity rate ($/kWh):",
        min_value=0.0,
        value=0.20
    )
    # Appliance power ratings (kW)
    appliance_power = {
        "AC/HVAC": 1.5,
        "Fridge": 0.2,
        "Lighting": 0.05,
        "Electronics": 0.15,
        "Washer/Dryer": 2.5
    }
    appliance_energy = {}
    for appliance, power in appliance_power.items():
        if appliance == "Washer/Dryer":
            cycles = st.number_input(f"{appliance} cycles per week", min_value=0, value=4)
            energy = power * cycles * 4
        else:
            hours = st.number_input(f"{appliance} usage hours per day", min_value=0, value=5)
            energy = power * hours * 30
        appliance_energy[appliance] = energy

    monthly_kwh = sum(appliance_energy.values())
    monthly_cost = monthly_kwh * rate

# Display results
st.subheader("Estimated Monthly Cost")
st.success(f"${monthly_cost:.2f}")

st.subheader("Estimated Appliance Energy Usage (kWh)")
for appliance, energy in appliance_energy.items():
    st.write(f"{appliance}: {energy:.1f} kWh")

# Visualization
st.subheader("Energy Usage by Appliance")
fig, ax = plt.subplots()
ax.bar(appliance_energy.keys(), appliance_energy.values(), color='skyblue')
ax.set_ylabel("Energy (kWh)")
ax.set_title("Appliance Energy Breakdown")
st.pyplot(fig)

# Recommendation based on the estimate cost
highest = max(appliance_energy, key=appliance_energy.get)
st.subheader("Recommendation")
if monthly_cost < 150:
    st.success("Your energy usage is efficient.")
elif monthly_cost < 300:
    st.warning("Your energy usage is moderate. Please consider energy saving.")
else:
    st.error("Your energy usage is high! Reduce heavy appliances usage may help.")

appliance_colors = {
    "AC/HVAC": "#ff6666",
    "Fridge": "#66b3ff",
    "Lighting": "#ffcc66",
    "Electronics": "#99ff99",
    "Washer/Dryer": "#ff99ff"
}
st.markdown(
    """
    ---
    © 2026 Thanh Xuan Dao. All rights reserved.
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .sticky-banner {
        position: fixed;
        top: 50px;               
        left: 0;
        width: 100%;
        background-color: #2ca02c; 
        color: white;
        text-align: center;
        padding: 20px;
        font-size: 18px;
        font-weight: bold;
    }
    </style>

    <div class="sticky-banner">
        Home Energy Usage Cost Estimate
    </div>
    """,
    unsafe_allow_html=True
)

