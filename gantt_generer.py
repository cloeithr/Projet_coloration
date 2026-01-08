import random as random
import matplotlib.pyplot as plt

# --- CONSTANTE DE FORMAT DE DATE ---
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f' 

# =================================================================
# UTILITAIRES COULEUR (Algorithme Luminance Professeur)
# =================================================================

def lineariser_canal(c_255):
    """Linéarise une valeur de canal (0-255) selon la formule fournie."""
    if c_255 <= 10:
        return c_255 / 3294
    else:
        return ((c_255 / 255 + 0.055) / 1.055) ** 2.4

def calculer_luminescence(r, g, b):
    """Calcule la luminescence relative (0.0 à 1.0)."""
    r_lin = lineariser_canal(r)
    g_lin = lineariser_canal(g)
    b_lin = lineariser_canal(b)
    
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin

def est_couleur_valide(r, g, b):
    """Vérifie si la couleur offre un contraste suffisant (ni trop blanche, ni trop noire)."""
    lum = calculer_luminescence(r, g, b)
    
    # Contraste avec le Blanc (pour la visibilité sur fond blanc)
    contraste_blanc = 1.05 / (lum + 0.05)
    
    # Contraste avec le Noir (pour la lisibilité du texte)
    contraste_noir = (lum + 0.05) / 0.05
    
    # Critères: on veut une couleur visible et qui permette un texte lisible (si possible en noir)
    return contraste_blanc > 1.2 and contraste_noir > 2.5

def generer_palette_intelligente(nombre_couleurs):
    """Génère une palette de couleurs distinctes et contrastées."""
    palette = []
    attempts = 0
    
    while len(palette) < nombre_couleurs and attempts < 10000:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        
        if est_couleur_valide(r, g, b):
            couleur_matplotlib = (r/255, g/255, b/255)
            # Vérification simple pour éviter les doublons aléatoires
            if not any(sum((a - b)**2 for a, b in zip(couleur_matplotlib, existing)) < 0.05 for existing in palette):
                 palette.append(couleur_matplotlib)
        
        attempts += 1
        
    # Si l'algo de contraste n'a pas trouvé assez de couleurs, compléter avec une palette standard
    if len(palette) < nombre_couleurs:
        manquants = nombre_couleurs - len(palette)
        palette_sup = plt.cm.get_cmap('hsv', manquants).colors
        palette.extend(palette_sup[:manquants]) # Utiliser seulement le nombre manquant
        
    return palette

def generer_gantt(liste_operations, nombre_chromatique):
    """Crée et affiche le diagramme de Gantt coloré, avec l'axe X en semaines et limité."""
    
    if not liste_operations:
        print("Aucune opération à visualiser.")
        return

    # --- PARAMÈTRE D'AFFICHAGE MODIFIÉ ---
    LIMIT_SEMAINES = 2 # Limite de visualisation définie par l'utilisateur
    JOURS_PAR_SEMAINE = 7 
    
    # Préparation des données pour le tracé
    machines_uniques = sorted(list(set(op.machine for op in liste_operations)))
    machine_vers_y = {machine: i for i, machine in enumerate(machines_uniques)}
    
    date_min = min(op.date_debut for op in liste_operations)
    date_max = max(op.date_fin for op in liste_operations)
    
    # Utilisation de la palette intelligente
    palette = generer_palette_intelligente(nombre_chromatique)
    
    total_jours = (date_max - date_min).total_seconds() / (24 * 3600)
    total_semaines = total_jours / JOURS_PAR_SEMAINE 

    # Création du graphique
    fig, ax = plt.subplots(figsize=(15, 8))

    for op in liste_operations:
        
        # Calcul des coordonnées en UNITÉS DE SEMAINES
        y_pos = machine_vers_y[op.machine] 
        start_offset_jours = (op.date_debut - date_min).total_seconds() / (24 * 3600)
        start_offset_semaines = start_offset_jours / JOURS_PAR_SEMAINE
        
        duration_jours = (op.date_fin - op.date_debut).total_seconds() / (24 * 3600)
        duration_semaines = duration_jours / JOURS_PAR_SEMAINE
        
        # Si l'opération est entièrement après la limite d'affichage, on l'ignore
        if start_offset_semaines > LIMIT_SEMAINES:
            continue
            
        # Choix de la couleur
        couleur_id = op.couleur_assignee
        idx_couleur = (couleur_id - 1) % len(palette)
        couleur = palette[idx_couleur]
        
        # Dessiner la barre
        ax.barh(
            y_pos, 
            duration_semaines, 
            left=start_offset_semaines, 
            height=0.6,
            color=couleur,
            edgecolor='black',
            linewidth=0.5
        )
        
        # Ajout du label du produit au centre de la barre (seulement si la barre est visible)
        center_x = start_offset_semaines + duration_semaines / 2
        if center_x < LIMIT_SEMAINES:
            ax.text(center_x, y_pos, op.code_produit,
                    ha='center', va='center', color='black', fontsize=8)

    # Mise en forme de l'axe Y
    ax.set_yticks(range(len(machines_uniques)))
    ax.set_yticklabels(machines_uniques)
    ax.set_ylabel("Ressource (Machine)")
    
    # Mise en forme de l'axe X (en Semaines)
    ax.set_xlabel(f"Temps écoulé (en Semaines) depuis {date_min.strftime('%Y-%m-%d')}")
    
    # Définir la limite de l'axe X à la valeur demandée (4 semaines)
    ax.set_xlim(0, LIMIT_SEMAINES) 
    
    # Définir les marques (Ticks) jusqu'à la limite
    semaine_ticks = range(LIMIT_SEMAINES + 1)
    ax.set_xticks(semaine_ticks) 
    ax.set_xticklabels([f'S{i}' for i in semaine_ticks]) 
    
    # Titre et légende
    ax.set_title(f"Diagramme de Gantt Coloré par Produit (Nombre Chromatique : {nombre_chromatique}, Affichage : {LIMIT_SEMAINES} Semaines)")
    
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, fc=palette[(i - 1) % len(palette)], edgecolor='black')
        for i in range(1, nombre_chromatique + 1)
    ]
    legend_labels = [f"Couleur {i}" for i in range(1, nombre_chromatique + 1)]
    ax.legend(legend_elements, legend_labels, title="Couleurs Affectées", loc='upper right')
    
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()