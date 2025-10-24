import keyboard
import time
import string



def start_scan(timeout=None, digits_only=True): # Kein Timeout und nur Nummerische Werte
    buffer = ""
    start_time = time.time()
    printable = set(string.printable) - set("\r\n\t\x0b\x0c") #gibt an welche Zeichen ich Ausschließe

    try:
        while True:
            if timeout is not None and (time.time() - start_time) > timeout: #Überprüft ob ein Timeout Vorhanden ist 
                return None

            event = keyboard.read_event()
            if event.event_type != keyboard.KEY_DOWN: # hier wird auf die Tastatureingabe gelauscht "Key_Down steht dafür, dass das Loslassen Ignoriert wird"
                continue
            key = event.name  #wertet das Ergebnis aus keyboard.read.event aus

            if key == 'enter': # Wenn Enter gedrückt wird entfernt buffer.strip() Leerzeichen am Anfang und Ende
                result = buffer.strip()
                print(f"Scan abgeschlossen: {result}") 
                return result
            
            if key == 'space':
                char = ' '
            elif len(key) == 1: #Hier wird das wird das ganze nochmal ins richtige Format gebracht
                char = key
            else:
                continue

            if digits_only and not char.isdigit():    # Prüft ob es nur Nummerische Werte sind
                continue

            if all(c in printable for c in char): # Hier wird geprüft ob z.b char = '5' in printable ist wenn ja dann buffer + '5'
                buffer += char

    except KeyboardInterrupt: #Ende
        print("\nBeendet durch Benutzer.")
        return None


