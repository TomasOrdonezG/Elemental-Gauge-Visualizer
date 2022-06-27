#import and initialize
import pygame, os, math, random, sys
pygame.init()
cnvW = 800
cnvH = 600

#global vars
A1 = True
B2 = False
C4 = False
auraList = []
reactionTextList = []

#create screen/canvas
canvas = pygame.display.set_mode((cnvW, cnvH))
pygame.display.set_caption("Title")

#elements colours
elementC = [(163, 243, 202), (250, 182, 50), (175, 142, 193), (165, 200, 59), (76, 194, 241), (239, 121, 56), (159, 214, 227)]

# Assign FPS a value
FPS = 60
FramePerSec = pygame.time.Clock()

#Elements images (0 anemo 1 geo 2 electro 3 dendro 4 hydro 5 pyro 6 cryo)
elementW, elementH = 65, 65
elimgs = []
for elIMG in os.listdir('elements'):
    elimgs.append(pygame.image.load('elements/' + str(elIMG)))

#reaction text
class reactionText:
    def __init__(self, text):
        self.text = text
        self.colour = self.setColour()

    def setColour(self):
        if self.text == 'Fwd. Vaporize' or self.text == 'Rev. Vaporize':
            return (254, 203, 99)

        elif self.text == 'Overload':
            return (251, 136, 155)

        elif self.text == 'Superconduct':
            return (196, 187, 245)

        elif self.text == 'Fwd. Melt' or self.text == 'Rev. Melt':
            return (255, 202, 105)

        elif self.text == 'Crystalize':
            return (215, 184, 130)

        elif self.text == 'Swirl':
            return (163, 243, 202)

        elif self.text == 'E-Charged':
            return (212, 162, 255)

        elif self.text == 'Burning':
            return (233, 152, 8)

        elif self.text == 'Overgrown':
            return (76, 194, 241)

        elif self.text == 'Intensified':
            return (175, 142, 193)

        else:
            return (255, 255, 255)

#Active aura
class Aura:
    IMGside = 300
    tax = 0.8

    def __init__(self, aura, U, decayU, elementNum, auraNumber):
        if elementNum == 0 or elementNum == 1:
            self.aura = False
        else:
            self.aura = aura
        self.U = U * Aura.tax
        self.decayU = decayU
        self.elementNum = elementNum
        self.auraNumber = auraNumber

    def display(self):
        if self.aura:
            if self.auraNumber == 1:
                img = pygame.transform.scale(elimgs[self.elementNum], (Aura.IMGside, Aura.IMGside))

                if len(auraList) == 2: #if there is only one aura active display in the middle
                    canvas.blit(img, ((cnvW / 2) - (Aura.IMGside / 2) - 100, (cnvH / 2.8) - (Aura.IMGside / 2) - 30))
                elif len(auraList) == 3: #if there are 2 auras active display on the left
                    canvas.blit(img, ((cnvW / 2) - Aura.IMGside - 100, (cnvH / 2.8) - (Aura.IMGside / 2) - 30))

            elif self.auraNumber == 2: #display secondary aura on the right
                img = pygame.transform.scale(elimgs[self.elementNum], (Aura.IMGside, Aura.IMGside))
                canvas.blit(img, (cnvW / 2 - 100, (cnvH / 2.8) - (Aura.IMGside / 2) - 30))

    def decay(self):
        if self.aura:
            if self.decayU == 'A':
                self.U -= 1 / (11.875 * FPS)
            if self.decayU == 'B':
                self.U -= 1 / (7.5 * FPS)
            if self.decayU == 'C':
                self.U -= 1 / (5.3125 * FPS)
            if self.decayU == 'AB':
                self.U -= (1 / (11.875 * FPS)) + (1 / (7.5 * FPS))
            if self.decayU == 'BB':
                self.U -= (1 / (7.5 * FPS)) + (1 / (7.5 * FPS))
            if self.decayU == 'CB':
                self.U -= (1 / (5.3125 * FPS)) + (1 / (7.5 * FPS))
        
        #remove aura when decay is complete
        if self.U <= 0:
            self.U = 0
            self.aura = False 

    def auraDisplay(self):
        if self.aura:
            #rect   
            pygame.draw.rect(canvas, (elementC[self.elementNum]), pygame.Rect(0, cnvH - (100 * self.auraNumber), self.U * (cnvW / 4), 30))

            #units
            font = pygame.font.SysFont(None, 50)
            img = font.render(str(math.ceil(self.U * 100) / 100) + self.decayU, True, (255, 255, 255))
            canvas.blit(img, (10, cnvH - (100 * self.auraNumber) - 40))

    def dendroDecay(self):
        global burning
        if self.elementNum == 3 and burning:
            if self.decayU == 'A':
                self.decayU = 'AB'
            if self.decayU == 'B':
                self.decayU = 'BB'
            if self.decayU == 'C':
                self.decayU = 'CB'

