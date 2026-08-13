import streamlit as st
import requests
import time


# =========================================================
# CONFIGURATION
# =========================================================

BACKEND_URL = "https://crop-iq-0gbw.onrender.com"


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CropIQ | Smart Spraying",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* ==============================
       GLOBAL
       ============================== */

    .stApp {
        background: #f4f7f3;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 25px;
        padding-bottom: 40px;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }


    /* ==============================
       HEADER
       ============================== */

    .topbar {
        background: #173b2b;
        padding: 20px 28px;
        border-radius: 18px;
        color: white;
        box-shadow: 0 6px 20px rgba(23,59,43,0.12);
        margin-bottom: 22px;
    }

    .brand {
        font-size: 30px;
        font-weight: 750;
        letter-spacing: -0.5px;
    }

    .brand span {
        color: #a8d96f;
    }

    .tagline {
        color: #cbd9ce;
        font-size: 14px;
        margin-top: 3px;
    }


    /* ==============================
       DEVICE STATUS
       ============================== */

    .device-status {
        background: #204b37;
        border: 1px solid #3d6a51;
        border-radius: 30px;
        padding: 10px 18px;
        text-align: center;
        color: #dff5e3;
        font-size: 14px;
        font-weight: 600;
        margin-top: 4px;
    }

    .green-dot {
        color: #8fe388;
        font-size: 18px;
    }


    /* ==============================
       SECTION LABEL
       ============================== */

    .section-label {
        color: #506357;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }


    /* ==============================
       CAMERA CARD
       ============================== */

    .camera-card {
        background: white;
        border-radius: 18px;
        padding: 18px;
        border: 1px solid #e0e8e1;
        box-shadow: 0 5px 18px rgba(25,60,35,0.06);
    }

    .camera-title {
        font-size: 21px;
        font-weight: 700;
        color: #183b2b;
        margin-bottom: 5px;
    }

    .camera-subtitle {
        color: #7b897f;
        font-size: 13px;
        margin-bottom: 15px;
    }


    /* ==============================
       CONTROL CARD
       ============================== */

    .control-card {
        background: white;
        border-radius: 18px;
        padding: 24px;
        border: 1px solid #e0e8e1;
        box-shadow: 0 5px 18px rgba(25,60,35,0.06);
        min-height: 420px;
    }

    .control-title {
        font-size: 21px;
        font-weight: 700;
        color: #183b2b;
    }

    .control-subtitle {
        color: #7b897f;
        font-size: 13px;
        margin-bottom: 25px;
    }


    /* ==============================
       DOSAGE DISPLAY
       ============================== */

    .dosage-display {
        background: #f1f7ed;
        border: 1px solid #d9e8d2;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin: 18px 0;
    }

    .dosage-number {
        font-size: 46px;
        font-weight: 750;
        color: #245c39;
        line-height: 1;
    }

    .dosage-unit {
        font-size: 16px;
        color: #71806f;
        margin-left: 5px;
    }

    .dosage-caption {
        color: #7b897f;
        font-size: 12px;
        margin-top: 8px;
    }


    /* ==============================
       STATUS CARD
       ============================== */

    .status-card {
        background: #173b2b;
        border-radius: 18px;
        padding: 22px 25px;
        color: white;
        margin-top: 22px;
        box-shadow: 0 6px 20px rgba(23,59,43,0.14);
    }

    .status-title {
        color: #b8cdbd;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        font-weight: 700;
    }

    .status-main {
        font-size: 28px;
        font-weight: 700;
        margin-top: 8px;
    }

    .status-detail {
        color: #cbd9ce;
        font-size: 13px;
        margin-top: 5px;
    }


    /* ==============================
       INFO CARDS
       ============================== */

    .info-card {
        background: white;
        border-radius: 15px;
        padding: 17px 20px;
        border: 1px solid #e0e8e1;
        box-shadow: 0 4px 15px rgba(25,60,35,0.04);
    }

    .info-label {
        color: #7b897f;
        font-size: 12px;
        margin-bottom: 5px;
    }

    .info-value {
        color: #183b2b;
        font-size: 21px;
        font-weight: 700;
    }


    /* ==============================
       SPRAY BUTTON
       ============================== */

    div.stButton > button {
        background: #2e7d46;
        color: white;
        border: none;
        border-radius: 12px;
        height: 58px;
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 0.3px;
        box-shadow: 0 5px 14px rgba(46,125,70,0.25);
        transition: 0.2s;
    }

    div.stButton > button:hover {
        background: #25683a;
        color: white;
        border: none;
        transform: translateY(-1px);
        box-shadow: 0 7px 18px rgba(46,125,70,0.30);
    }


    /* ==============================
       FOOTER
       ============================== */

    .footer {
        text-align: center;
        color: #89958d;
        font-size: 12px;
        padding-top: 28px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# BACKEND FUNCTIONS
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
        pass

    return None


def send_spray(amount):

    try:

        response = requests.post(
            BACKEND_URL + "/spray",
            json={
                "amount_ml": amount
            },
            timeout=15
        )

        return response

    except Exception:
        return None


# =========================================================
# GET STATE
# =========================================================

state = get_state()

if state:

    current_status = state.get(
        "status",
        "Ready"
    )

    sprayed_amount = state.get(
        "sprayed_amount",
        0
    )

else:

    current_status = "Offline"
    sprayed_amount = 0


# =========================================================
# HEADER
# =========================================================

header_left, header_right = st.columns(
    [5, 1]
)

with header_left:

    st.markdown(
        """
        <div class="topbar">
            <div class="brand">
                🌱 <span>Crop</span>IQ
            </div>

            <div class="tagline">
                Intelligent Crop Monitoring & Precision Spraying
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with header_right:

    if state:

        st.markdown(
            """
            <div class="device-status">
                <span class="green-dot">●</span>
                Raspberry Pi Online
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="device-status">
                ● Raspberry Pi Offline
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# MAIN AREA
# =========================================================

camera_col, control_col = st.columns(
    [1.55, 1],
    gap="large"
)


# =========================================================
# CAMERA
# =========================================================

with camera_col:

    st.markdown(
        '<div class="section-label">LIVE MONITORING</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="camera-card">
            <div class="camera-title">
                🌿 Plant Inspection
            </div>

            <div class="camera-subtitle">
                Latest image captured by the Raspberry Pi camera
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
                "Waiting for the Raspberry Pi camera..."
            )

    except Exception:

        st.warning(
            "Unable to retrieve plant image."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# SPRAY CONTROL
# =========================================================

with control_col:

    st.markdown(
        '<div class="section-label">SPRAY CONTROL</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="control-card">

            <div class="control-title">
                💧 Precision Dosage
            </div>

            <div class="control-subtitle">
                Set the required spray volume
            </div>
        """,
        unsafe_allow_html=True
    )

    dosage = st.number_input(
        "Dosage",
        min_value=1.0,
        max_value=500.0,
        value=25.0,
        step=1.0,
        label_visibility="collapsed"
    )

    st.markdown(
        f"""
        <div class="dosage-display">

            <div>
                <span class="dosage-number">
                    {dosage:.0f}
                </span>

                <span class="dosage-unit">
                    ml
                </span>
            </div>

            <div class="dosage-caption">
                TARGET SPRAY VOLUME
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if current_status == "Spraying...":

        st.button(
            "🚿  SPRAYING...",
            disabled=True,
            use_container_width=True
        )

    else:

        if st.button(
            "🚿  START SPRAY",
            use_container_width=True
        ):

            response = send_spray(dosage)

            if response is not None:

                if response.status_code == 200:

                    st.success(
                        f"{dosage:.0f} ml spray command sent."
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

            else:

                st.error(
                    "Unable to connect to CropIQ backend."
                )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# STATUS
# =========================================================

st.markdown(
    '<div class="section-label" style="margin-top:25px;">SYSTEM STATUS</div>',
    unsafe_allow_html=True
)


if current_status == "Ready":

    status_icon = "🟢"
    status_text = "Ready"
    status_detail = "System is ready for the next spray operation."

elif current_status == "Spraying...":

    status_icon = "🟡"
    status_text = "Spraying..."
    status_detail = "Pump is currently dispensing the requested volume."

elif current_status == "Completed":

    status_icon = "🟢"
    status_text = "Completed"
    status_detail = f"{sprayed_amount:.2f} ml successfully dispensed."

else:

    status_icon = "🔴"
    status_text = current_status
    status_detail = "Check the Raspberry Pi connection."


st.markdown(
    f"""
    <div class="status-card">

        <div class="status-title">
            Spray Operation
        </div>

        <div class="status-main">
            {status_icon} {status_text}
        </div>

        <div class="status-detail">
            {status_detail}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INFORMATION CARDS
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

info1, info2, info3 = st.columns(3)


with info1:

    st.markdown(
        f"""
        <div class="info-card">

            <div class="info-label">
                TARGET VOLUME
            </div>

            <div class="info-value">
                {dosage:.0f} ml
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with info2:

    st.markdown(
        f"""
        <div class="info-card">

            <div class="info-label">
                LAST DISPENSED
            </div>

            <div class="info-value">
                {sprayed_amount:.2f} ml
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with info3:

    connection_text = (
        "Connected"
        if state
        else "Offline"
    )

    st.markdown(
        f"""
        <div class="info-card">

            <div class="info-label">
                DEVICE STATUS
            </div>

            <div class="info-value">
                {connection_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        CropIQ • Raspberry Pi Precision Spraying System
    </div>
    """,
    unsafe_allow_html=True
)
