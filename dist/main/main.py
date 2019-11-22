# Filechooser
# https://stackoverflow.com/questions/43452697/browse-an-image-file-and-display-it-in-a-kivy-window
# https://kivy.org/doc/stable/api-kivy.uix.filechooser.html

# Button
# https://stackoverflow.com/questions/19005182/rounding-button-corners-in-kivy
# https://github.com/kivy/kivy/issues/4263

# Color
# https://stackoverflow.com/questions/39976475/python-kivy-language-color-property
# https://www.materialui.co/flatuicolors

# Spinner
# https://github.com/kivy/kivy/wiki/Styling-a-Spinner-and-SpinnerOption-in-KV
# https://kivy.org/doc/stable/api-kivy.uix.spinner.html

# Barra de Progresso
# https://www.geeksforgeeks.org/python-progress-bar-widget-in-kivy/

# Menubar e ScreenManager
# https://alwaysemmyhope.com/es/python/696837-kivy-with-menubar-python-kivy.html

# Códigos EXIF
# https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html

# Métrics
# https://kivy.org/doc/stable/api-kivy.metrics.html

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.config import Config
from kivy.metrics import dp, sp
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import (ListProperty, BooleanProperty, StringProperty, 
ObjectProperty)

import os
from os import listdir
from os.path import isfile, join, basename, isdir
import shutil
from PIL import Image
from pathlib import Path
from pytz import timezone
from datetime import datetime
import sys

#os.environ['KIVY_AUDIO'] = 'ffpyplayer'
#os.environ['KIVY_IMAGE'] = 'img_ffpyplayer'
#os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
#os.environ['KIVY_GRAPHICS'] = 'angle_sdl2'

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '600')
Config.set('kivy', 'exit_on_escape', '1')
Config.write()

