import streamlit as st
import requests
import time


# =========================================================
# CONFIGURATION
# =========================================================

BACKEND_URL = "PASTE_YOUR_RENDER_URL_HERE"


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CropIQ",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f5f7f6;
    }

    /* Remove top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Header */
    .cropiq-header {
        background-color: #ffffff;
        padding: 22px 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        border: 1px solid #e5e7eb;
    }

    .cropiq-title {
        font-size: 34px;
        font-weight: 700;
        margin: 0;
    }

    .cropiq-subtitle {
        font-size: 15px;
        color: #6b7280;
        margin-top: 4px;
    }

    /* Status badge */
    .online-badge {
        background-color: #dcfce7;
        color: #166534;
        padding: 8px 14px;
        border-radius: 20px;
        font-weight: 600;
        text-align: center;
    }

    /* Cards */
    .card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        min-height: 300px;
    }

    .card-title {
        font-size: 20px;
        font-weight: 650;
        margin-bottom: 20px;
    }

    /* Status card */
    .status-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        margin-top: 20px;
        text-align: center;
    }

    .status-ready {
        font-size: 28px;
        font-weight: 700;
    }

    .status-description {
        color: #6b7280;
        margin-top: 5px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 13px;
        margin-top: 30px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

header_col1, header_col2 = st.columns(
    [5, 1]
)

with header_col1:

    st.markdown(
        """
        <div class="cropiq-header">
            <div class="cropiq-title">
                🌱 CropIQ
            </div>
            <div class="cropiq-subtitle">
                Precision Smart Spraying System
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with header_col2:

    st.markdown(
        """
        <div style="margin-top:25px;">
            <div class="online-badge">
                ● Raspberry Pi
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BACKEND STATE
# =========================================================

def get_state():

    try:

        response = requests.get(
            BACKEND_URL + "/state",
            timeout=10
        )

        if response.status_code == 200:

            return response.json()

    except Exception:

        return None

    return None


state = get_state()


# =========================================================
# MAIN TWO-COLUMN AREA
# =========================================================

left_col, right_col = st.columns(
    [1.4, 1],
    gap="large"
)


# =========================================================
# LEFT - PLANT IMAGE
# =========================================================

with left_col:

    st.markdown(
        """
        <div class="card">
            <div class="card-title">
                🌿 Plant Image
            </div>
        """,
        unsafe_allow_html=True
    )

    try:

        image_response = requests.get(
            BACKEND_URL + "/latest-image",
            timeout=10
        )

        if image_response.status_code == 200:

            st.image(
                image_response.content,
                use_container_width=True
            )

        else:

            st.info(
                "Waiting for Raspberry Pi camera..."
            )

    except Exception:

        st.warning(
            "Camera image unavailable."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# RIGHT - SPRAY CONTROL
# =========================================================

with right_col:

    st.markdown(
        """
        <div class="card">
            <div class="card-title">
                💧 Spray Control
            </div>
        """,
        unsafe_allow_html=True
    )

    dosage = st.number_input(
        "Required dosage",
        min_value=1.0,
        max_value=500.0,
        value=25.0,
        step=1.0
    )

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:16px;
            margin:15px 0;
            color:#6b7280;
        ">
            Required amount
            <br>
            <strong style="
                font-size:32px;
                color:#111827;
            ">
                {dosage:.0f} ml
            </strong>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🚿  SPRAY",
        type="primary",
        use_container_width=True
    ):

        try:

            response = requests.post(
                BACKEND_URL + "/spray",
                json={
                    "amount_ml": dosage
                },
                timeout=15
            )

            if response.status_code == 200:

                st.success(
                    f"{dosage:.0f} ml spray command sent!"
                )

                time.sleep(0.5)

                st.rerun()

            elif response.status_code == 409:

                st.warning(
                    "A spray operation is already running."
                )

            else:

                st.error(
                    response.text
                )

        except Exception as e:

            st.error(
                f"Backend connection failed: {e}"
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# SPRAY STATUS
# =========================================================

st.markdown(
    """
    <div class="status-card">
        <div class="card-title">
            📡 Spray Status
        </div>
    """,
    unsafe_allow_html=True
)


if state:

    current_status = state.get(
        "status",
        "Ready"
    )

    sprayed_amount = state.get(
        "sprayed_amount",
        0
    )

    if current_status == "Ready":

        st.markdown(
            """
            <div class="status-ready">
                🟢 Ready
            </div>

            <div class="status-description">
                System is ready for spraying
            </div>
            """,
            unsafe_allow_html=True
        )

    elif current_status == "Spraying...":

        st.markdown(
            """
            <div class="status-ready">
                🟡 Spraying...
            </div>

            <div class="status-description">
                Pump is currently dispensing
            </div>
            """,
            unsafe_allow_html=True
        )

    elif current_status == "Completed":

        st.markdown(
            f"""
            <div class="status-ready">
                🟢 Completed
            </div>

            <div class="status-description">
                {sprayed_amount:.2f} ml sprayed
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="status-ready">
                {current_status}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.error(
        "Backend unavailable"
    )


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        CropIQ • Raspberry Pi Precision Spraying
    </div>
    """,
    unsafe_allow_html=True
)
