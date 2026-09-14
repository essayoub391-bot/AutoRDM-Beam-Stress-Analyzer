import matplotlib.pyplot as plt
import numpy as np

# 1. قاعدة بيانات المواد الميكانيكية (حد الخضوع MPa)
MATERIALS = {
    "Steel_S235": {"name": "صلب إنشائي (Steel S235)", "yield_strength": 235.0},
    "Steel_S355": {"name": "صلب عالي المقاومة (Steel S355)", "yield_strength": 355.0},
    "Aluminum_6061_T6": {"name": "ألمنيوم (Alloy 6061-T6)", "yield_strength": 276.0},
    "Cast_Iron": {"name": "حديد زهر (Gray Cast Iron)", "yield_strength": 130.0}
}


def analyze_advanced_beam(length: float, point_loads: list, q_load: float,
                          width: float, height: float, material_key: str):
    """
    أداة تحليل الجوائز والإجهادات الميكانيكية المتقدمة
    - length: طول الجائز (m)
    - point_loads: قائمة القوى المركزة [(القوة_N, الموضع_m), ...]
    - q_load: الحمل الموزع بانتظام (N/m)
    - width (b): عرض المقطع المستطيل (m)
    - height (h): ارتفاع المقطع المستطيل (m)
    - material_key: اسم المادة من قاعدة البيانات
    """
    x = np.linspace(0, length, 1000)
    dx = length / 1000

    # --- حساب ردود الأفعال (Reactions R1 & R2) ---
    # عزوم الأحمال المركزة حول R1
    moments_point = sum(f * p for f, p in point_loads)
    total_point_force = sum(f for f, p in point_loads)

    # عزم وقوة الحمل الموزع q
    total_q_force = q_load * length
    moment_q = total_q_force * (length / 2.0)

    # ردود الأفعال
    R2 = (moments_point + moment_q) / length
    R1 = (total_point_force + total_q_force) - R2

    # --- حساب مخطط القص والعزم (SFD & BMD) ---
    shear_force = np.zeros_like(x)
    bending_moment = np.zeros_like(x)

    for i, xi in enumerate(x):
        # قوة القص عند x
        V = R1 - (q_load * xi)
        for f, p in point_loads:
            if xi >= p:
                V -= f
        shear_force[i] = V

        # عزم الانحناء عند x
        M = (R1 * xi) - (q_load * (xi ** 2) / 2.0)
        for f, p in point_loads:
            if xi >= p:
                M -= f * (xi - p)
        bending_moment[i] = M

    max_moment = np.max(bending_moment)
    max_moment_pos = x[np.argmax(bending_moment)]

    # --- الحسابات الميكانيكية والإجهاد ---
    I = (width * (height ** 3)) / 12.0  # Inertia (m^4)
    y = height / 2.0  # Distance to neutral axis (m)
    sigma_max_pa = (max_moment * y) / I  # Bending Stress (Pa)
    sigma_max_mpa = sigma_max_pa / 1e6  # (MPa)

    # جلب بيانات المادة وحساب معامل الأمان (Factor 
