from scraper.scrape import scraper_multi_pages

def main():
    print("=== Scraping des données Expat-Dakar ===")
    choix = {
        "1": "Appartements à louer",
        "2": "Appartements meublés",
        "3": "Terrains à vendre"
    }

    print("Choisissez une catégorie :")
    for k, v in choix.items():
        print(f"{k}. {v}")
    
    selected = input("Numéro de la catégorie : ")
    categorie = choix.get(selected)
    
    if not categorie:
        print("Catégorie invalide.")
        return

    nb_pages = int(input("Nombre de pages à scraper : "))
    df = scraper_multi_pages(nb_pages, categorie)

    nom_fichier = {
        "Appartements à louer": "data/expat_dkr_app_a_louer.csv",
        "Appartements meublés": "data/expat_dkr_app_meubles.csv",
        "Terrains à vendre": "data/expat_dkr_terrain_a_vendre.csv"
    }[categorie]

    df.to_csv(nom_fichier, index=False)
    print(f" Scraping terminé : {len(df)} annonces sauvegardées dans {nom_fichier}")

if __name__ == "__main__":
    main()
