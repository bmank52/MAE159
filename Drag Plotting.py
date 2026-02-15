from drag_constant_Cdo import drag_constant_Cdo
from Calc_CDo import calc_CD0
from matplotlib import pyplot as plt
from Resize_Geometry import resize_geometry
from Resize_Engine import resize_engine
from Mdd_constraint import Mdd_constraint
import numpy as np

h = 35000
M = .85
sweep = 40
W = 393665
T_W = .31
AR = 8
W_S = 141
sweep = 40

S_ref, mac, b_ref, Cr, Ct, mac_quarter_c, L_f, D_f =resize_geometry(W, W_S, AR,sweep,  250, 0.35)
T_SLSD = resize_engine(W, T_W)
t2c, CL_max_LND, CL_max_TO, CL_max_clean = Mdd_constraint(W_S, M, h, sweep, AR)
print(t2c, CL_max_LND, CL_max_TO, CL_max_clean)

CDo = calc_CD0(h, M, L_f, D_f, S_ref, mac, sweep, t2c, T_SLSD)

plt.close('all')

# Define your configurations
configs = [
    ('Clean', False, False, CL_max_clean, 'blue'),
    ('Takeoff', True, 'TO', CL_max_TO, 'orange'),
    ('Landing', True, 'LND', CL_max_LND, 'green')
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

for label, gear, flaps, cl_limit, color in configs:
    # Ensure cl_limit is a standard float
    limit = float(cl_limit)

    # A. Generate the parabolic curve data
    cl_range = np.linspace(0.01, limit, 100)
    cd_vals = []

    for cl in cl_range:
        res = drag_constant_Cdo(cl, limit, AR, gear, flaps, M, 0.85, CDo)

        # FIX: res[0] might be a numpy array. We use np.ravel to flatten it
        # and take the first item to ensure it is a scalar.
        cd_scalar = np.ravel(res[0])[0]
        cd_vals.append(cd_scalar)

    # Convert lists to clean 1D numpy arrays for plotting
    cl_curve = np.array(cl_range)
    cd_curve = np.array(cd_vals)

    # B. Define the "Cap" values for Figure 8
    cd_last_val = cd_curve[-1]

    # C. Plot CL vs CD (Figure 8 style)
    # 1. Plot the parabolic portion
    ax1.plot(cd_curve, cl_curve, color=color, label=label, linewidth=2)
    # 2. Plot the horizontal line from CD_at_max_CL to the plot edge (1.4)
    ax1.plot([cd_last_val, 1.4], [limit, limit], color=color, linewidth=2)

    # D. Plot L/D vs CL (Figure 9 style)
    ld_curve = cl_curve / cd_curve
    # 1. Plot the efficiency curve
    ax2.plot(cl_curve, ld_curve, color=color, label=label, linewidth=2)
    # 2. Plot the vertical drop to zero at exactly the CL limit
    ax2.plot([limit, limit], [ld_curve[-1], 0], color=color, linewidth=2)

# --- Final Formatting to match your reference exactly ---
ax1.set_title('Figure 8: Polars by Configuration')
ax1.set_xlabel('CD')
ax1.set_ylabel('CL')
ax1.set_xlim(0, 1.4)
ax1.set_ylim(0, 3.5)
ax1.legend()
ax1.grid(True, linestyle=':', alpha=0.6)

ax2.set_title('Figure 9: L/D by Configuration')
ax2.set_xlabel('CL')
ax2.set_ylabel('L/D')
ax2.set_xlim(0, 3.5)
ax2.set_ylim(0, 20.0)
ax2.legend()
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()