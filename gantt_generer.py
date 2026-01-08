import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

def generer_gantt(liste_operations, nombre_chromatique, affichage_semaines_reelles=False, fenetre_temps=None):
    """
    Génère un diagramme de Gantt.
    
    Args:
        liste_operations (list): Liste des opérations à afficher (déjà filtrée).
        nombre_chromatique (int): Pour le titre.
        affichage_semaines_reelles (bool): Si True, tente d'afficher le vrai numéro de semaine ISO.
    """
    if not liste_operations:
        print("⚠️ Aucune opération à afficher pour cette période.")
        return

    fig, ax = plt.subplots(figsize=(16, 8))

    # 1. Trouver les bornes temporelles de CETTE sélection (ou forcer une fenêtre)
    if fenetre_temps:
        date_min, date_max = fenetre_temps
    else:
        date_min = min(op.date_debut for op in liste_operations)
        date_max = max(op.date_fin for op in liste_operations)
    
    # Numéro de la semaine de départ (pour l'affichage sur l'axe X)
    num_semaine_start = date_min.isocalendar().week

    # 2. Identifier les machines uniques pour l'axe Y
    machines_uniques = sorted(list(set(op.machine for op in liste_operations)))
    machine_to_y = {machine: i for i, machine in enumerate(machines_uniques)}

    # Palette de couleurs (index 0-based) pour éviter le clip des entiers > 1
    couleurs_base = plt.cm.get_cmap('tab10', max(nombre_chromatique, 1)).colors

    # 3. Dessiner les barres
    for op in liste_operations:
        if op.machine not in machine_to_y: continue
        
        # Calcul : combien de semaines se sont écoulées depuis le début de la sélection ?
        visible_start = max(op.date_debut, date_min)
        visible_end = min(op.date_fin, date_max)
        if visible_end <= visible_start:
            continue
        start_offset_semaines = (visible_start - date_min).total_seconds() / (3600 * 24 * 7)
        duration_semaines = (visible_end - visible_start).total_seconds() / (3600 * 24 * 7)
        
        y_pos = machine_to_y[op.machine]
        # Mappe l'ID (1-based) vers l'index 0-based, et sécurise par modulo
        color_id = op.couleur_assignee if op.couleur_assignee and op.couleur_assignee > 0 else 1
        color_index = (color_id - 1) % max(nombre_chromatique, 1)
        color = couleurs_base[color_index]

        ax.barh(y_pos, duration_semaines, left=start_offset_semaines, height=0.6, 
                color=color, edgecolor='black', alpha=0.8)

        # Ajouter le texte du produit
        center_x = start_offset_semaines + duration_semaines / 2
        ax.text(center_x, y_pos, op.code_produit, ha='center', va='center', 
                color='white', fontsize=7, fontweight='bold')

    # 4. Configuration Axes
    ax.set_yticks(range(len(machines_uniques)))
    ax.set_yticklabels(machines_uniques)
    ax.set_ylabel("Machine")

    # Configuration Axe X (Temps)
    duree_totale_semaines = (date_max - date_min).total_seconds() / (3600 * 24 * 7)
    if fenetre_temps:
        limit_x = max(1, int(round(duree_totale_semaines)))
    else:
        limit_x = int(duree_totale_semaines) + 2 # +2 pour avoir de la marge
    
    ax.set_xlim(0, limit_x)
    
    # --- ASTUCE : Changer les labels S0, S1 en S48, S49 ---
    if affichage_semaines_reelles and fenetre_temps:
        ticks = range(limit_x)
    else:
        ticks = range(limit_x + 1)
    ax.set_xticks(ticks)
    
    if affichage_semaines_reelles:
        # On ajoute le numéro de la première semaine aux labels
        labels = [f'Sem {num_semaine_start + i}' for i in ticks]
    else:
        labels = [f'+{i} Sem' for i in ticks]
        
    ax.set_xticklabels(labels)
    ax.set_xlabel(f"Semaines (Année {date_min.year})")

    ax.set_title(f"Planning - Semaines {num_semaine_start} à {num_semaine_start + int(duree_totale_semaines)}")
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
