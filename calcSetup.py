import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.uix.button import Button
from kivy.core.window import Window

from calculatorLogic import *

kivy.require('1.9.0')
Window.size = (500,500)
 
class CalcGridLayout(GridLayout):
    def __init__(self, *args, **kwargs):
        super(CalcGridLayout, self).__init__(*args, **kwargs)
    
    def button_press(self, button):
        prior = self.input.text
		
        if "Error" in prior or 'None' in prior:
            prior = ''

        if prior == "0":
            self.input.text = ''
            self.input.text = f'{button}'
        else: 
            self.input.text = f'{prior}{button}'

    def calculate(self, calculation):
        try:
            x = Calculator()
            x.expr = str(calculation)
            res = x.calculate()
            self.input.text = str(res)
        except Exception:
            self.input.text = 'Error'

    def clear(self, expression):
        if not expression or all(c == ' ' for c in expression):
            self.input.text = ''
            return

        self.input.text = self.input.text[:-1]

        if expression[-1] == ' ':
            self.input.text = self.input.text.rstrip()
        else:
            self.input.text = self.input.text.rstrip()
  
class CalculatorApp(App):
    def build(self):
        return CalcGridLayout()

if __name__ == '__main__':
    calcApp = CalculatorApp()
    calcApp.run()