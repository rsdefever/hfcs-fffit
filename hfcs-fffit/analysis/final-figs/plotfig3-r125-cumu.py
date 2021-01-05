import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn

sys.path.append("../")

from utils.r125 import R125Constants
from utils.id_new_samples import prepare_df_vle
from utils.analyze_samples import prepare_df_vle_errors

R125 = R125Constants()

matplotlib.rc("font", family="sans-serif")
matplotlib.rc("font", serif="Arial")

############################# QUANTITIES TO EDIT #############################
##############################################################################

iternum = 5

##############################################################################
##############################################################################

csv_path = "../csv/"
in_csv_names = [
    "r125-vle-iter" + str(i) + "-results.csv" for i in range(1, iternum + 1)
]

# Read files
df_csvs = [
    pd.read_csv(csv_path + in_csv_name, index_col=0)
    for in_csv_name in in_csv_names
]
dfs = [prepare_df_vle(df_csv, R125) for df_csv in df_csvs]


def main():

    # Create a dataframe with one row per parameter set
    dfs_paramsets = [prepare_df_vle_errors(df, R125) for df in dfs]

    names = {
        "mape_liq_density": "Liquid density",
        "mape_vap_density": "Vapor density",
        "mape_Pvap": "Vapor pressure",
        "mape_Hvap": "Enthalpy of vaporization",
        "mape_Tc": "Critical temperature",
        "mape_rhoc": "Critical density",
    }

    # Plot MAPE sorted by each property
    fig, axes = plt.subplots(6, 1, figsize=(4,7))
    piter=0
    for name, label in names.items():
        axes[piter].plot(
            dfs_paramsets[0].sort_values(name)[name],
            np.arange(1, 26,1),
            '-o',
            markersize=4,
            alpha=0.8,
            label="VLE-1",
        )
        axes[piter].plot(
            dfs_paramsets[1].sort_values(name)[name],
            np.arange(1, 26, 1),
            '-o',
            markersize=4,
            alpha=0.8,
            label="VLE-2",
        )
        axes[piter].plot(
            dfs_paramsets[2].sort_values(name)[name],
            np.arange(1, 26, 1),
            '-o',
            markersize=4,
            alpha=0.8,
            label="VLE-3",
        )
        axes[piter].plot(
            dfs_paramsets[3].sort_values(name)[name],
            np.arange(1, 26, 1),
            '-o',
            markersize=4,
            alpha=0.8,
            label="VLE-4",
        )
        axes[piter].plot(
            dfs_paramsets[4].sort_values(name)[name],
            np.arange(1, 26, 1),
            '-o',
            markersize=4,
            alpha=0.8,
            label="VLE-5",
        )
        axes[piter].text(
            19.6, 1.0,
            label,
            verticalalignment="bottom",
            horizontalalignment="right",
            fontsize=13
        )
        axes[piter].set_ylim(0,25)
        axes[piter].set_xlim(0,20)
        axes[piter].set_yticks([0,10,20])
        axes[piter].set_yticks([5,15], minor=True)
        axes[piter].set_xticks([0,5,10,15,20])
        axes[piter].set_xticks([1,2,3,4,6,7,8,9,11,12,13,14,16,17,18,19], minor=True)
        axes[piter].tick_params("both", direction="in", which="both", labelbottom=False, length=1.5, labelsize=12)
        axes[piter].tick_params("both", which="major", length=3)
        axes[piter].xaxis.set_ticks_position("both")
        axes[piter].yaxis.set_ticks_position("both")
        piter +=1

    text = axes[5].set_ylabel("Cumulative number parameter sets", fontsize=16, labelpad=15)
    text.set_y(3)
    axes[5].set_xlabel("Mean abs. % error", fontsize=16, labelpad=10)
    axes[5].tick_params(labelbottom=True)
    plt.subplots_adjust(hspace=.0)
    plt.subplots_adjust(left = 0.18, right=0.92, top=0.84)
    axes[0].legend(fontsize=12, loc=(0.21,1.05), ncol=2)
    fig.savefig("pdfs/fig3_r125-cumu.pdf")

if __name__ == "__main__":
    main()