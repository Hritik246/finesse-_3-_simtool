import matplotlib.pyplot as plt

def plot_scan(df, png_path, title=\"Scan\"):
    plt.figure()
    # auto-detect columns
    xcol = df.columns[0]
    ycol = df.columns[1] if len(df.columns) > 1 else None
    if ycol is not None:
        plt.plot(df[xcol], df[ycol])
        plt.xlabel(xcol)
        plt.ylabel(ycol)
    else:
        plt.plot(df.index, df[xcol])
        plt.xlabel(\"index\")
        plt.ylabel(xcol)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(png_path)
    plt.close()
