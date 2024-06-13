from Processing3 import *

def keyReleased():
    global heldKeys, last_input
    last_input = millis()
    if (key in heldKeys):
        heldKeys.remove(key)
        print("release", key, heldKeys)

def keyPressed():
    global heldKeys, last_input
    last_input = millis()
    if (not key in heldKeys):
        heldKeys.append(key)
        print("pressed", key, heldKeys)

def keyTyped():
    global typedKey
    typedKey = key

def getKeyTyped():
    global typedKey
    k = typedKey
    return k

def keyRenderEnd():
    global typedKey
    typedKey = None

def isKeyTyped(key):
    return getKeyTyped() == key

def isKeyPressed(key):
    global heldKeys, typedKey
    return key in heldKeys
