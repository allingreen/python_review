import tkinter as tk


class Tool:
    def __init__(self, name, cost, quantity=0, per_second=0, limit=0):
        self.name = name
        self.cost = cost
        self.quantity = quantity
        self.per_second = per_second
        self.limit = limit


class Clicker:
    def __init__(self, parent):
        self.parent = parent
        self.current_clicks = 0

        self.gear = {}  # имя приспособления - само приспособление
        self.purchase_buttons = {}  # имя приспособления - кнопка

        self.the_button = tk.Button(parent, text='Button to click!', width=20, height=5, command=self.increment)
        root.bind("<space>", self.increment)

        self.gear['simple click'] = Tool('simple click', 10, quantity=1)
        self.gear['click booster'] = Tool('click booster', 50, limit=5)
        self.gear['auto clicker'] = Tool('auto clicker', 15, per_second=1)

        self.purchase_buttons['simple click'] = tk.Button(parent, text='Simple click: (%d): 1' % self.gear['simple click'].cost,
                                                     command=lambda: self.purchase('simple click'))
        self.purchase_buttons['click booster'] = tk.Button(parent, text='Multiplicative booster: (%d): 1' % self.gear['click booster'].cost,
                                                     command=lambda: self.purchase('click booster'))
        self.purchase_buttons['auto clicker'] = tk.Button(parent, text='Auto clicker: (%d): 0' % self.gear['auto clicker'].cost,
                                                     command=lambda: self.purchase('auto clicker'))

        # placement
        self.current_click_label = tk.Label(parent, text='0')
        self.the_button.grid(row=0, column=0)
        self.current_click_label.grid(row=0, column=1, columnspan=2)

        not_auto_row = 0
        auto_row = 0
        for name in self.gear:
            if self.gear[name].per_second:
                not_auto_row += 1
                row = not_auto_row
                column = 2
            else:
                auto_row += 1
                row = auto_row
                column = 1
            self.purchase_buttons[name].grid(row=row, column=column)
        self.update()

    def increment(self, event="Click"):
        self.current_clicks += self.gear['simple click'].quantity * 2**self.gear['click booster'].quantity
        self.current_click_label.config(text='%d' % self.current_clicks)

    def purchase(self, name):
        if self.current_clicks >= self.gear[name].cost and (self.gear[name].limit == 0 or self.gear[name].quantity < self.gear[name].limit):
            self.gear[name].quantity += 1
            self.current_clicks -= self.gear[name].cost
            self.gear[name].cost *= 1.5
            self.current_click_label.config(text='% d' % self.current_clicks)
            self.purchase_buttons[name].config(
                text=self.purchase_buttons[name]['text'].split(': ')[0] + ': {:.1f}: {}'.format(self.gear[name].cost,
                                                                                          self.gear[name].quantity))

    def update(self):
        for gear in self.gear.values():
            self.current_clicks += gear.per_second * gear.quantity
        self.current_click_label.config(text='% d' % self.current_clicks)
        self.parent.after(1000, self.update)


root = tk.Tk()
clicker = Clicker(root)
root.mainloop()