def reaction(mouseX, mouseY):
    w, h = elementW, elementH
    y = cnvH - elementH
    if mouseY > y and mouseY < y + h:
        for i in range(2):
            slot = -(i + 1)
            
            #anemo
            x = elementW * 0
            if mouseX > x and mouseX < x + w:
                anemoTrigger(slot)

            #geo
            x = elementW * 1
            if mouseX > x and mouseX < x + w:
                geoTrigger(slot)

            #cryo
            x = elementW * 6
            if mouseX > x and mouseX < x + w:
                cryoTrigger(slot)
        #dendro
        x = elementW * 3
        if mouseX > x and mouseX < x + w:
            dendroTrigger()

        #pyro
        x = elementW * 5
        if mouseX > x and mouseX < x + w:
            pyroTrigger()

        #electro
        x = elementW * 2
        if mouseX > x and mouseX < x + w:
            electroTrigger()

        #Hydro
        x = elementW * 4
        if mouseX > x and mouseX < x + w:
            hydroTrigger()

#All reactions
#reaction modifiers
reverseAmpModifier = 0.5
forwardAmpModifier = 2
superconductModifier = 1
overloadModifier = 1
swirlModifier = 0.5
crystalizeModifier = 0.5
electroChargedModifier = -0.4

def anemoTrigger(slot):
    #Swirl
    if auraList[slot].elementNum == 2 or auraList[slot].elementNum == 4 or auraList[slot].elementNum == 5 or auraList[slot].elementNum == 6:
        rxnMod(swirlModifier, slot)
        reactionTextList.insert(0, reactionText('Swirl'))

def geoTrigger(slot):
    #Crystalize
    if auraList[slot].elementNum == 2 or auraList[slot].elementNum == 4 or auraList[slot].elementNum == 5 or auraList[slot].elementNum == 6:
        rxnMod(crystalizeModifier, slot)
        reactionTextList.insert(0, reactionText('Crystalize'))

def electroTrigger():
    global EC, frameEC
    for i in range(2):
        slot = -(i + 1)
        #Overload
        if auraList[slot].elementNum == 5:
            rxnMod(overloadModifier, slot)
            reactionTextList.insert(0, reactionText('Overload'))

        #Superconduct
        if auraList[slot].elementNum == 6:
            rxnMod(superconductModifier, slot)
            reactionTextList.insert(0, reactionText('Superconduct'))

        #Intensified
        if auraList[slot].elementNum == 3:
            reactionTextList.insert(0, reactionText('Intensified'))

    #Electro-charged
    if auraList[-1].elementNum == 4:
        doubleAura(auraList[-1], 2)
        reactionTextList.insert(0, reactionText('E-Charged'))
        auraList[-1].U -= 0.4
        auraList[-2].U -= 0.4
        frameEC = 0
        EC = True

        #Electro-charged
    elif auraList[-2].elementNum == 4:
        doubleAura(auraList[-2], 2)
        reactionTextList.insert(0, reactionText('E-Charged'))
        auraList[-1].U -= 0.4
        auraList[-2].U -= 0.4
        frameEC = 0
        EC = True

