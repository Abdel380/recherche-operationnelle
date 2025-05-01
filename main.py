from function import *
from complexite import*

# Lecture du fichier contenant capacités et coûts
capacites, couts = generer_capacites_couts_aleatoirement(10)



csv_files = [
    "./temps_execution/temps_execution_FF.csv",
    "./temps_execution/temps_execution_PR.csv",
    "./temps_execution/temps_execution_FM.csv",
]

labels = ["Edmonds–Karp (FF)", "Push–Relabel (PR)", "Flot à coût min (FM)"]
for path, lbl in zip(csv_files, labels):
    plot_algorithm(path, lbl)

