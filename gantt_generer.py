import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Slider
from datetime import datetime, timedelta

def generer_gantt(
    liste_operations,
    nombre_chromatique,
    affichage_semaines_reelles=False,
    fenetre_temps=None,
    navigation_semaines=False,
    taille_fenetre_semaines=2,
):
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

    # 1. Bornes temporelles globales (toutes les opérations)
    date_min_global = min(op.date_debut for op in liste_operations)
    date_max_global = max(op.date_fin for op in liste_operations)

    # Fenêtre d'affichage initiale
    if fenetre_temps:
        date_min, date_max = fenetre_temps
    else:
        date_min, date_max = date_min_global, date_max_global
    
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
        
        # Calcul : combien de semaines se sont écoulées depuis le début global ?
        if fenetre_temps and not navigation_semaines:
            visible_start = max(op.date_debut, date_min)
            visible_end = min(op.date_fin, date_max)
            if visible_end <= visible_start:
                continue
            start_offset_semaines = (visible_start - date_min_global).total_seconds() / (3600 * 24 * 7)
            duration_semaines = (visible_end - visible_start).total_seconds() / (3600 * 24 * 7)
        else:
            start_offset_semaines = (op.date_debut - date_min_global).total_seconds() / (3600 * 24 * 7)
            duration_semaines = op.duree.total_seconds() / (3600 * 24 * 7)
        
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
    duree_totale_semaines = (date_max_global - date_min_global).total_seconds() / (3600 * 24 * 7)
    limit_x = max(1, int(math.ceil(duree_totale_semaines)))
    
    # Fenêtre d'affichage initiale (en semaines)
    if fenetre_temps:
        debut_fenetre_sem = (date_min - date_min_global).total_seconds() / (3600 * 24 * 7)
        fin_fenetre_sem = (date_max - date_min_global).total_seconds() / (3600 * 24 * 7)
        ax.set_xlim(debut_fenetre_sem, fin_fenetre_sem)
    else:
        ax.set_xlim(0, limit_x)
    
    # --- ASTUCE : Changer les labels S0, S1 en S48, S49 ---
    ticks = range(limit_x + 1)
    ax.set_xticks(ticks)
    
    if navigation_semaines:
        labels = [f"Semaine {i}" for i in ticks]
    elif affichage_semaines_reelles:
        # On calcule le vrai numéro de semaine à partir de la date globale
        labels = []
        for i in ticks:
            d = date_min_global + timedelta(weeks=i)
            iso_year, iso_week, _ = d.isocalendar()
            labels.append(f"Sem {iso_week}-{iso_year}")
    else:
        labels = [f'+{i} Sem' for i in ticks]
        
    ax.set_xticklabels(labels)
    ax.set_xlabel(f"Semaines (Année {date_min_global.year})")

    ax.set_title(f"Planning - Semaines {labels[0]} à {labels[-1]}")
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)

    # Navigation par semaines via un slider
    if navigation_semaines:
        fenetre = max(1, int(taille_fenetre_semaines))
        max_start = max(0, limit_x - fenetre)
        initial_start = 0
        if fenetre_temps:
            initial_start = int(round((date_min - date_min_global).total_seconds() / (3600 * 24 * 7)))

        slider_ax = fig.add_axes([0.12, 0.03, 0.76, 0.03])
        slider = Slider(
            ax=slider_ax,
            label="Semaine",
            valmin=0,
            valmax=max_start,
            valinit=min(initial_start, max_start),
            valstep=1,
        )

        def update(val):
            start = slider.val
            ax.set_xlim(start, start + fenetre)
            fig.canvas.draw_idle()

        slider.on_changed(update)

    plt.tight_layout()
    plt.show()
