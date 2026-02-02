from PIL import Image
import random as rand
from collections import deque
import zlib

rand.seed(32)
image_path = "image_codee.png"
masque = "Test"

#Création du buffer du texte
start_random_number = rand.randint(0,4294967295)
key_starting_byte =  format(start_random_number,'032b')

#Chargement de l'image
image = Image.open(image_path)
pix = image.load()
largeur, hauteur = image.size
total_pixels = largeur * hauteur

def decode_pixel(i,j):
    r, g, b = pix[i,j]
    if g % 2: #On regarde blue
        bit = b % 2
    else : #On regarde green
        bit = r % 2
    return bit

def find_start_position(key_start):
    len_key = len(key_start)

    target_key = [int(b) for b in key_start]

    buffer = deque(maxlen=len_key)
    for idx in range(total_pixels):
        x, y = idx % largeur, idx // largeur
        buffer.append(decode_pixel(x, y))
        
        if list(buffer) == target_key:
            return idx + 1 # On a trouvé !
            
    return "Clé non trouvée."

def find_end_position(idx_start):
    bits_taille = ""
    for i in range(32):
        curr = (idx_start + i) % total_pixels
        bits_taille += str(decode_pixel(curr % largeur, curr // largeur))
    
    longueur_message = int(bits_taille, 2)
    # On renvoie la longueur pour savoir combien de bits lire après les 32 bits de taille
    return longueur_message

def chiffre(message_bytes, masque):
    masque_bytes = masque.encode('utf-8')
    # On fait le XOR octet par octet directement
    return bytes([message_bytes[i] ^ masque_bytes[i % len(masque_bytes)] for i in range(len(message_bytes))])


def visualise_on_image(idx_start, idx_end): 
    for i in range(idx_start-32, idx_end+32):
        current_index = (i) % total_pixels
        y = current_index // largeur
        x = current_index % largeur 
        if i < idx_start :
            pix[x,y] = (255,0,0)

        elif i < idx_start + 32 :
            pix[x,y] = (0,0,255)

        else :
            pix[x,y] = (0,255,0)

def extraire_texte(key_start) :
    idx_start = find_start_position(key_start) 
    longueur_msg = find_end_position(idx_start)
    idx_message_reel = (idx_start + 32) % total_pixels

    bits_utiles = ""
    for i in range(longueur_msg):
        current_index = (idx_message_reel + i) % total_pixels
        bit = decode_pixel(current_index % largeur, current_index // largeur)
        bits_utiles += str(bit)
    
    liste_octets = []

    for i in range(0, len(bits_utiles) - (len(bits_utiles) % 8), 8):
        octet_binaire = bits_utiles[i:i+8]
        liste_octets.append(int(octet_binaire, 2))
    objet_bytes = bytes(liste_octets)

    message_un_XOR = chiffre(objet_bytes,masque)

    try:
        message_decompressé = zlib.decompress(message_un_XOR)
        message_final = message_decompressé.decode('utf-8')
        visualise_on_image(idx_start, (idx_message_reel + longueur_msg) % total_pixels)

    except UnicodeDecodeError:
        message_final = "Erreur de décodage (données corrompues ou mauvaise clé)"

    except zlib.error:
        message_final = "Erreur, masque XOR invalide"

    return message_final


message = extraire_texte(key_starting_byte)

with open("Output.txt", "w") as text_file:
    text_file.write("Texte decodé: %s" % message)

image.save("image_decodee.png")
print("Image decodée sauvegardée avec succès !")    

