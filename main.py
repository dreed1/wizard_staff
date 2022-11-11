from machine import Pin, Timer
import machine, neopixel, random, time

#set up buttons
def mode_pressed(pin):
  global current_mode
  global mode_count
  current_mode = (current_mode + 1) % mode_count
  mode_button.irq(trigger=Pin.IRQ_RISING, handler=mode_pressed)

def mode_debounce(pin):
  timer.init(mode=Timer.ONE_SHOT, period=250, callback=mode_pressed)
  mode_button.irq(handler=None)
  
mode_button = Pin(12, Pin.IN)
mode_button.irq(trigger=Pin.IRQ_RISING, handler=mode_pressed)

# set up the neopixel library
n = 25 # the number of LEDS
p = 5 # the pin it's hooked to

current_mode = 0
mode_count = 6
rainbow_position = 0
max_rainbow = 255

np = neopixel.NeoPixel(machine.Pin(p), n)
timer = Timer()

def clear():
  for i in range(n):
    np[i] = (0, 0, 0)
    np.write()

def wheel(pos):
  #Input a value 0 to 255 to get a color value.
  #The colours are a transition r - g - b - back to r.
  if pos < 0 or pos > 255:
    return (0, 0, 0)
  if pos < 85:
    return (255 - pos * 3, pos * 3, 0)
  if pos < 170:
    pos -= 85
    return (0, 255 - pos * 3, pos * 3)
  pos -= 170
  return (pos * 3, 0, 255 - pos * 3)

def lightning():
    color_diff = random.randint(0, 50);
    red = random.randint(0, 40)
    green = random.randint(10, 25)
    blue = random.randint(0, 170)
    for i in range(n):
      np[i] = (red + color_diff, green + color_diff, blue + color_diff)
    np.write()

def fire():
  for i in range(n):
    red = random.randint(170, 254)
    green = random.randint(5, 65)
    blue = random.randint(0, 40) 
    np[i] = (red, green, blue)
  np.write()

def rainbow_cycle():
    global rainbow_position
    rainbow_position = (rainbow_position + 1) % 256
    for i in range(n):
      rc_index = (i * 256 // n) + rainbow_position
      np[i] = wheel(rc_index & 255)
    np.write()
    
def rainbow_pulse():
    global rainbow_position
    rainbow_position = (rainbow_position + 1) % 256
    for i in range(n):
        np[i] = wheel(rainbow_position)
    np.write()

def sparkle():
  for i in range(n):
    if random.randint(0, 100) > 90:
      red = random.randint(200, 254)
      green = random.randint(200, 254)
      blue = random.randint(200, 254) 
      np[i] = (red, green, blue)
    else:
      np[i] = (0,0,0)
  np.write()

def poison():
  red = random.randint(0, 15)
  green = random.randint(200, 254)
  blue = random.randint(0, 15)
  for i in range(n):
    np[i] = (red, green, blue)
  np.write()

while True:
  if current_mode == 0:
    rainbow_pulse()
  elif current_mode == 1:
    fire()
  elif current_mode == 2:
    lightning()
  elif current_mode == 3:
    sparkle()
  elif current_mode == 4:
    poison()
  else:
    clear()
  time.sleep_ms(1)