def dendroTrigger():
    global burning, frameBurning
    #Burning
    if auraList[-1].elementNum == 5:
        doubleAura(auraList[-1], 3)
        reactionTextList.insert(0, reactionText('Burning'))
        frameBurning = 0
        burning = True
    #Burning
    elif auraList[-2].elementNum == 5:
        doubleAura(auraList[-2], 3)
        reactionTextList.insert(0, reactionText('Burning'))
        frameBurning = 0
        burning = True

    for i in range(2):
        slot = -(i + 1)

        #Overgrown
        if auraList[slot].elementNum == 4:
            reactionTextList.insert(0, reactionText('Overgrown'))

        #Intensified
        if auraList[slot].elementNum == 2:
            reactionTextList.insert(0, reactionText('Intensified'))

def hydroTrigger():
    global EC, frameEC
    for i in range(2):
        slot = -(i + 1)
        #forward vaporize
        if auraList[slot].elementNum == 5:
            rxnMod(forwardAmpModifier, slot)
            reactionTextList.insert(0, reactionText('Fwd. Vaporize'))

        #Overgrown
        if auraList[slot].elementNum == 3:
            reactionTextList.insert(0, reactionText('Overgrown'))

    #Electro-charged
    if auraList[-1].elementNum == 2:
        doubleAura(auraList[-1], 4)
        reactionTextList.insert(0, reactionText('E-Charged'))
        auraList[-1].U -= 0.4
        auraList[-2].U -= 0.4
        frameEC = 0
        EC = True

        #Electro-charged
    elif auraList[-2].elementNum == 2:
        doubleAura(auraList[-2], 4)
        reactionTextList.insert(0, reactionText('E-Charged'))
        auraList[-1].U -= 0.4
        auraList[-2].U -= 0.4
        frameEC = 0
        EC = True

def pyroTrigger():
    for i in range(2):
        slot = -(i + 1)
        #forward melt
        if auraList[slot].elementNum == 6:
            rxnMod(forwardAmpModifier, slot)
            reactionTextList.insert(0, reactionText('Fwd. Melt'))

        #reverse vaporize
        if auraList[slot].elementNum == 4:
            rxnMod(reverseAmpModifier, slot)
            reactionTextList.insert(0, reactionText('Rev. Vaporize'))

        #Overload
        if auraList[slot].elementNum == 2:
            rxnMod(overloadModifier, slot)
            reactionTextList.insert(0, reactionText('Overload'))

    global burning, frameBurning
    #Burning
    if auraList[-1].elementNum == 3:
        doubleAura(auraList[-1], 5)
        reactionTextList.insert(0, reactionText('Burning'))
        frameBurning = 0
        burning = True
    #Burning
    elif auraList[-2].elementNum == 3:
        doubleAura(auraList[-2], 5)
        reactionTextList.insert(0, reactionText('Burning'))
        frameBurning = 0
        burning = True


    #Burning
    if auraList[slot].elementNum == 3:
        pass

def cryoTrigger(slot):
    #Superconduct
    if auraList[slot].elementNum == 2:
        rxnMod(superconductModifier, slot)
        reactionTextList.insert(0, reactionText('Superconduct'))

    #Reverse melt
    if auraList[slot].elementNum == 5:
        rxnMod(reverseAmpModifier, slot)
        reactionTextList.insert(0, reactionText('Rev. Melt'))

def rxnMod(mod, auraSlot):
    if A1:
        auraList[auraSlot].U -= 1 * mod
    elif B2:
        auraList[auraSlot].U -= 2 * mod
    elif C4:
        auraList[auraSlot].U -= 4 * mod

def getDecayRate():
    if A1:
        U = 1
        d = 'A'
    elif B2:
        U = 2
        d = 'B'
    elif C4:
        U = 4
        d = 'C'

    return U, d

