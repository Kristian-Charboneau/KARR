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

  shutdown_pin =  ' the pin connected to the On/Off switch board
  light_pin =  ' denotes the pin used for the led
  'motor control pins are less than light_pin
VAR

  'Globally accessible variables
  long  setMototrStack[100]
  byte  m1, m2, m3, m4, m5, m6, m7, m8, m9

  
OBJ
  serial        : "Parallax Serial Terminal"
  servo         : "PWM_32_v7"
  bs2           : "BS2_Functions"

PUB Main | pin, value, failed
{{
  Init drivers, get data from host and set outputs.
  variables:
    pin: I/O pin to set. The max I/O pin value is 27, this leaves 28-255 for other "modes" or control codes that can be used
    value: what value the I/O pin should be set to
    failed: Incremented if a packet wasn't received correctly
}}
  serial.start(256000)
  servo.start
  bs2.start

  repeat
	if serial.rx = '<'
		pin := serial.rx
		value := serial.rx
		if serial.rx = '>'
			serial.tx(32)  ' send a space character if the packet was recieved correclty
			if pin < light_pin 
				servo.Servo(pin, convert(value))
			if pin == light_pin
				servo.Duty(pin, value, 5000)
			if pin == shutdown_pin
				shutdown
		else
			serial.tx('!')  ' send a "!" if the packet wasn't received correctly
		

PUB convert(value, min, max)
{{
  converts a range (such as 0 to 200) to servo pwm values
 
  parameters:    value = the input value to convert
                 min = minimum value in range
                 max = maximum value in range
                 
  return:        new value

  expected outcome of example usage call: Does nothing yet.
}}

  'Your code here
PUB shutdown
	bs2.PAUSE(5000)
	bs2.HIGH(shutdown_pin)

