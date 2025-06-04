import matplotlib.pyplot as plt
import random
import csv
from scipy.stats import sem
from scipy.stats import bootstrap
import numpy as np
import scipy

plt.rcParams.update({'axes.labelsize': 15})
plt.rcParams.update({'xtick.labelsize': 15})
plt.rcParams.update({'ytick.labelsize': 15})

def get_mean(v, x):
    return np.mean(v)

filenames = ["results_human.csv"] # names of files containing the results

tags = ["deepl","george","tieck","regis","wolff","walesrode"] # the tags of the relevant conditions in the result files
markers = ["o","o","o","o","o","o"] # markers (for average values)
colors = ["black","indigo","dodgerblue","crimson","limegreen","sienna"]

type = "average_values" # "average_values" or "points", depending on whether averages or individual poems shall be visualized
plot_besides = True # plot metre and rhyme next to each other

results = []
for fn in filenames:
    for l in csv.reader(open(f"{fn}","r")):
        if 'None' not in l: # unless the metre is undefined
            results.append([l[0], int(l[1]), float(l[2]), float(l[3]), float(l[4])])
# convert to dictionary
data = {} # dictionary with lists of triples as values: key: tag, value: [(Bert score, metre, rhyme)]
for tag in tags:
    data[tag] = []
for r in results:
    if r[0] in tags:
        data[r[0]].append((r[2],r[3],r[4]))

if plot_besides:
    plt.subplots(1, 2)
    plt.subplot(1, 2, 1)

if type == "average_values":
    # get average values and bootstrap confidence intervals
    means_bert = [np.mean([r[0] for r in data[c]]) for c in tags]
    means_metre = [np.mean([r[1] for r in data[c]]) for c in tags]
    means_rhyme = [np.mean([r[2] for r in data[c]]) for c in tags]
    boot_bert = [bootstrap(([r[0] for r in data[c]], [0 for r in data[c]]), get_mean, method="basic") for c in tags]
    boot_metre = [bootstrap(([r[1] for r in data[c]], [0 for r in data[c]]), get_mean, method="basic") for c in tags]
    boot_rhyme = [bootstrap(([r[2] for r in data[c]], [0 for r in data[c]]), get_mean, method="basic") for c in tags]

    plt.gca().invert_xaxis()

    # visualize metrical distance
    for i in range(len(tags)):
        metre_mean = np.mean(boot_metre[i].bootstrap_distribution)
        bert_mean = np.mean(boot_bert[i].bootstrap_distribution)
        xerr = [[metre_mean - boot_metre[i].confidence_interval[0]], [boot_metre[i].confidence_interval[1] - metre_mean]]
        yerr = [[bert_mean - boot_bert[i].confidence_interval[0]], [boot_bert[i].confidence_interval[1] - bert_mean]]
        plt.errorbar(metre_mean, bert_mean, xerr=xerr, yerr=yerr, fmt=markers[i], color=colors[i])
        plt.ylabel("BERTScore")
        plt.xlabel("Metrical distance")
    if not plot_besides:
        plt.show()
    else:
        plt.subplot(1, 2, 2)

    # visualize rhyme scheme similarities
    for i in range(len(tags)):
        rhyme_mean = np.mean(boot_rhyme[i].bootstrap_distribution)
        bert_mean = np.mean(boot_bert[i].bootstrap_distribution)
        xerr = [[rhyme_mean - boot_rhyme[i].confidence_interval[0]], [boot_rhyme[i].confidence_interval[1] - rhyme_mean]]
        yerr = [[bert_mean - boot_bert[i].confidence_interval[0]], [boot_bert[i].confidence_interval[1] - bert_mean]]
        plt.errorbar(rhyme_mean, bert_mean, xerr=xerr, yerr=yerr, fmt=markers[i], color=colors[i])
        plt.ylabel("BERTScore")
        plt.xlabel("Rhyme scheme similarity")
    plt.show()

elif type == "points":
    plt.gca().invert_xaxis()

    # visualize metrical distance
    for i in range(len(tags)):
        plt.scatter([x[1] for x in data[tags[i]]], [y[0] for y in data[tags[i]]], c=colors[i], marker='.')
        plt.ylabel("BERTScore")
        plt.xlabel("Metrical distance")

    if not plot_besides:
        plt.show()
    else:
        plt.subplot(1, 2, 2)

    # visualize rhyme scheme similarity
    for i in range(len(tags)):
        plt.scatter([x[2]+random.randrange(-10,10)/1000 for x in data[tags[i]]], [y[0] for y in data[tags[i]]], c=colors[i], marker='.')
        plt.ylabel("BERTScore")
        plt.xlabel("Rhyme scheme similarity")
    plt.show()