#sets up double auras for the electro-charged and burning reactions
def doubleAura(aura1, aura2):
    if aura1.elementNum == 4 and aura2 == 2: #electro on hydro
        U, d = getDecayRate()
        if aura1.auraNumber == 1:
            auraList.append(Aura(True, U, d, aura2, 2))
        elif aura1.auraNumber == 2:
            auraList.append(Aura(True, U, d, aura2, 1))

    elif aura1.elementNum == 2 and aura2 == 4: #hydro on electro
        U, d = getDecayRate()
        if aura1.auraNumber == 1:
            auraList.append(Aura(True, U, d, aura2, 2))
        elif aura1.auraNumber == 2:
            auraList.append(Aura(True, U, d, aura2, 1))

    elif aura1.elementNum == 5 and aura2 == 3: #dendro on pyro
        U, d = getDecayRate()
        if aura1.auraNumber == 1:
            auraList.append(Aura(True, U, d, aura2, 2))
        elif aura1.auraNumber == 2:
            auraList.append(Aura(True, U, d, aura2, 1))

    elif aura1.elementNum == 3 and aura2 == 5: #pyro on dendro
        U, d = getDecayRate()
        if aura1.auraNumber == 1:
            auraList.append(Aura(True, U, d, aura2, 2))
        elif aura1.auraNumber == 2:
            auraList.append(Aura(True, U, d, aura2, 1))

def e_charged(): #electro charged ticks
    global frameEC, EC
    if EC:
        if frameEC == FPS and len(auraList) >= 2:
            frameEC = 0
            auraList[-1].U -= 0.4
            auraList[-2].U -= 0.4
            reactionTextList.insert(0, reactionText('E-Charged'))

        if auraList[-1].U <= 0 or auraList[-2].U <= 0:
            EC = False
            frameEC = FPS + 1

def burningReaction(): #burning ticks
    global frameBurning, burning
    if burning:
        if frameBurning == (FPS / 4) and len(auraList) >= 2:
            frameBurning = 0
            reactionTextList.insert(0, reactionText('Burning'))

            #reapply 2B pyro every tick
            if auraList[-1].U <= 2 * Aura.tax and auraList[-1].elementNum == 5:
                auraList[-1] = Aura(True, 2, 'B', 5, 2)

            if auraList[-2].U <= 2 * Aura.tax and auraList[-2].elementNum == 5:
                auraList[-2] = Aura(True, 2, 'B', 5, 1)

        if auraList[-1].U <= 0 or auraList[-2].U <= 0:
            burning = False
            frameBurning = (FPS / 4) + 1

#(0 anemo, 1 geo, 2 electro, 3 dendro, 4 hydro, 5 pyro, 6 cryo)
#initial
auraList.append(Aura(False, 1, 'A', 7, 3))

def clickUnit():
    global A1, B2, C4
    x = cnvW - 300
    y = cnvH - 50
    w = 45
    h = 40
    if mouseX > x and mouseX < x + w:
        if mouseY > y and mouseY < y + h:
            A1 = True
            B2 = False
            C4 = False
    x = cnvW - 200
    if mouseX > x and mouseX < x + w:
        if mouseY > y and mouseY < y + h:
            A1 = False
            B2 = True
            C4 = False
    x = cnvW - 100
    if mouseX > x and mouseX < x + w:
        if mouseY > y and mouseY < y + h:
            A1 = False
            B2 = False
            C4 = True

