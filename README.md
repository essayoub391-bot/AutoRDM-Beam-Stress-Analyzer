# AutoRDM-Beam-Stress-Analyzer
Automated Mechanical Beam Analysis
# 🛠️ AutoRDM: Automated Structural & Stress Analysis Tool

**AutoRDM** is an engineering automation tool built in Python to perform real-time structural analysis on mechanical beams. It calculates internal forces, checks material yield limits, and generates interactive Shear Force Diagrams (SFD) and Bending Moment Diagrams (BMD).

---

## ✨ Key Features
* **Multi-Load Support:** Handles point loads alongside uniform distributed loads ($q$).
* **Material Failure Assessment:** Compares maximum bending stress ($\sigma_{max}$) against yield strength ($\sigma_y$) to compute the **Factor of Safety (FoS)**.
* **Integrated Material Database:** Built-in yield properties for Structural Steel (S235/S355), Aluminum 6061-T6, and Cast Iron.
* **Automated Visual Reports:** Generates interactive matplotlib plots displaying structural safety status (`SAFE` / `UNSAFE`).

---

## 📐 Governing Engineering Equations

1. **Bending Stress Equation:**
   $$\sigma = \frac{M \cdot y}{I}$$

2. **Area Moment of Inertia (Rectangular Section):**
   $$I = \frac{b \cdot h^3}{12}$$

3. **Factor of Safety (FoS):**
   $$\text{FoS} = \frac{\sigma_{\text{yield}}}{\sigma_{\text{max}}}$$

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/AutoRDM-Beam-Stress-Analyzer.git](https://github.com/YOUR_USERNAME/AutoRDM-Beam-Stress-Analyzer.git)