Builder.load_string('''

<Botao@Button>:
	background_color: 0,0,0,0
	background_normal: ''
	background_down: ''
	canvas.before:
		Color:
			rgba: app.color_button if self.state == "normal" else app.color_button_pressed
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: [15,]

<Texto@TextInput>:
	use_bubble: True
	font_size: app.tam_font
	align: "center"
	halign: "center"
	background_color: 1,1,1,0
	cursor_color: 0,0,0,1
	multiline: False
	canvas.before:
		Color:
			rgba: 1,1,1,1
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: [15,]
		Color:
			rgba: [0.1, 0.1, 0.1, 1]

<MySpinnerOption@SpinnerOption>:
	background_color: 0,0,0,0
	background_normal: ''
	background_down: ''
	font_size: app.tam_font
	canvas.before:
		Color:
			rgba: app.color_button_pressed if self.state == "normal" else app.color_button
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: [15,]

<Display>:
	BoxLayout:
		orientation: 'vertical'
		BoxLayout:
			size_hint: 1, None
			height: '48dp'
			canvas.before:
				Color:
					rgba: app.color_menubar
				Rectangle:
					size: self.size
					pos: self.pos
			Botao:
				text: 'Início'
				size_hint_x: .175
				font_color: app.color_font1 if app.switch == True else app.color_font2
				font_size: app.tam_font
				on_release:
					sm.current = "inicio"
					sm.transition.direction = "left"
			Botao:
				text: 'Configuração'
				size_hint_x: .35
				font_color: app.color_font1 if app.switch == True else app.color_font2
				font_size: app.tam_font
				on_release:
					sm.current = "configuracao"
					sm.transition.direction = "right"
			Botao:
				text: 'Sobre'
				size_hint_x: .175
				font_color: app.color_font1 if app.switch == True else app.color_font2
				font_size: app.tam_font
				on_release:
					sm.current = "sobre"
					sm.transition.direction = "left"
			Label:
				size_hint_x: .3
		ScreenManager:
			id: sm
			Inicio:
				name: "inicio"
			Configuracao:
				name: "configuracao"
			Sobre:
				name: "sobre"

<Inicio>:
	BoxLayout:
		orientation: 'vertical'
		size_hint: 1, 1
		canvas.before:
			Color:
				rgba: app.color_background2 if app.switch == True else app.color_background1
			Rectangle:
				size: self.size
				pos: self.pos
		padding: dp('0'), dp('50'), dp('0'), dp('0')
		BoxLayout:
			orientation: 'vertical'
			size_hint: 1,.8
			canvas.before:
				Color:
					rgba: app.color_background1 if app.switch == True else app.color_background2
				Rectangle:
					size: self.size
					pos: self.pos
			spacing: dp('10')
			padding: dp('10')
			BoxLayout:
				size_hint_x: 1
				size_hint_y: .1
				spacing: dp('10')
				Label:
					text: ''
					size_hint_x: .001
				Texto:
					id: caminho
					text: ""
					hint_text: "Selecione a pasta das imagens"
				Botao:
					text: '...'
					font_size: app.tam_font
					color: app.color_font1 if app.switch == True else app.color_font2
					size_hint_x: .1
					on_release:
						barra_progresso.value = 0
						root.show_load()
				Label:
					text: ''
					size_hint_x: .001
			Widget:
				size_hint_y: .01
			BoxLayout:
				size_hint_x: 1
				size_hint_y: .1
				spacing: dp('10')
				Label:
					text: ''
					size_hint_x: .001
				Label:
					text: "Modo de Organização"
					color: app.color_font1 if app.switch == True else app.color_font2
					font_size: app.tam_font
					size_hint_x: .6
				Spinner:
					id: spinner
					background_color: 0,0,0,0
					canvas.before:
						Color:
							rgba: (app.color_button if self.state == "normal" else app.color_button_pressed)
						RoundedRectangle:
							pos: self.pos
							size: self.size
							radius: [15,]
					text: 'Ano'
					values: ('Ano', 'Mês', 'Dia', 'Hora')
					color: app.color_font1 if app.switch == True else app.color_font2
					font_size: app.tam_font
					size_hint_x: .5
					option_cls: "MySpinnerOption"
				Label:
					text: ''
					size_hint_x: .001
			BoxLayout:
				size_hint_y: .1
				Label:
					text: "Status: %d %%" % barra_progresso.value
					color: app.color_font1 if app.switch == True else app.color_font2
					size_hint_x: .2
				ProgressBar:
					id: barra_progresso
					value: 0
					min: 1
					max: 100
					pos_hint: {'x':0}
					size_hint_x: .87
				Label:
					text: ''
					size_hint_x: .03
			FloatLayout:
				size_hint_y: .5
				Label:
					text: "Informações"
					markup: True
					color: app.color_font1 if app.switch == True else app.color_font2
					font_size: app.tam_font
					text_size: self.size
					size_hint: .55, .13
					pos_hint: {'center_x':.3, 'center_y':.98}
				Label:
					id: info
					text: ""
					markup: True
					color: app.color_font1 if app.switch == True else app.color_font2
					font_size: app.tam_font
					text_size: self.size
					size_hint: .5, .5
					pos_hint: {'center_x':.279, 'center_y':.55}
				Botao:
					text: 'Desfazer'
					font_size: app.tam_font
					color: app.color_font1 if app.switch == True else app.color_font2
					pos_hint: {'center_x':.8, 'center_y':.7}
					size_hint: .3, .3
					on_release:
						barra_progresso.value = 0
						root.path_directory = caminho.text
						root.voltar_formacao_antiga()
				Botao:
					text: 'Iniciar'
					font_size: app.tam_font
					color: app.color_font1 if app.switch == True else app.color_font2
					pos_hint: {'center_x':.8, 'center_y':.3}
					size_hint: .3, .3
					on_release:
						barra_progresso.value = 0
						root.path_directory = caminho.text
						root.organizer()
		Label:
			text: "© 2019. FULLVE -Todos os Direitos Reservados"
			size_hint: 1, .1
			color: app.color_font2 if app.switch == True else app.color_font1
			align: 'center'
			halign: 'center'
	
<Configuracao>:
	switch: switch
	BoxLayout:
		id: box
		orientation: 'vertical'
		canvas.before:
			Color:
				rgba: app.color_background1 if app.switch == True else app.color_background2
			Rectangle:
				size: self.size
				pos: self.pos
		BoxLayout:
			Label:
				text: 'Modo Noite' if app.switch == True else 'Modo Dia'
				size_hint: 1, .1
				color: app.color_font1 if app.switch == True else app.color_font2
				font_size: app.tam_font
				align: 'center'
				halign: 'center'
			Switch:
				id: switch
				active: True
				size_hint: 1, .1
				color: app.color_font1
				font_size: app.tam_font
				align: 'center'
				halign: 'center'
				on_active:
					app.switch = not app.switch
		Label:
			size_hint: 1, .8
			color: app.color_font1
			font_size: app.tam_font
			align: 'center'
			halign: 'center'
			
<Sobre>:
	BoxLayout:
		orientation: 'vertical'
		canvas.before:
			Color:
				rgba: app.color_background1 if app.switch == True else app.color_background2
			Rectangle:
				size: self.size
				pos: self.pos
		Label:
			text: "FULLVE - Tecnologia Objetiva"
			color: app.color_font1 if app.switch == True else app.color_font2
			font_size: app.tam_font
			size_hint: 1, .2
		Label:
			text: "    Gerente:    Eid Sakai \\n    Designer:    Victor Souza \\n    Desenvolvedor:    Victor Manhani"
			color: app.color_font1 if app.switch == True else app.color_font2
			font_size: app.tam_font
			size_hint: 1, .6
		Label:
			text: "Versão: 1.0.0"
			color: app.color_font1 if app.switch == True else app.color_font2
			font_size: app.tam_font
			size_hint: 1, .3
''')

