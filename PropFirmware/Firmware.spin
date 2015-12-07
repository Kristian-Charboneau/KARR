{{
Object file:    Firmware.spin
Version:        0.1
Date:           11/15/2015
Author:         Kristian Charboneau
Company:
Email:          

Description:
This is the firmware for the Propeller Chip in KARR
The current functionality is basically a serial servo driver.
The chip drives 6 HB-25 motor controllers and two mosfets for controlling the main LEDs

=============================================
        Connection Diagram
=============================================

N/A

Components:
N/A

=============================================
setMotors()  # could be run in its own cog
getData()

cog0 = get serial data from pc
cog1 = serial driver
cog2 = pwm driver
cog3
cog4
cog5
cog6
cog7

}}
CON

  'Set up the clock mode
  _clkmode = xtal1 + pll16x
  _xinfreq = 5_000_000
  '5 MHz clock * 16x PLL = 80 MHz system clock speed

  base_pin = 0  'the pin for the first motor
  shutdown_pin = 22 ' the pin connected to the On/Off switch board. Not necessary with current design.
  light_pin =  8' denotes the pin used for the led
  'motor control pins are less than light_pin
  return_char = 35  ' #
  
  do_POST = 1  ' 1 = do POST routine, 0 = skip POST
VAR

  'Globally accessible variables
  long  setMototrStack[100]
  byte  m1, m2, m3, m4, m5, m6, m7, m8, m9

  
OBJ
  serial        : "Parallax Serial Terminal"
  servo         : "Servo32v7"
  bs2           : "BS2_Functions"

PUB Main | pin, value, failed
{{
  Init drivers, get data from host and set outputs.
  variables:
    pin: I/O pin to set. The max I/O pin value is 27, this leaves 28-255 for other "modes" or control codes that can be used
    value: what value the I/O pin should be set to
    failed: Incremented if a packet wasn't received correctly
}}
  serial.start(115_200)
  servo.start
  bs2.start(20,21)
  POST
  'serial.Str(String("Hello World"))
  repeat
	if serial.CharIn == 60 '<'
		pin := serial.CharIn
		value := serial.CharIn
		if serial.CharIn == 62 '>'
			serial.char(return_char)  ' send a character if the packet was recieved correclty
			if pin < light_pin 
				servo.set(pin, (convert(value)))
                                serial.Char(return_char)
			'if pin == light_pin
			'	servo.Duty(pin, value, 5000)
                          '                 serial.Char(return_char)
                else
	          serial.char(33)  ' send a "!" if the packet wasn't received correctly
	else
	   serial.char(33)  ' send a "!" if the packet wasn't received correctly
		

PUB convert(value) | oldMin, oldMax, newMin, newMax, oldRange, newRange, newValue
{{
  converts a range (such as 0 to 200) to servo pwm values
 
  parameters:    value = the input value to convert
                 
  return:        new value
}}

  oldMin := 0
  oldMax := 200
  newMin := 1000
  newMax := 2000
  
  oldRange := oldMax - oldMin
  newRange := newMax - newMin
  newValue := (((value - oldMin) * newRange) / oldRange) + newMin
  
  return newValue
PUB shutdown
	bs2.PAUSE(5000)
	bs2.HIGH(shutdown_pin)

PUB POST | i
    if do_POST == 1
        i := base_pin
        REPEAT 6  'cycle thru each motor and set it to reverse
            servo.set(i, 1000)
            i:= i+1
            
        bs2.PAUSE(500) 'wait 1 second
                        
        i := base_pin                
        REPEAT 6  'cycle thru each motor and set it to off
            servo.set(i, 1500)
            i:= i+1
            
         bs2.PAUSE(500) 'wait 1 second
         i := base_pin                
         REPEAT 6  'cycle thru each motor and set it to forward
            servo.set(i, 2000)
            i:= i+1
            
         bs2.PAUSE(500) 'wait 1 second
                         
        i := base_pin                '
        REPEAT 6  'cycle thru each motor and set it to off
            servo.set(i, 1500)
            i:= i+1

            
    RETURN             
