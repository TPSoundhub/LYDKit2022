# MBType-D.py - Gem i main.py på Micro:Bit når den skal køre selvstændigt og kombineres med et program på PC/PI/MAC
#             - Husk at det skal være med lille m i main.py ellers duer det ikke!
#
# Version 1.1 - 03 nov 2021 - Rettet fejl i kommentar
# Version 1.0 - 31 aug 2021 - For at lave et komplet sæt MB koder er denne tilføjet. LYD-KIT Region MidtJylland
#
# Type D:
# Program der løbende checker magnet felt styrken og sender værdi på radio hhv seriel når ændring i værdi er stor nok.
# Er det tilfældet sendes tegn: "M" , efterfulgt af en værdi på USB og Radio.
# Værdier sendes løbende med 50 msec interval, men kun hvis der er een tilstrækkelig stor ændring i aflæst værdi siden sidst,
# styret af konstanten THRESHOLD som man kan ændre efter behov.
# Det betyder så at hvis der kommer een værdi er der sket en tilstrækkelig stor ændring i magnetfeltstyrken.
#
# Bemærk potentiel konflikt med TYPE 3!
# Bruges både Type 3 og Type D i een opstilling skal man teste på typen!! 
# sammen med MB-id og Type identifikation for at gøre det til et unikt event med flere MB i opstilling.
#
# Modtages noget på radio sendes det videre på USB.
# Derved kan man sætte een MB til PC/MAC/PI og have flere andre der sender på radio og få
# input events fra alle overført til PC/MAC/PI
#
from microbit import *
import radio
import math
#
# Konstanter til at identificere MB, som I skal rette til jeres opstilling
#
MB_TYPE = "D"     # identificerer denne MB som een type D. SKAL ikke ændres
MB_ID   = "0"     # nummer på MB når i bruger flere af dem i opstilling for at kunne skelne dem ad
CH      = 60      # Den radio kanal I benytter til jeres opstilling/produkt

   
THRESHOLD = 10000
#
# Variabler til at holde styr på input og hvor stor en ændring. Hvis forskel mellem value og last value er mindre end TRESHOLD
# så sendes der ingen værdi.

value      = 0
last_value = 0

#
# Tænde for radio med fuld sende styrke men på specifik kanal som benyttes i opstillingen
#
radio.config(channel=CH)     # samme kanal i alle MB's i samme opstilling. Brug nummer som gruppe har fået tildelt
radio.on()
#
# For at identificere MB på USB (hvis den er tilsluttet via USB) samt kokalt på MB display
#
print("MicroBit på kanal : "+str(CH)+" med ID: "+MB_ID+" og af Typen: "+MB_TYPE)
display.show("K:"+str(CH)+"I:"+MB_ID+"T:"+MB_TYPE)
sleep(1000)
display.clear()


key = "M"
    
while True:                        # Forever - genererer events på radio og USB 

    value = compass.get_field_strength()

    if (abs(value-last_value) > THRESHOLD):        # sender kun hvis ændring i værdi er stor nok
        
        event = MB_ID+MB_TYPE+key+str(int(value))  # unik event med MB ident,type og key der er aktiveret
        print(event)                               # Send streng på USB   - OK selvom MB ikke er tilsluttet via USB
        radio.send(event)                          # Send streng på radio - OK selvom MB er tilslutet via USB 
        display.show(key)                          # Local feedback på Micro:Bit display. Kan fjernes for at spare strøm.
        last_value=value
    else: display.clear()
    #
    # Hvis der modtages noget på radio sendes det ufilteret/uændret videre på USB.
    #
    r = radio.receive()
    if r :
        print(r)

    sleep(50)

