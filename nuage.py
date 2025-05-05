import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file
df = pd.read_csv('relation_max.csv')

# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df['Graph_Size'], df['Relation'], alpha=0.6)

# Add labels and title
plt.title("Relation Ford-Fulker par rapport à Pousser-Réétiqueter ")
plt.xlabel("Taille du graphe (Nombre de sommet)")
plt.ylabel("Relation (FF/PR)")

# Show plot
plt.show()
