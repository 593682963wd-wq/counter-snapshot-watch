from __future__ import annotations
import statistics,math

def median(vs):
    return statistics.median(vs) if vs else 0.0

def mad(vs, med=None):
    """Median Absolute Deviation —— 比标准差抗离群"""
    if not vs:
        return 0.0
    if med is None:
        med = statistics.median(vs)
    return statistics.median(abs(v - med) for v in vs)

def modified_z_score(value, vs):
    """Iglewicz & Hoaglin 修正 Z-score
    使用 MAD 代替 std；常数 0.6745 = ~Φ⁻¹(0.75)，使 MAD 近似为高斯分布的 σ
    """
    if len(vs) < 5:
        return 0.0
    med = statistics.median(vs)
    md = mad(vs, med)
    if md < 1e-9:
        # 历史几乎完全恒定，MAD 退化
        mean_abs_dev = sum(abs(v - med) for v in vs) / len(vs)
        if mean_abs_dev < 1e-9:
            # 历史完全恒定（如全是 +1）；此时任何明显偏离都是离群
            diff = value - med
            if abs(diff) < 0.5:
                return 0.0
            # 用 max(median,1) 做归一化，避免除 0
            return 10.0 * diff / max(abs(med), 1.0)
        return 0.7979 * (value - med) / mean_abs_dev
    return 0.6745 * (value - med) / md
