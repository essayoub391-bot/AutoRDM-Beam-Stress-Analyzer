import numpy as np
import matplotlib.pyplot as plt

# Material Yield Strength Database (MPa)
MATERIALS = {
    "Structural_Steel_S235": {"name": "Structural Steel (S235)", "yield": 235.0},
    "Structural_Steel_S355": {"name": "Structural Steel (S355)", "yield": 355.0},
    "Aluminum_6061_T6": {"name": "Aluminum (6061-T6)", "yield": 276.0},
    "Cast_Iron": {"name": "Cast Iron", "yield": 150.0}
}

def analyze_advanced_beam(length, point_loads, q_load, width, height, material_key="Aluminum_6061_T6"):
    x = np.linspace(0, length, 1000)
    
    # 1. Reaction Forces
    total_point_force = sum([f for f, p in point_loads])
    total_q_force = q_load * length
    
    moment_about_r1 = sum([f * p for f, p in point_loads]) + (q_load * length * (length / 2.0))
    R2 = moment_about_r1 / length
    R1 = (total_point_force + total_q_force) - R2
    
    # 2. Shear Force & Bending Moment Diagrams
    shear_force = np.zeros_like(x)
    bending_moment = np.zeros_like(x)
    
    for i, xi in enumerate(x):
        V = R1 - (q_load * xi)
        for f, p in point_loads:
            if xi >= p:
                V -= f
        shear_force[i] = V
        
        M = (R1 * xi) - (q_load * (xi ** 2) / 2.0)
        for f, p in point_loads:
            if xi >= p:
                M -= f * (xi - p)
        bending_moment[i] = M
        
    max_moment = np.max(bending_moment)
    max_moment_pos = x[np.argmax(bending_moment)]
    
    # 3. Mechanical & Stress Calculations
    I = (width * (height ** 3)) / 12.0
    y = height / 2.0
    sigma_max_pa = (max_moment * y) / I
    sigma_max_mpa = sigma_max_pa / 1e6
    
    mat = MATERIALS.get(material_key, MATERIALS["Aluminum_6061_T6"])
    sigma_yield = mat["yield"]
    FoS = sigma_yield / sigma_max_mpa if sigma_max_mpa > 0 else float('inf')
    is_safe = FoS >= 1.5
    
    # 4. English Console Output
    print("==================================================")
    print("       AutoRDM - Structural Analysis Report       ")
    print("==================================================")
    print(f"* Selected Material : {mat['name']}")
    print(f"* Material Yield Strength (σy) : {sigma_yield:.1f} MPa")
    print(f"* Left Reaction Force (R1)     : {R1:.2f} N")
    print(f"* Right Reaction Force (R2)    : {R2:.2f} N")
    print(f"* Max Bending Moment (M_max)   : {max_moment:.2f} N.m (at x = {max_moment_pos:.2f} m)")
    print(f"* Max Normal Stress (σ_max)    : {sigma_max_mpa:.2f} MPa")
    print(f"* Factor of Safety (FoS)       : {FoS:.2f}")
    status_str = "SAFE (Acceptable FoS)" if is_safe else "UNSAFE (Structural Risk)"
    print(f"* Mechanical Verdict           : [{status_str}]")
    print("==================================================")
    
    # 5. Plotting Diagrams
    plt.figure(figsize=(10, 6))
    
    # SFD
    plt.subplot(2, 1, 1)
    plt.plot(x, shear_force, color='navy', linewidth=1.5, label='SFD')
    plt.fill_between(x, shear_force, color='navy', alpha=0.1)
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.title("Shear Force Diagram (SFD)", fontsize=11, fontweight='bold')
    plt.ylabel("Shear Force (N)")
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # BMD
    plt.subplot(2, 1, 2)
    plt.plot(x, bending_moment, color='crimson', linewidth=1.5, label='BMD')
    plt.fill_between(x, bending_moment, color='crimson', alpha=0.1)
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    status_text = "SAFE" if is_safe else "UNSAFE"
    plt.title(f"Bending Moment Diagram (BMD) - Status: {status_text} (FoS={FoS:.2f})", fontsize=11, fontweight='bold')
    plt.xlabel("Beam Length (m)")
    plt.ylabel("Moment (N.m)")
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig("advanced_beam_analysis.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    analyze_advanced_beam(
        length=5.0,
        point_loads=[(1200.0, 1.5), (800.0, 3.5)],
        q_load=300.0,
        width=0.08,
        height=0.15,
        material_key="Aluminum_6061_T6"
    )
