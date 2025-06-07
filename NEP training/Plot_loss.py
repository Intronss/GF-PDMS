from pylab import *

##set figure properties
aw = 1.5
fs = 16
lw = 2.0
font = {'size': fs}
matplotlib.rc('font', **font)
matplotlib.rc('axes', linewidth=aw)


def set_fig_properties(ax_list):
    tl = 8
    tw = 1.5
    tlm = 4

    for ax in ax_list:
        ax.tick_params(which='major', length=tl, width=tw)
        ax.tick_params(which='minor', length=tlm, width=tw)
        ax.tick_params(which='both', axis='both', direction='out', right=False, top=False)


loss = loadtxt('./loss.out')
loss[:, 0] = np.arange(1, len(loss) + 1) * 100
print(loss[-1, 0])
energy_train = loadtxt('./energy_train.out')
energy_test = loadtxt('./energy_test.out')
force_train = loadtxt('./force_train.out')
force_test = loadtxt('./force_test.out')

figure(figsize=(14, 8))
subplot(1, 2, 1)
set_fig_properties([gca()])
loglog(loss[:, 0] / 100, loss[:, 1], lw=lw, c="C0", label="Total")
loglog(loss[:, 0] / 100, loss[:, 2], lw=lw, c="C1", label="L1-regularization")
loglog(loss[:, 0] / 100, loss[:, 3], lw=lw, c="C2", label="L2-regularization")
loglog(loss[:, 0] / 100, loss[:, 4], lw=lw, c="C3", label="Energy-train")
loglog(loss[:, 0] / 100, loss[:, 5], lw=lw, c="C4", label="Force-train")
loglog(loss[:, 0] / 100, loss[:, 7], lw=lw, c="C5", label="Energy-test")
loglog(loss[:, 0] / 100, loss[:, 8], lw=lw, c="C6", label="Force-test")
legend()
xlabel('Generation/100')
ylabel('Loss')

subplot(2, 2, 2)
set_fig_properties([gca()])
plot(energy_train[:, 1], energy_train[:, 0], '.', c="C0", ms=10, label="Train")
plot(energy_test[:, 1], energy_test[:, 0], '.', c="C1", ms=10, label="Test")
plot(linspace(-8.9, -8.4), linspace(-8.9, -8.4), '-')
legend()
xlabel('DFT energy (eV/atom)')
ylabel('NEP energy (eV/atom)')

subplot(2, 2, 4)
set_fig_properties([gca()])
plot(force_train[:, 3:6].flatten(), force_train[:, 0:3].flatten(), '.', c="C2", ms=10, label="Train")
plot(force_test[:, 3:6].flatten(), force_test[:, 0:3].flatten(), '.', c="C3", ms=10, label="Test")
plot(linspace(-100, 100), linspace(-100, 100), '-')
legend()
xlabel(r'DFT force (eV/$\rm{\AA}$)')
ylabel(r'NEP force (eV/$\rm{\AA}$)')

subplots_adjust(wspace=0.35, hspace=0.3)
savefig("Loss.png", bbox_inches='tight')