class Display(BoxLayout):
	pass

class Configuracao(Screen):
	
	def __init__(self, **kwargs):
		super(Configuracao, self).__init__(**kwargs)

class Sobre(Screen):
	def __init__(self, **kwargs):
		super(Sobre, self).__init__(**kwargs)

class Inicio(Screen):
	loadfile = ObjectProperty(None)
	savefile = ObjectProperty(None)
	filechooser = ObjectProperty(None)
	path_directory = StringProperty('')
	qtd_imagens = 0
	extensions = [
		'jpg', 'JPG',
		'jpeg', 'JPEG',
		'png', 'PNG',
		'tif', 'TIF',
		'tiff', 'TIFF',
		'pnt', 'PNT',
		'pntg', 'PNTG',
		'pic', 'PIC', 
		'pict', 'PICT',
		'qti', 'QTI',
		'qtif', 'QTIF', 
		'jpe', 'JPE',
		'tga', 'TGA',
		'rle', 'RLE',
		'pcx', 'PCX', 
		'mac', 'MAC',
		'pct', 'PCT'
		#'mp4', 'MP4', 'mpeg', 'mpg', 'mkv', 'bmp', 'BMP', 'gif', 'GIF',
	]

	def dismiss_popup(self, bt):
		self._popup.dismiss()

	def show_load(self):
		self.filechooser = FileChooserIconView()
		bl1 = BoxLayout(size = self.size, pos = self.pos, orientation = "vertical")
		bl2 = BoxLayout(size_hint_y = None, height = 30)
		self._popup = Popup(title="Selecionar Pasta", content=bl1, size_hint = (0.9, 0.9), background="./img/blue.png")
		
		self.filechooser.path = f'{Path.home()}/Desktop/'
		
		bt1 = Builder.load_string('''
Botao:
	text: "Cancelar"
	size_hint: .5,1
''')
		bt1.bind(on_press = self.dismiss_popup)
		
		bt2 = Builder.load_string('''
Botao:
	text: "Selecionar Esta Pasta"
	size_hint: .5,1
''')
		bt2.bind(on_press = self.carregar)
		
		bl2.add_widget(bt1)
		bl2.add_widget(bt2)
		
		bl1.add_widget(self.filechooser)
		bl1.add_widget(bl2)
		
		self._popup.open()

	def carregar(self, bt):
		self.path_directory = self.filechooser.path
		self.dismiss_popup(self)
		self.ids.caminho.text = self.path_directory
		nome_pasta = os.path.abspath(self.path_directory).split("\\")[-1]
		self.ids.info.text = f"Pasta Selecionada: [color=ff3333]{nome_pasta}[/color]"

	def data_criacao_imagem(self, arquivo):
		imagem = Image.open(arquivo)
		info = imagem._getexif()
		data = datetime.fromtimestamp(os.path.getmtime(arquivo)) #Obté, data de modificação
		if info:
			if 36867 in info:
				data = info[36867]
				data = datetime.strptime(data, '%Y:%m:%d %H:%M:%S')
		return data		

	def caminho_da_pasta(self, arquivo, modo):
		data = self.data_criacao_imagem(arquivo)
		if modo == "Ano":
			return f"{self.path_directory}\\Organizex\\{data.strftime('%Y')}"
		elif modo == "Mês":
			return f"{self.path_directory}\\Organizex\\{data.strftime('%Y')}\\Mês - {data.strftime('%m')}"
		elif modo == "Dia":
			return f"{self.path_directory}\\Organizex\\{data.strftime('%Y')}\\Mês - {data.strftime('%m')}\\Dia - {data.strftime('%d')}"
		elif modo == "Hora":
			return f"{self.path_directory}\\Organizex\\{data.strftime('%Y')}\\Mês - {data.strftime('%m')}\\Dia - {data.strftime('%d')}\\Hora - {data.strftime('%H')}"

	def mover_imagem(self, arquivo_nome, arquivo_caminho, modo):
		nova_pasta = self.caminho_da_pasta(arquivo_caminho, modo)
		if not os.path.exists(nova_pasta):
			os.makedirs(nova_pasta)
		shutil.move(arquivo_caminho, nova_pasta + '\\' + arquivo_nome)

	def obter_imagens(self):
		imagens = {arquivo_nome:self.path_directory + '\\' + arquivo_nome for arquivo_nome in os.listdir(self.path_directory) if any(arquivo_nome.endswith(ext) for ext in self.extensions)}
		self.qtd_imagens = len(imagens.keys())
		return imagens

	def organizador(self, modo):
		imagens = self.obter_imagens()
		for arquivo_nome in imagens.keys():
			self.mover_imagem(arquivo_nome, imagens[arquivo_nome], modo)
			self.ids.barra_progresso.value += 100/self.qtd_imagens
		self.ids.barra_progresso.value = 100

	def voltar_formacao_antiga(self):
		#shutil.move("este-arquivo", "/tmp")
		
		root = self.path_directory
		caminho_atual = self.path_directory
		if '\\' in root: root = root.replace('\\','/')
		if '\\' in caminho_atual: caminho_atual = caminho_atual.replace('\\','/')
		if os.path.isdir(caminho_atual+'/Organizex'):
			self.qtd_imagens = 0
			try:
				walk_gen = os.walk(self.path_directory+'/Organizex')
				for root,dirs,files in walk_gen:
					for ext in self.extensions:
						images = [os.sep.join([root, cur_file]) for cur_file in files if cur_file.endswith('.{0}'.format(ext))]
						if images:
							for i in range(len(images)):
								if '\\' in images[i]:
									images[i] = images[i].replace('\\','/')
								shutil.move(images[i], caminho_atual)
								self.qtd_imagens += 1
								self.ids.barra_progresso.value += 100/self.qtd_imagens
				shutil.rmtree(self.path_directory+'/Organizex')
				if self.qtd_imagens > 0:
					self.ids.info.text = f"[color=ff3333]{self.qtd_imagens} imagens[/color] desorganizadas!"
					self.ids.caminho.text = ''
				else:
					self.ids.info.text = "[color=ff3333]Sem imagens[/color] \nnesta pasta!"
					self.ids.caminho.text = ''
			except OSError as e:
				print ("Erro: %s - %s." % (e.filename, e.strerror))
		else:
			if self.ids.caminho.text == '':
				self.ids.info.text = "Pasta não [color=ff3333]escolhida[/color]!"
			else:
				self.ids.info.text = "Caminho não [color=ff3333]existe[/color]!"
			self.ids.caminho.text = ''
			
	def organizer(self):
		modo = self.ids.spinner.text
		if os.path.exists(self.path_directory):
			if self.path_directory:
				self.organizador(modo)
				self.avaliador()
		else:
			if self.ids.caminho.text == '':
				self.ids.info.text = "Pasta não [color=ff3333]escolhida[/color]!"
			else:
				self.ids.info.text = "Caminho não [color=ff3333]existe[/color]!"
			self.ids.caminho.text = ''

	def avaliador(self):
		if self.qtd_imagens > 0:
			self.ids.info.text = f"[color=ff3333]{self.qtd_imagens} imagens[/color] organizadas por {self.ids.spinner.text}!"
			self.ids.caminho.text = ''
		else:
			self.ids.info.text = "[color=ff3333]Sem imagens[/color] \nnesta pasta!"
			self.ids.caminho.text = ''

class MyApp(App):
	title = "Organizex"
	switch = BooleanProperty(False)

	color_background2 = ListProperty([0.20392156862745098,0.596078431372549,0.8588235294117647,1])
	color_font2 = 0.9254901960784314,0.9411764705882353,0.9450980392156862,1
	color_font1 = 0.9254901960784314,0.9411764705882353,0.9450980392156862,1
	color_background1 = ListProperty([0.20392156862745098,0.28627450980392155,0.3686274509803922,1])
	color_button = 0.08627450980392157,0.6274509803921569,0.5215686274509804,1
	color_button_pressed = 0.10196078431372549,0.7372549019607844,0.611764705882353,1
	color_menubar = 0.10196078431372549,0.7372549019607844,0.611764705882353,1
	tam_font = sp('30')

	def build(self):
		self.icon = './img/logo.png'
		return Display()

if __name__ == '__main__':
	MyApp().run()