def click(mouseX, mouseY):
    global A1, B2, C4
    clickUnit()
    
    #Click aura
    for elementNumber in range(len(elimgs)):
        w, h = 65, 65
        x = w * elementNumber
        y = cnvH - h
        if mouseX > x and mouseX < x + w:
            if mouseY > y and mouseY < y + h:
                #if no aura, then apply an element
                if auraList[-1].aura == False:
                    if A1:
                        auraList.append(Aura(True, 1, 'A', elementNumber, 1))
                    elif B2:
                        auraList.append(Aura(True, 2, 'B', elementNumber, 1))
                    elif C4:
                        auraList.append(Aura(True, 4, 'C', elementNumber, 1))

                elif (auraList[-1].elementNum == elementNumber and auraList[-1].aura == True): #extending an aura with same element on slot 1
                    if A1 and auraList[-1].U < 0.8:
                        auraList[-1] = Aura(True, 1, auraList[-1].decayU, elementNumber, auraList[-1].auraNumber)
                    elif B2 and auraList[-1].U < 2.6:
                        auraList[-1] = Aura(True, 2, auraList[-1].decayU, elementNumber, auraList[-1].auraNumber)
                    elif C4 and auraList[-1].U < 3.2:
                        auraList[-1] = Aura(True, 4, auraList[-1].decayU, elementNumber, auraList[-1].auraNumber)

                elif auraList[-2].elementNum == elementNumber and auraList[-2].aura == True: #extending an aura with same element on slot 2
                    if A1 and auraList[-2].U < 0.8:
                        auraList[-2] = Aura(True, 1, auraList[-2].decayU, elementNumber, auraList[-2].auraNumber)
                    elif B2 and auraList[-2].U < 2.6:
                        auraList[-2] = Aura(True, 2, auraList[-2].decayU, elementNumber, auraList[-2].auraNumber)
                    elif C4 and auraList[-2].U < 3.2:
                        auraList[-2] = Aura(True, 4, auraList[-2].decayU, elementNumber, auraList[-2].auraNumber)
                else:
                    #reactions
                    reaction(mouseX, mouseY)

def draw():
    #element buttons
    for i in range(len(elimgs)):
        canvas.blit(pygame.transform.scale(elimgs[i], (elementW, elementH)), (elementW * i, cnvH - elementH))

    #Update Aura
    for i in range(len(auraList)):
        if auraList[i].aura:
            auraList[i].display()
            auraList[i].decay()
            auraList[i].auraDisplay()

    #Unit value tics
    for i in range(2):
        i += 1
        for x in range(5):
            pygame.draw.rect(canvas, (0, 0, 0), pygame.Rect(x * (cnvW / 4) - 2, cnvH - (100 * i), 2, 30))
            if x == 4:
                pygame.draw.rect(canvas, (0, 0, 0), pygame.Rect(x * (cnvW / 4) - 3, cnvH - (100 * i), 2, 30))
        for x in range(40):
            pygame.draw.rect(canvas, (0, 0, 0), pygame.Rect(x * (cnvW / 40) - 2, cnvH - (100 * i), 1, 20))

    #Units buttons
    font1A = pygame.font.SysFont(None, 50)
    font1A.set_underline(A1)
    font2B = pygame.font.SysFont(None, 50)
    font2B.set_underline(B2)
    font4C = pygame.font.SysFont(None, 50)
    font4C.set_underline(C4)
    img = font1A.render("1A", True, (255, 255, 255))
    canvas.blit(img, (cnvW - 300, cnvH - 50))
    img = font2B.render("2B", True, (255, 255, 255))
    canvas.blit(img, (cnvW - 200, cnvH - 50))
    img = font4C.render("4C", True, (255, 255, 255))
    canvas.blit(img, (cnvW - 100, cnvH - 50))

    reactionLog()

def reactionLog(): #reaction log
    if len(reactionTextList) > 0:
        for i in range(len(reactionTextList)):
            font = pygame.font.SysFont('dejavusansmono', 23)
            font = font.render(reactionTextList[i].text, True, reactionTextList[i].colour)
            canvas.blit(font, (cnvW - 200, (cnvH - 250) - (30 * i) + 15))

#Game loop
running = True
frameEC = 0
frameBurning = 0
EC = False
burning = False
while running:
    frameEC += 1
    frameBurning += 1
    #BG Colour keep at top
    canvas.fill((30, 30, 30))

    draw()


    for aura in auraList:
        aura.dendroDecay()
        aura.dendroDecay()

    e_charged()
    burningReaction()

    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            click(mouseX, mouseY)

    #Remove inactive auras from list
    newAuraList = [auraList[i] for i in range(len(auraList)) if auraList[i].aura or auraList[i].auraNumber == 3]
    auraList = newAuraList

    #Remove old reaction logs
    newReactionTextList = [reactionTextList[i] for i in range(len(reactionTextList)) if i <= 12]
    reactionTextList = newReactionTextList

    #Update display
    pygame.display.update()
    FramePerSec.tick(FPS)