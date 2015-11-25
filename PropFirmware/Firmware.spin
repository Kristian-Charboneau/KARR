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
}}
CON

  'Set up the clock mode
  _clkmode = xtal1 + pll16x
  _xinfreq = 5_000_000
  '5 MHz clock * 16x PLL = 80 MHz system clock speed

VAR

  'Globally accessible variables
  long  cogStack[100]
  long  routine1_cog, routine2_cog  

  
OBJ
  serial        : "FullDuplexSerial"
  servo         : "Servo32v7"

PUB Main
{{
  First public method in the top .spin file starts execution, runs in cog 0
  
  parameters:    none
  return:        none
  
  example usage: N/A - executes on startup
  
  Starts two cogs running in parallel with separate routines, then
  repeats forever.
}}

  'your code here

  'Start parallel routines
  routine1_cog := cognew(Parallel_Routine_1(6, 365, -1), @cogStack[0]) + 1
  routine2_cog := cognew(Parallel_Routine_2, @cogStack[50]) + 1


  'main loop - repeats forever
  repeat

PUB Parallel_Routine_1(param_var1, param_var2, param_var_etc) | local_var1, local_var2, local_var_etc
{{
  Does nothing yet. Add Spin statements to define the operation of this
  public method.  Meant to run independently in its own cog.
 
  parameters:    param_var1    = first parameter passed into Parallel_Routine_1
                 param_var2    = second parameter passed into Parallel_Routine_1
                 param_var_etc = third parameter passed into Parallel_Routine_1
                 
  return:        none

  example usage: cognew(Parallel_Routine_1(42, 89, 314), @cogStack[0]) + 1

  expected outcome of example usage call: Does nothing yet.
}}

  'Your code here


PUB Parallel_Routine_2 | local_var1, local_var2, local_var_etc
{{
  Does nothing yet. Add Spin statements to define the operation of this
  public method.  Meant to run independently in its own cog.
 
  parameters:    none
  return:        none

  example usage: cognew(Parallel_Routine_2, @cogStack[50]) + 1

  expected outcome of example usage call: Does nothing yet.
}}

  'Your code here

PRI Private_Method_1 : return_result | local_var1, local_var2, local_var_etc
{{
  Does nothing yet. Add Spin statements to define the operation of this
  private method.
 
  parameters:    none
  return:        0 - alias is "return_result"

  example usage: Private_Method_1

  expected outcome of example usage call: Does nothing yet.
}}

  'Your code here
  
PUB Public_Method_1 : return_result | local_var1, local_var2, local_var_etc
{{
  Does nothing yet. Add Spin statements to define the operation of this
  public method.
 
  parameters:    none
  return:        0 - alias is "return_result"

  example usage: Public_Method_1

  expected outcome of example usage call: Does nothing yet.
}}

  'Your code here
