"""Diagnostic and presentation figures, from saved simulation output."""
import csv
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/unit2-matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from .simulation import ROOT
from .analyze import load_raw

LABELS = {"normal":"Normal", "student_t3":"Student t (3 df)", "contaminated_normal":"5% contaminated normal"}

def main():
    out = ROOT / "results/figures"
    out.mkdir(parents=True,exist_ok=True)
    groups = load_raw()
    with (ROOT / "results/raw/summary.csv").open() as f:
        rows = list(csv.DictReader(f))
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,"figure.dpi":150})
    fig, axes = plt.subplots(1,3,figsize=(12,3.8),sharey=True)
    for ax,(distribution,label) in zip(axes,LABELS.items()):
        for method,color in [("mean","#2166ac"),("median","#b2182b")]:
            subset=sorted([r for r in rows if r["distribution"]==distribution and r["method"]==method],key=lambda r:int(r["n"]))
            n=np.array([int(r["n"]) for r in subset])
            mse=np.array([float(r["mse"]) for r in subset])
            se=np.array([float(r["mse_mcse"]) for r in subset])
            ax.errorbar(n,n*mse,yerr=1.96*n*se,label=method.title(),color=color,marker="o",capsize=4)
        ax.axhline(1,color="gray",ls=":",lw=1,label="Mean theory: n × MSE = 1")
        ax.set(xscale="log",xticks=[20,100,500],xticklabels=[20,100,500],xlabel="Sample size n",title=label)
    axes[0].set_ylabel("n × mean squared error")
    axes[-1].legend(fontsize=8)
    fig.suptitle("Location estimation at equal population variance (10,000 replicates per condition)")
    fig.text(.5,.01,"Bars: ±1.96 Monte Carlo standard errors; heavy-tail MSE uncertainty may be unstable.",ha="center",fontsize=9)
    fig.tight_layout(rect=[0,.05,1,.94])
    fig.savefig(out/"performance.png")
    fig.savefig(out/"performance.pdf")
    plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(12,3.8),sharey=True)
    for ax,(distribution,label) in zip(axes,LABELS.items()):
        values=[groups[(distribution,20,m)] for m in ["mean","median"]]
        ax.boxplot(values,tick_labels=["Mean","Median"],showfliers=True,flierprops={"markersize":2,"alpha":.25})
        ax.axhline(0,color="gray",ls="--",lw=1)
        ax.set_title(label)
    axes[0].set_ylabel("Estimated location (true value = 0)")
    fig.suptitle("Diagnostic: sampling distributions at n = 20 (10,000 replicates)")
    fig.text(.5,.01,"Boxes: middle 50%; line: median; whiskers: 1.5 IQR; points: observations beyond whiskers.",ha="center",fontsize=9)
    fig.tight_layout(rect=[0,.05,1,.94])
    fig.savefig(out/"diagnostic.png")
    plt.close(fig)

if __name__ == "__main__":
    main()
