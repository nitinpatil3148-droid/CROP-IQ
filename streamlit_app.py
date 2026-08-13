import streamlit as st
import requests
import time


# ============================================================
# CONFIGURATION
# ============================================================

BACKEND_URL = "https://crop-iq-0gbw.onrender.com"


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="CropIQ",
    page_icon="🌱",
    layout="wide"
)


# ============================================================
# SIMPLE CSS
# ============================================================

st.markdown("""
<style>

.main {
    padding-top: 20px;
}

.title {
    font-size: 40px;
    font-weight: 700;
    color: #1b5e20;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 18px;
    color: #666666;
    margin-bottom: 25px;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 15px;
}

.status-box {
    padding: 20px;
    border-radius: 10px;
    background-color: #f5f5f5;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🌱 CropIQ</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Precision Smart Spraying System'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# FUNCTIONS
# ============================================================

def get_state():

    try:

        response = requests.get(
            BACKEND_URL + "/state",
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

    except Exception:
        pass

    return None


def get_latest_image():

    try:

        response = requests.get(
            BACKEND_URL + "/latest-image",
            timeout=10
        )

        if response.status_code == 200:
            return response.content

    except Exception:
        pass

    return None


def send_spray_command(amount):

    try:

        response = requests.post(
            BACKEND_URL + "/spray",
            json={
                "amount_ml": amount
            },
            timeout=15
        )

        return response

    except Exception as e:

        return None


# ============================================================
# MAIN LAYOUT
# ============================================================

image_column, control_column = st.columns(
    [1.5, 1],
    gap="large"
)


# ============================================================
# COMPONENT 1 — PLANT IMAGE
# ============================================================

with image_column:

    st.markdown(
        '<div class="section-title">🌿 Plant Image</div>',
        unsafe_allow_html=True
    )

    image = get_latest_image()

    if image:

        st.image(
            image,
            caption="Latest image captured by Raspberry Pi",
            use_container_width=True
        )

    else:

        st.info(
            "No plant image available yet."
        )


# ============================================================
# COMPONENT 2 + 3 — DOSAGE AND SPRAY
# ============================================================

with control_column:

    st.markdown(
        '<div class="section-title">💧 Spray Control</div>',
        unsafe_allow_html=True
    )

    dosage = st.number_input(
        "Required dosage (mL)",
        min_value=1,
        max_value=500,
        value=25,
        step=1
    )

    st.write(
        "Selected dosage:"
    )

    st.markdown(
        f"### **{dosage} mL**"
    )

    spray_clicked = st.button(
        "🚿 SPRAY",
        type="primary",
        use_container_width=True
    )

    if spray_clicked:

        response = send_spray_command(
            dosage
        )

        if response is None:

            st.error(
                "❌ Could not connect to Render backend."
            )

        elif response.status_code == 200:

            st.success(
                f"✅ Spray command sent: {dosage} mL"
            )

            st.rerun()

        elif response.status_code == 409:

            st.warning(
                "⚠️ A spray operation is already running."
            )

        else:

            st.error(
                f"Backend error: {response.text}"
            )


# ============================================================
# COMPONENT 4 — SPRAY STATUS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📡 Spray Status</div>',
    unsafe_allow_html=True
)

state = get_state()


if state is None:

    st.error(
        "🔴 Backend unavailable"
    )

else:

    current_status = state.get(
        "status",
        "Ready"
    )

    sprayed_amount = state.get(
        "sprayed_amount",
        0
    )

    # --------------------------------------------
    # READY
    # --------------------------------------------

    if current_status == "Ready":

        st.success(
            "🟢 READY"
        )

        st.caption(
            "System is ready for spraying."
        )


    # --------------------------------------------
    # SPRAYING
    # --------------------------------------------

    elif current_status == "Spraying...":

        st.warning(
            "🟡 SPRAYING..."
        )

        st.caption(
            "Pump is currently dispensing water."
        )


    # --------------------------------------------
    # COMPLETED
    # --------------------------------------------

    elif current_status == "Completed":

        st.success(
            "🟢 COMPLETED"
        )

        st.write(
            f"**{sprayed_amount:.2f} mL sprayed**"
        )


    # --------------------------------------------
    # OTHER STATUS
    # --------------------------------------------

    else:

        st.info(
            f"Status: {current_status}"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CropIQ | Raspberry Pi Precision Spraying System"
)
