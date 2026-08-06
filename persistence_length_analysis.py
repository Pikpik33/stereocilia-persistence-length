import os
import glob
import numpy as np
from scipy.optimize import curve_fit
import csv

# On ne donne plus de chemin, on demande au script de trouver où il est
dossier_actuel = os.getcwd()
print(f"DEBUG: Je scanne le dossier actuel : {dossier_actuel}")

# On cherche les fichiers .txt dans ce dossier précis
fichiers = glob.glob("*.txt")

print(f"DEBUG: Fichiers trouvés par Python : {len(fichiers)}")
for f in fichiers:
    print(f" -> Je vois ce fichier : {f}")

results = []

for fichier in fichiers:
    try:
        # Lecture
        data = np.loadtxt(fichier)
        
        # Vérification des colonnes
        if data.shape[1] >= 2:
            x, y = data[:, 0], data[:, 1]
            
            # Calculs...
            dx, dy = np.diff(x), np.diff(y)
            angles = np.arctan2(dy, dx)
            distances = np.arange(len(angles))
            correlations = [np.mean(np.cos(angles[:len(angles)-s] - angles[s:])) for s in range(len(angles))]
            
            # Ajustement
            def model(s, lp): return np.exp(-s / lp)
            popt, _ = curve_fit(model, distances, correlations, p0=[10], bounds=(0, np.inf))
            
            results.append([fichier, popt[0]])
            print(f"Succès : {fichier}")
        else:
            print(f"Format incorrect : {fichier}")
            
    except Exception as e:
        print(f"Erreur sur {fichier} : {e}")

# Sauvegarde
if results:
    with open("resultats_analyse.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Fichier", "Lp"])
        writer.writerows(results)
    print(f"\nTerminé ! 'resultats_analyse.csv' a été créé dans le dossier.")
else:
    print("\nERREUR : Toujours aucun fichier trouvé. Vérifiez bien l'icône de nuage bleu (OneDrive) !")
