import pandas as pd

try:
    # Lire les fichiers Parquet
    entities_df = pd.read_parquet("./graphrag_index/output/entities.parquet")
    relationships_df = pd.read_parquet("./graphrag_index/output/relationships.parquet")
    communuteries_df = pd.read_parquet("./graphrag_index/output/communities.parquet")
    # Afficher les noms des colonnes disponibles
    print("Colonnes disponibles dans entities_df:")
    print(entities_df.columns.tolist())
    
    print("\nColonnes disponibles dans relationships_df:")
    print(relationships_df.columns.tolist())

    # Afficher les premières lignes des DataFrames complets
    print("\nAperçu des entités:")
    print(entities_df[["title","type"]].head(30))

    # print("\nAperçu des relations:")
    # print(relationships_df.head())
    
    # print("\nAperçu des communautés:")
    # print(communuteries_df.head())

except FileNotFoundError:
    print("Erreur: Les fichiers Parquet n'ont pas été trouvés. Vérifiez les chemins d'accès.")
    print("Chemin recherché: ./graphrag_index/output/")

except Exception as e:
    print(f"Une erreur s'est produite: {str(e)}")