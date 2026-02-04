# ParityStego-Python : Encodage RGB Adaptatif

Ce projet implémente une méthode de stéganographie avancée en Python, combinant compression, chiffrement XOR et une logique de sélection de canal dynamique basée sur la parité. Des LLM ont pu être utilisés dans ce projet pour débugger ou expliquer des librairies. Cependant, le code a été écrit entièrement à la main par moi même.

---

## 🚀 Caractéristiques principales

* **Sélecteur G-Channel :** La parité du canal Vert (G) détermine dynamiquement si l'information est stockée dans le canal Rouge (R) ou Bleu (B).
* **Pipeline de Sécurité :**
    * **Compression Zlib :** Réduction de la taille et augmentation de l'entropie des données pour une meilleure discrétion.
    * **Chiffrement XOR :** Masquage des données via une clé symétrique pour empêcher toute extraction sans le masque.
* **Buffer Circulaire :** Le message peut commencer à n'importe quel pixel (même en fin d'image) et "boucler" au début sans perte de données.
* **Détection par Header :** Utilisation d'un marqueur de début de 32 bits et d'un champ de longueur de 32 bits pour une extraction automatisée et précise.

## Image avec mise en valeur de la zone contenant le message crypté
<img width="2058" height="2129" alt="image" src="https://github.com/user-attachments/assets/cc845383-a1aa-4822-8e22-02d9205cb3c6" />

---

## 🛠️ Fonctionnement Technique

### Algorithme d'insertion
Le script utilise la technique du **LSB (Least Significant Bit)**. La modification est invisible à l'œil nu car elle ne varie la valeur d'un canal que de **±1** sur une échelle de 255.



**Logique de sélection :**

$$
\text{Si } G \pmod 2 = 0 \Rightarrow \text{Bit stocké dans } R
$$
$$
\text{Si } G \pmod 2 = 1 \Rightarrow \text{Bit stocké dans } B
$$

### Pipeline de traitement des données



> **Texte Brut** ➔ **Compression (Zlib)** ➔ **Chiffrement (XOR)** ➔ **Flux Binaire** ➔ **Insertion LSB**

---

## 📊 Analyse de Complexité

| Métrique | Complexité | Commentaires |
| :--- | :--- | :--- |
| **Encodage** | $O(M)$ | $M$ est la taille du message original. |
| **Décodage** | $O(N)$ | $N$ est le nombre total de pixels (scan de la clé). |
| **Brute-force** | $N \times 2^{8K}$ | $K$ est la taille du masque XOR en octets. |
| **Format requis** | **.png** | Format sans perte (Lossless) impératif. |

---

## 💻 Installation & Usage

### Prérequis
* Python 3.x
* Bibliothèque Pillow (`pip install Pillow`)

### Utilisation
1.  **Encodage :** Configurez votre message, votre masque et la graine (seed) dans `encodage.py` et lancez le script.
2.  **Décodage :** Utilisez `decodage.py` avec le même **seed** et le même **masque** pour extraire le secret.
3.  **Sortie :** Le texte décodé est généré dans `Output.txt`. Une image de visualisation (`image_decodee.png`) est générée pour mettre en évidence les zones de données (Rouge: Clé, Bleu: Taille, Vert: Message).



---

## 📈 Évolutions futures
* [ ] Implémentation d'un code correcteur d'erreurs (**Reed-Solomon**).
* [ ] Dispersion des bits via une suite pseudo-aléatoire (**Spread Spectrum**).
* [ ] Interface graphique (**GUI**) pour faciliter l'encodage/décodage.
