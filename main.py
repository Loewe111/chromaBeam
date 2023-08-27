import time
import pygame
import sys
from pythonosc import dispatcher
from pythonosc import osc_server
import threading
import asyncio

import effects
import argparse

parser = argparse.ArgumentParser(description="ChromaBeam - Convert any projector into a Show Laser")
parser.add_argument("-m", "--mode", type=int, default=1, help="0 = OSC, 1 = DMX over OSC")
parser.add_argument("--dmx-start-address", type=int, default=1, help="DMX start address")
parser.add_argument("-i", "--osc-ip", type=str, default="127.0.0.1", help="OSC IP")
parser.add_argument("-p", "--osc-port", type=int, default=1337, help="OSC port")
parser.add_argument("--windowed-size", type=int, nargs=2, default=[1280, 720], help="Windowed size")
parser.add_argument("--framerate", type=int, default=60, help="Framerate")
parser.add_argument("-f", "--fullscreen", type=bool, default=False, help="Start in fullscreen mode")
args = parser.parse_args()

FRAMERATE = args.framerate
WINDOWED_SIZE = args.windowed_size
OSC_IP = args.osc_ip
OSC_PORT = args.osc_port
MODE = args.mode # 0 = OSC, 1 = DMX over OSC
DMX_START_ADDRESS = args.dmx_start_address

ADDRESSES = [
  "dimmer",
  "red",
  "green",
  "blue",
  "effect",
  "speed",
  "seed",
  "width"
]

effectObjects = []
currentEffect = 0
effectSettings = {
  "dimmer": 1,
  "speed": 1,
  "color": [255, 255, 255],
  "seed": 0.5,
  "width": 0.5,
  "alpha": 0,
}

def splashScreen():
  screen.fill((0, 0, 0))
  logo = pygame.image.load('images/logo_splash.png')
  # center logo
  logoRect = logo.get_rect()
  logoRect.center = screen.get_rect().center
  screen.blit(logo, logoRect)
  pygame.display.update()

def isAddress(value, address):
  if MODE == 0:
    return "/" + address == value
  elif MODE == 1:
    parts = value.split("/")
    # remove empty strings
    parts = list(filter(None, parts))

    if parts[1] != "dmx":
      print("Invalid OSC address: ", parts)
      return False
    
    return int(parts[2]) == DMX_START_ADDRESS + ADDRESSES.index(address) - 1

def setEffect(value):
  global currentEffect
  if MODE == 0:
    currentEffect = value % len(effectObjects)
  elif MODE == 1:
    currentEffect = int(value * 255) % len(effectObjects)

def oscHandler(address, *args):
  global currentEffect
  if isAddress(address, "dimmer"):
    effectSettings["dimmer"] = args[0]
  elif isAddress(address, "red"):
    effectSettings["color"][0] = int(args[0] * 255)
  elif isAddress(address, "green"):
    effectSettings["color"][1] = int(args[0] * 255)
  elif isAddress(address, "blue"):
    effectSettings["color"][2] = int(args[0] * 255)

  elif isAddress(address, "speed"):
    effectSettings["speed"] = args[0]
  elif isAddress(address, "seed"):
    effectSettings["seed"] = args[0]
  elif isAddress(address, "width"):
    effectSettings["width"] = args[0]
  elif isAddress(address, "effect"):
    setEffect(args[0])
  
  print("[OSC] " + address + " " + str(args))
  updateValues()

def updateValues():
  global currentEffect
  effectObjects[currentEffect].speed = effectSettings["speed"]
  effectObjects[currentEffect].seed = effectSettings["seed"]
  effectObjects[currentEffect].width = effectSettings["width"]
  effectObjects[currentEffect].color = effectSettings["color"]

def toggleFullscreen():
  if screen.get_flags() & pygame.FULLSCREEN:
    pygame.display.set_mode(WINDOWED_SIZE)
  else:
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

def draw():
  # clear screen
  screen.fill((0, 0, 0))

  effectObjects[currentEffect].draw()

  # dimmer
  dark_surface = pygame.Surface(screen.get_size()) 
  dark_surface.fill((0, 0, 0)) 
  dark_surface.set_alpha(int(255 * (1 - effectSettings["dimmer"])))
  screen.blit(dark_surface, (0, 0))

  pygame.display.update()

def mainLoop():
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F11:
          toggleFullscreen()
        if event.key == pygame.K_ESCAPE:
          return
      elif event.type == pygame.USEREVENT:
        draw()

# Initialize pygame

pygame.init()
logo = pygame.image.load('images/logo128.png') 
pygame.display.set_icon(logo)
if args.fullscreen:
  screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
  screen = pygame.display.set_mode(WINDOWED_SIZE)
pygame.display.set_caption("ChromaBeam")

# Load effects

for name, clazz in effects.__dict__.items():
  if callable(clazz) and name.startswith("Effect"):
    effectObjects.append(clazz(screen))

if len(effectObjects) == 0:
  print("No effects found!")
  sys.exit(1)

# Create a dispatcher for OSC messages
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/message", oscHandler)  # Replace "/message" with your desired OSC address
dispatcher.set_default_handler(oscHandler)

server = osc_server.ThreadingOSCUDPServer((OSC_IP, OSC_PORT), dispatcher)

# Create an OSC server in a separate thread
server_thread = threading.Thread(target=lambda: server.serve_forever(), daemon=True)
server_thread.start()

# Start the main loop
pygame.time.set_timer(pygame.USEREVENT, 1000 // FRAMERATE)
mainLoop()
server.shutdown()