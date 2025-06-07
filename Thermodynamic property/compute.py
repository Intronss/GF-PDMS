"""
Select structures
===========================

This example shows how to select structures from dataset
"""
from pylab import *
from ase.build import graphene_nanoribbon
from ase.io import read, write
from gpyumd.atoms import GpumdAtoms
from gpyumd.load import load_shc, load_compute

aw = 2
fs = 16
font = {'size': fs}
matplotlib.rc('font', **font)
matplotlib.rc('axes', linewidth=aw)


def set_fig_properties(ax_list):
    tl = 8
    tw = 2
    tlm = 4

    for ax in ax_list:
        ax.tick_params(which='major', length=tl, width=tw)
        ax.tick_params(which='minor', length=tlm, width=tw)
        ax.tick_params(axis='both', direction='in', right=True, top=True)


compute = load_compute(['temperature'])
compute.keys()

T = compute['temperature']
Ein = compute['Ein']
Eout = compute['Eout']
ndata = T.shape[0]
a = int(ndata / 2)
abc = T[a + 1:, 1:]
b = mean(abc, axis=0)
temp_ave = mean(T[int(ndata / 2) + 1:, 1:], axis=0)

dt = 0.001  # ps 
Ns = 1000  # Sample interval
bb = np.arange(1, ndata + 1)
t = dt * np.arange(1, ndata + 1) * Ns / 1000  # ns

figure(figsize=(10, 5))
subplot(1, 2, 1)
set_fig_properties([gca()])
group_idx = range(0, 3)
plot(group_idx, temp_ave, linewidth=3, marker='o', markersize=10)
xlim([0, 3])
gca().set_xticks(group_idx)
ylim([270, 330])
gca().set_yticks(range(270, 330, 5))
xlabel('group index')
ylabel('T (K)')
title('(a)')

subplot(1, 2, 2)
set_fig_properties([gca()])
plot(t, Ein / 1000, 'C3', linewidth=3)
plot(t, Eout / 1000, 'C0', linewidth=3, linestyle='--')
xlim([0, 3])
gca().set_xticks(linspace(0, 2, 6))
ylim([-15, 15])
gca().set_yticks(range(-15, 15, 3))
xlabel('t (ns)')
ylabel('Heat (keV)')
title('(b)')
tight_layout()
show()

deltaT = temp_ave[0] - temp_ave[-1]  # [K]
new_t = temp_ave[1] - temp_ave[-2]
Q1 = (Ein[0] - Ein[-1]) / (ndata) / dt / Ns
Q2 = (Eout[-1] - Eout[0]) / (ndata) / dt / Ns
Q = mean([Q1, Q2])  # [eV/ps]

A = 18.459 * 13.503 / 100  # [nm2]
G = 160 * Q / deltaT / A  # [GW/m2/K]
k = G * 1.149
# k1 = 160 * Q / A / (new_t / 2.8)
print(G, k)

# shc = load_shc(250, 1000)['run0']
# shc.keys()

# Ly = split[5]-split[4]
# Lx, Lz = 32, 32
# V = Lx*Ly*Lz
# Gc = 1.6e4*(shc['jwi']+shc['jwo'])/V/deltaT
# figure(figsize=(10,5))
# subplot(1,2,1)
# set_fig_properties([gca()])
# plot(shc['t'], (shc['Ki']+shc['Ko'])/Ly, linewidth=2)
# xlim([-0.5, 0.5])
# gca().set_xticks([-0.5, 0, 0.5])
# ylim([-1, 1])
# gca().set_yticks(range(-1,2,2))
# ylabel('K (eV/ps)')
# xlabel('Correlation time (ps)')
# title('(a)')

# subplot(1,2,2)
# set_fig_properties([gca()])
# plot(shc['nu'], Gc, linewidth=2)
# xlim([0, 50])
# gca().set_xticks(range(0,51,10))
# ylim([0, 0.01])
# gca().set_yticks(linspace(0,0.01,5))
# ylabel(r'$G$($\omega$) (GW/m$^2$/K/THz)')
# xlabel(r'$\omega$/2$\pi$ (THz)')
# title('(b)')
# tight_layout()
# show()
