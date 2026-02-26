import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import Slider
from datetime import timedelta

def generer_gantt(
    liste_operations,
    nombre_chromatique,
    affichage_semaines_reelles=True,
    navigation_semaines=True,
    taille_fenetre_semaines=1,
    affichage_toutes_semaines=True,
    navigation_souris=True,
):
    """
    Génère un diagramme de Gantt avec une navigation stricte "Semaine par Semaine".
    Le graphique s'aligne automatiquement sur les vrais Lundis.
    """
    if not liste_operations:
        print("⚠️ Aucune opération à afficher pour cette période.")
        return

    fig, ax = plt.subplots(figsize=(16, 8))
    plt.subplots_adjust(bottom=0.20) 

    # 1. Bornes temporelles globales
    date_min_global = min(op.date_debut for op in liste_operations)
    date_max_global = max(op.date_fin for op in liste_operations)

    # --- NOUVEAUTÉ : Alignement strict sur le Lundi ---
    # On recule jusqu'au Lundi de la première semaine (0 = Lundi)
    date_min_alignee = date_min_global - timedelta(days=date_min_global.weekday())
    date_min_alignee = date_min_alignee.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Convertir en format numérique (jours)
    min_num = mdates.date2num(date_min_alignee)
    max_num_reel = mdates.date2num(date_max_global)
    
    # Calculer le nombre total de semaines nécessaires pour tout couvrir
    duree_totale_jours = max_num_reel - min_num
    nb_semaines_totales = max(1, math.ceil(duree_totale_jours / 7))

    # 2. Identifier les machines uniques
    machines_uniques = sorted(list(set(op.machine for op in liste_operations)))
    machine_to_y = {machine: i for i, machine in enumerate(machines_uniques)}

    # Palette de couleurs
    cmap = plt.get_cmap('tab10' if nombre_chromatique <= 10 else 'tab20')
    couleurs_base = cmap.colors

    # 3. Dessiner les barres
    for op in liste_operations:
        if op.machine not in machine_to_y: continue
        
        start_num = mdates.date2num(op.date_debut)
        end_num = mdates.date2num(op.date_fin)
        duration = end_num - start_num 
        
        y_pos = machine_to_y[op.machine]
        color_id = op.couleur_assignee if op.couleur_assignee and op.couleur_assignee > 0 else 1
        color_index = (color_id - 1) % len(couleurs_base)
        color = couleurs_base[color_index]

        ax.barh(y_pos, duration, left=start_num, height=0.6, 
                color=color, edgecolor='black', alpha=0.8)

        # Ajouter le texte du produit
        if duration > 0.1: 
            center_x = start_num + duration / 2
            ax.text(center_x, y_pos, op.code_produit, ha='center', va='center', 
                    color='white', fontsize=8, fontweight='bold', clip_on=True)

    # 4. Configuration Axes
    ax.set_yticks(range(len(machines_uniques)))
    ax.set_yticklabels(machines_uniques)
    ax.set_ylabel("Machine", fontweight='bold')

    # 5. Configuration Axe X (Temps)
    ax.xaxis_date() 
    
    # Marqueurs principaux : Chaque Lundi
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MONDAY))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b\nSem %W'))
    
    # Marqueurs secondaires : Chaque Jour
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%A %d')) 
    ax.tick_params(axis='x', which='minor', labelsize=8, labelcolor='dimgray', rotation=45)

    ax.grid(True, axis='x', which='major', color='black', linestyle='-', linewidth=1.2, alpha=0.5)
    ax.grid(True, axis='x', which='minor', color='gray', linestyle=':', alpha=0.4)
    ax.grid(True, axis='y', linestyle='--', alpha=0.2)

    # 6. Affichage initial : EXACTEMENT 1 SEMAINE (7 jours à partir du Lundi)
    ax.set_xlim(min_num, min_num + 7)
    
    ax.set_title(f"Planning d'Atelier - {len(liste_operations)} Opérations ({nombre_chromatique} couleurs)", fontsize=14, pad=20)

    # 7. LE SLIDER "CRANTÉ" SEMAINE PAR SEMAINE
    if navigation_semaines:
        ax_slider = fig.add_axes([0.15, 0.05, 0.75, 0.03])
        
        # Le slider s'arrête à la dernière semaine
        slider_max = min_num + (nb_semaines_totales - 1) * 7
            
        slider_nav = Slider(
            ax=ax_slider,
            label='Semaine du',
            valmin=min_num,
            valmax=slider_max,
            valinit=min_num,
            valstep=7, # C'EST LA MAGIE ICI : Le slider saute de 7 jours en 7 jours !
        )

        # Formater l'affichage de la date sur le slider
        def format_date_slider(val):
            return mdates.num2date(val).strftime('%d %b %Y')
            
        slider_nav.valtext.set_text(format_date_slider(slider_nav.val))

        def update_slider(val):
            # On force la vue à afficher exactement les 7 jours de la semaine sélectionnée
            ax.set_xlim(val, val + 7)
            slider_nav.valtext.set_text(format_date_slider(val))
            fig.canvas.draw_idle()

        slider_nav.on_changed(update_slider)

    # 8. Désactivation du zoom molette pour ne pas casser l'affichage strict d'une semaine
    # (Tu peux réactiver on_scroll si tu le souhaites, mais le drag&drop reste utile)
    if navigation_souris:
        state = {"press_x": None, "xlim": None}

        def on_press(event):
            if event.inaxes != ax or event.button != 1: return
            state["press_x"] = event.xdata
            state["xlim"] = ax.get_xlim()

        def on_release(event):
            state["press_x"] = None

        def on_motion(event):
            if state["press_x"] is None or event.inaxes != ax or event.xdata is None: return
            dx = event.xdata - state["press_x"]
            cur_xmin, cur_xmax = state["xlim"]
            ax.set_xlim(cur_xmin - dx, cur_xmax - dx)
            fig.canvas.draw_idle()

        fig.canvas.mpl_connect("button_press_event", on_press)
        fig.canvas.mpl_connect("button_release_event", on_release)
        fig.canvas.mpl_connect("motion_notify_event", on_motion)

    plt.show()