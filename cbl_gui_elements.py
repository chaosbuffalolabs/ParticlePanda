import kivy
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.app import App

class RectangleWidget(Widget):
    def __init__(self,color=None,**kwargs):
        super(RectangleWidget,self).__init__(**kwargs)
        self.color = (1,1,1) if color is None else color
        Clock.schedule_once(self.setup_window)

    def setup_window(self,dt):
        with self.canvas:
            Color(*self.color)
            Rectangle(pos=self.pos, size=self.size)

class TagItem(Widget):

    parent = ObjectProperty(None,allownone = True)

    def __init__(self,text,color=None,text_color=None,**kwargs):
        super(TagItem,self).__init__(height=20,size_hint_y=None,**kwargs)
        self.text = text
        self.color = (.6,.6,.6) if color is None else color
        self.text_color = (0,0,0,1) if text_color is None else text_color
        Clock.schedule_once(self.setup_window)

    def setup_window(self,dt):
        if self.text == '[blank]':
            with self.canvas:
                Color(*self.color)
                Line(points= (self.x,self.y,self.x,self.top, self.right, self.top, self.right, self.y, self.x, self.y), dash_length = 5, dash_offset = 2)

            self.label = Label(text='Add an item...', text_size=(self.width-25,18), size = (self.width-20,20), color=self.color, pos = (self.x+5, self.y), size_hint = (None,None))
            self.remove_icon = None
            self.add_widget(self.label)

        else:
            with self.canvas:
                Color(*self.color)
                Rectangle(pos=self.pos, size=self.size)

            self.label = Label(text=self.text, text_size=(self.width-25,20), size = (self.width-20,20), color=self.text_color, pos = (self.x+5, self.y), size_hint = (None,None))
            self.remove_icon = Image(source='Assets/remove.png',pos = (self.x + self.width - 20, self.y), size = (20,20), size_hint = (None,None))
            self.add_widget(self.label)
            self.add_widget(self.remove_icon)

    def on_touch_down(self,touch):
        if not self.collide_point(*touch.pos):
            return False
        if self.remove_icon is not None and self.remove_icon.collide_point(*touch.pos):
            self.parent.remove(self)
        else:
            self.parent.item_callback(self)


class TagItemContainer(BoxLayout):
    items = ListProperty([])

    def __init__(self,**kwargs):
        super(TagItemContainer,self).__init__(orientation='vertical', spacing = 10, padding = 10, **kwargs)
        # self.items = []
        Clock.schedule_once(self.redraw)
        

    def redraw(self,dt):
        self.clear_widgets()
        for i in self.items:
            self.add_widget(TagItem(i,parent = self))   
        
        # now add an item sayin "Add new item"
        self.add_widget(TagItem('[blank]', parent=self))

        # and finally a spacer widget to force everything to the top
        self.add_widget(Widget())
        

    def on_items(self,instance,value):
        print self.items
        self.redraw(None)

    def add_item(self,item_text):
        self.items.append(item_text)

    def remove(self,instance):
        self.items = [x for x in self.items if x != instance.text]

    def item_callback(self,instance):
        print "Button %s pressed; override item_callback to add functionality." % (instance.text,)

class CBL_DebugPanel(BoxLayout):
    fps = StringProperty("")
    
    def __init__(self,**kwargs):
        super(CBL_DebugPanel,self).__init__(**kwargs)
        Clock.schedule_once(self.setup_window)

    def setup_window(self,dt):
        self.label = Label(text='FPS:')
        self.update(None)
        self.add_widget(self.label)

    def update(self, dt):
        self.label.text = 'FPS: ' + str(int(Clock.get_fps()))
        Clock.schedule_once(self.update,.1)