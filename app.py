import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from four_model import FourIndustriel
from pid_controller import PIDController

# ── Configuration de la page ──────────────────────────────────────
st.set_page_config(
    page_title="PID - Contrôle de Température",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ Régulateur PID — Four Industriel")
st.markdown("Simulation du contrôle de température d'un four industriel avec un régulateur PID discret.")

# ── Sidebar — Paramètres ──────────────────────────────────────────
st.sidebar.header("⚙️ Paramètres PID")

Kp = st.sidebar.slider("Kp — Proportionnel", 0.01, 2.0, 0.5, 0.01)
Ki = st.sidebar.slider("Ki — Intégral",      0.00, 0.1, 0.01, 0.001, format="%.3f")
Kd = st.sidebar.slider("Kd — Dérivé",        0.00, 5.0, 0.1, 0.05)

st.sidebar.markdown("---")
st.sidebar.header("🎯 Consigne")
consigne = st.sidebar.slider("Température cible (°C)", 50, 500, 200, 10)

st.sidebar.markdown("---")
st.sidebar.header("💥 Perturbation")
perturbation_active = st.sidebar.checkbox("Activer une perturbation", value=False)
t_perturbation      = st.sidebar.slider("Moment (secondes)", 100, 400, 200, 10)
amplitude_perturb   = st.sidebar.slider("Amplitude (°C)", -50, 50, -20, 5)

st.sidebar.markdown("---")
duree = st.sidebar.slider("Durée simulation (secondes)", 300, 1000, 600, 50)

# ── Simulation ────────────────────────────────────────────────────
four = FourIndustriel()
pid  = PIDController(Kp=Kp, Ki=Ki, Kd=Kd, Te=four.Te)

temps        = []
temperatures = []
commandes    = []
erreurs      = []
termes_P     = []
termes_I     = []
termes_D     = []

for t in range(duree):
    # Perturbation au moment choisi
    perturb = 0.0
    if perturbation_active and t == t_perturbation:
        perturb = amplitude_perturb

    # Calcul PID
    u, P, I, D = pid.compute(consigne, four.T)

    # Mise à jour du four
    T = four.step(u, perturbation=perturb)

    # Enregistrement
    temps.append(t)
    temperatures.append(T)
    commandes.append(u * 100)   # En %
    erreurs.append(consigne - T)
    termes_P.append(P)
    termes_I.append(I)
    termes_D.append(D)

# ── Métriques ─────────────────────────────────────────────────────
erreur_finale  = abs(consigne - temperatures[-1])
depassement    = max(0, max(temperatures) - consigne)
temps_reponse  = next((t for t, T in zip(temps, temperatures)
                       if abs(T - consigne) < 0.05 * consigne), duree)

col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Température finale", f"{temperatures[-1]:.1f} °C")
col2.metric("🎯 Consigne",            f"{consigne} °C")
col3.metric("📏 Erreur statique",     f"{erreur_finale:.2f} °C")
col4.metric("⚡ Dépassement",         f"{depassement:.2f} °C")

st.markdown("---")

# ── Graphiques ────────────────────────────────────────────────────
fig, axes = plt.subplots(3, 1, figsize=(12, 10))
fig.patch.set_facecolor('#0f1117')
for ax in axes:
    ax.set_facecolor('#1c2128')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')

# Graphique 1 — Température
axes[0].plot(temps, temperatures, color='#4a9edd', linewidth=2, label='Température mesurée')
axes[0].axhline(y=consigne, color='#2ecc71', linewidth=1.5, linestyle='--', label=f'Consigne ({consigne}°C)')
if perturbation_active:
    axes[0].axvline(x=t_perturbation, color='#e74c3c', linewidth=1.5,
                    linestyle=':', label='Perturbation')
axes[0].fill_between(temps, consigne * 0.95, consigne * 1.05,
                     alpha=0.1, color='#2ecc71', label='Bande ±5%')
axes[0].set_ylabel('Température (°C)', color='white')
axes[0].set_title('Réponse du Système — Suivi de Consigne')
axes[0].legend(facecolor='#1c2128', labelcolor='white', fontsize=9)
axes[0].grid(True, alpha=0.2, color='#30363d')

# Graphique 2 — Commande
axes[1].plot(temps, commandes, color='#f79b2e', linewidth=2, label='Commande u(t)')
axes[1].axhline(y=100, color='#e74c3c', linewidth=1, linestyle='--', alpha=0.5, label='Saturation (100%)')
axes[1].axhline(y=0,   color='#e74c3c', linewidth=1, linestyle='--', alpha=0.5)
axes[1].set_ylabel('Commande (%)', color='white')
axes[1].set_title('Signal de Commande — Ouverture du Brûleur')
axes[1].legend(facecolor='#1c2128', labelcolor='white', fontsize=9)
axes[1].grid(True, alpha=0.2, color='#30363d')
axes[1].set_ylim(-5, 110)

# Graphique 3 — Termes PID
axes[2].plot(temps, termes_P, color='#4a9edd', linewidth=1.5, label='Terme P')
axes[2].plot(temps, termes_I, color='#2ecc71', linewidth=1.5, label='Terme I')
axes[2].plot(temps, termes_D, color='#f79b2e', linewidth=1.5, label='Terme D')
axes[2].set_xlabel('Temps (secondes)', color='white')
axes[2].set_ylabel('Amplitude', color='white')
axes[2].set_title('Décomposition des Termes P — I — D')
axes[2].legend(facecolor='#1c2128', labelcolor='white', fontsize=9)
axes[2].grid(True, alpha=0.2, color='#30363d')

plt.tight_layout()
st.pyplot(fig)

# ── Explication ───────────────────────────────────────────────────
with st.expander("📚 Comprendre les paramètres PID"):
    st.markdown("""
    | Paramètre | Rôle | Effet si trop élevé |
    |---|---|---|
    | **Kp** | Réagit à l'erreur actuelle | Oscillations, dépassement |
    | **Ki** | Élimine l'erreur statique | Oscillations lentes, windup |
    | **Kd** | Anticipe l'évolution | Sensible au bruit |

    **Réglage conseillé pour ce four :**
    - Commencer avec Ki=0, Kd=0 et augmenter Kp jusqu'à avoir une réponse rapide
    - Ajouter Ki progressivement pour éliminer l'erreur statique
    - Ajouter Kd si le dépassement est trop important
    """)