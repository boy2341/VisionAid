import streamlit as st
import numpy as np
from PIL import Image
import base64

# 1. PAGE CONFIG (Must be the very first Streamlit command)
st.set_page_config(page_title="VisionAid Pro", layout="wide")

# 2. DESIGN & THEME UTILITIES
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_design_theme(image_file, sidebar_opacity):
    bin_str = get_base64(image_file)
    # Convert slider 0-100 to 0.0-1.0 for CSS
    op = sidebar_opacity / 100.0
    
    style = f"""
    <style>
    /* Main App Background */
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 15, 20, {op}) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}

    /* Main Content Glassmorphism Container */
    .reportview-container .main .block-container {{
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 100px;
        margin-top: 20px;
    }}

    /* Center and Style Titles */
    h1, h2, h3 {{
        text-align: center !important;
        color: #00d4ff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }}
    
    .stMarkdown p, label {{
        color: white !important;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# 3. ADVANCED IMAGE PROCESSING
def process_vision(image, cvd_type, gamma, contrast, brightness):
    # Convert to float and normalize
    img_array = np.array(image).astype(float) / 255.0
    
    # Linearize (Gamma Removal)
    img_linear = np.power(img_array, gamma)
    
    # CVD Transformation Matrices
    matrices = {
        "Protanopia": np.array([[0.567, 0.433, 0], [0.558, 0.442, 0], [0, 0.242, 0.758]]),
        "Deuteranopia": np.array([[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.3, 0.7]]),
        "Tritanopia": np.array([[0.95, 0.05, 0], [0, 0.433, 0.567], [0, 0.475, 0.525]]),
        "Achromatopsia": np.array([[0.299, 0.587, 0.114], [0.299, 0.587, 0.114], [0.299, 0.587, 0.114]])
    }
    
    # Apply CVD Matrix
    M = matrices[cvd_type]
    converted = img_linear @ M.T
    
    # Apply Brightness
    converted = converted * brightness
    
    # Apply Contrast Adjustment
    mean = np.mean(converted)
    converted = (converted - mean) * contrast + mean
    
    # Re-apply Gamma & Clip
    converted = np.power(np.clip(converted, 0, 1), 1/gamma)
    return (converted * 255).astype(np.uint8)

# 4. SIDEBAR UI
with st.sidebar:
    st.header("🎨 Theme & UI")
    # Change 'bg.jpg' to your actual file path
    try:
        side_op = st.slider("Sidebar Opacity", 0, 100, 40)
        set_design_theme('bg.jpg', side_op)
    except FileNotFoundError:
        st.warning("Background image 'bg.jpg' not found. Please add it to your folder.")

    st.header("⚙️ Simulation Settings")
    uploaded_file = st.file_uploader("Upload Image Assets", type=['png', 'jpg', 'jpeg'])
    
    st.markdown("---")
    cvd = st.selectbox("Deficiency Type", ["Protanopia", "Deuteranopia", "Tritanopia", "Achromatopsia"])
    
    st.subheader("Fine-Tuning")
    gamma_v = st.slider("Gamma Correction", 1.0, 3.0, 2.2)
    bright_v = st.slider("Brightness", 0.5, 2.0, 1.0)
    contrast_v = st.slider("Contrast Boost", 0.5, 2.0, 1.0)

# 5. MAIN DISPLAY LOGIC
st.markdown("<h1>VisionAid Pro: Advanced CVD Diagnostic</h1>", unsafe_allow_html=True)

if uploaded_file:
    original = Image.open(uploaded_file).convert("RGB")
    
    # Process image with all parameters
    final_output = process_vision(original, cvd, gamma_v, contrast_v, bright_v)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3>Standard Vision</h3>", unsafe_allow_html=True)
        st.image(original, use_container_width=True)
        
    with col2:
        st.markdown(f"<h3>{cvd} Simulation</h3>", unsafe_allow_html=True)
        st.image(final_output, use_container_width=True)

    # Download Button
    st.markdown("---")
    res_img = Image.fromarray(final_output)
    st.download_button(
        label="Download Analysis Report", 
        data=res_img.tobytes(), 
        file_name=f"vision_aid_{cvd.lower()}.png", 
        mime="image/png"
    )
else:
    st.markdown(
    """
    <p style='text-align: center; color: #00d4ff; font-weight: bold; font-size: 18px;'>
        Waiting for image assets in the sidebar...
    </p>
    """, 
    unsafe_allow_html=True
    )