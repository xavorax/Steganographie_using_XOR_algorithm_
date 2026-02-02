from PIL import Image
import random as rand
from math import floor
import zlib

rand.seed(32)
image_path = "image.jpg"
with open("Input.txt", "r") as text_file:
    texte = text_file.read()
masque = "Test"

#Création du buffer du texte
random_number = rand.randint(0,4294967295)
key_starting_byte =  format(random_number,'032b')

#Chargement de l'image
image = Image.open(image_path)
largeur, longueur = image.size
pix = image.load()

total_pixels = image.size[0]*image.size[1]
max_caracteres = floor(total_pixels/8)

pos_depart = [rand.randint(0, d - 1) for d in image.size]
pos_depart_1D = pos_depart[1] * largeur + pos_depart[0]
print("Pixel de départ", pos_depart)

def insert_bit_in_pixel(i, j, bit):
    r, g, b = pix[i,j]
    G_value = rand.randint(0,1)
    if G_value: #On change blue

        g = g | 1
        if bit == "1":
            b = b | 1
        else : 
            b = b & ~1
    else : #On change green
        g = g & ~1
        if bit == "1":
            r = r | 1
        else : 
            r = r & ~1
    pix[i,j] = r, g, b
 
def chiffre(message_bytes, masque):
    masque_bytes = masque.encode('utf-8')
    # On fait le XOR octet par octet directement
    return bytes([message_bytes[i] ^ masque_bytes[i % len(masque_bytes)] for i in range(len(message_bytes))])

def encodage_message(key_start, message, start_index, masque):  
    capacite_totale_octets = (image.size[0] * image.size[1] - 64) // 8

    #Compression pour éviter la redondance
    texte = zlib.compress(message.encode('utf-8'))

    taille_requise = len(texte)

    if taille_requise > capacite_totale_octets:
        return 'Texte trop long pour être chiffré dans cette image'
    
    #Chiffrement du message
    message_XOR = chiffre(texte, masque)

    #Message au format binaire
    b = ''.join(format(byte, '08b') for byte in message_XOR)

    taille_binaire = format(len(b), '032b')

    if len(b) > (total_pixels * 1) - 64:
        print("Message trop long !")
        return

    key_text_encode = key_start + taille_binaire + b

    for i in range(len(key_text_encode)):
            current_index = (start_index + i) % total_pixels
            y = current_index // largeur  # La ligne
            x = current_index % largeur   # La colonne
            insert_bit_in_pixel(x,y,key_text_encode[i])
    
    
encodage_message(key_starting_byte, texte, pos_depart_1D, masque)
    
image.save("image_codee.png")
print("Image sauvegardée avec succès !")