# VisionAid Pro: Advanced CVD Diagnostic Tool

VisionAid Pro is a specialized image processing application designed to simulate and analyze Color Vision Deficiency (CVD). Developed as a technical accessibility tool, it provides high-fidelity simulations of how digital content appears to individuals with various forms of color blindness, incorporating advanced optical physics like gamma correction and linear RGB transformations.

## Core Features

The application moves beyond basic color filtering by implementing a robust digital signal processing pipeline:

* **Multi-Type Simulation**: Accurate modeling of Protanopia, Deuteranopia, Tritanopia, and Achromatopsia.
* **Linearized Processing**: Converts standard sRGB images into linear space to perform mathematically accurate matrix transformations before re-encoding.
* **Fine-Tuning Controls**: Real-time adjustment of Gamma Correction, Brightness, and Contrast to simulate different viewing environments and display hardware.
* **Glassmorphism UI**: A modern, high-contrast interface designed for maximum readability against custom background textures.
* **Export Functionality**: Generate and download processed diagnostic reports for use in accessibility audits.

## Technical Implementation

### 1. Mathematical Transformation
The system utilizes industry-standard transformation matrices applied via NumPy's dot product operations. The simulation logic accounts for the confusion lines of the LMS color space, ensuring that the resulting visual output accurately represents the specific deficiency.

### 2. The Processing Pipeline
1.  **Normalization**: Input pixels are scaled to a [0, 1] range.
2.  **De-gamma**: Application of a power function to remove sRGB encoding.
3.  **Matrix Multiplication**: The linearized RGB vector is multiplied by the specific CVD matrix ($M$).
4.  **Signal Correction**: Brightness and contrast adjustments are applied to the transformed signal.
5.  **Re-gamma**: The signal is converted back to non-linear space for screen display.

## Installation

### Dependencies
Ensure you have the following requirements installed:
* streamlit
* numpy
* Pillow

### Running Locally
1.  Clone the repository and navigate to the project folder.
2.  Ensure `bg.jpg` (or your chosen background) is in the root directory.
3.  Execute the following command:
    ```bash
    streamlit run app.py
    ```

## Project Motivation
VisionAid was created to bridge the gap between engineering-grade color science and accessible web tools. By providing a platform where designers and developers can test their assets in real-time, the project aims to foster more inclusive digital design standards.
