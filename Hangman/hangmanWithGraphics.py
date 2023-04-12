"""
The hangman game
"""

import random as r
import pygame
import os
import time
import sys

pygame.init()
pygame.font.init()
pygame.mixer.init()
width, height = 1200, 700


#categories (města, filmy, knihy, seriály)
#20 největších měst v ČR (podle počtu obyvatel, zdroj:cs.wikipedia.org)
CityCategory = ["Praha", "Brno", "Ostrava", "Plzeň", "Liberec", "Olomouc", "České budějovice", "Hradec Králové", "Ústí nad Labem", "Pardubice", "Zlín", "Havířov", "Kladno", "Most", "Opava", "Frýdek-Místek", "Jihlava", "Karviná", "Teplice", "Chomutov"]
#19 nejlepších filmů podle csfd
MovieCategory = ["Vykoupení z věznice Shawhank", "Forrest Gump", "Zelená míle", "Přelet nad kukaččím hnízdem", "Sedm", "Schindlerův seznam", "Kmotr", "Dvanáct rozhněvaných mužů", "Nedotknutelní", "Pelíšky", "Terminátor Den zůčtování", "Pulp Fiction Historky z podsvětí","Pán prstenů Společenstvo Prstenu","Mlčení jehňátek", "Tenkrát na Západě", "Pán prstenů Návrat krále", "Temný rytíř", "Gran Torino", "The Matrix"]
#20 knih z povinné četby k maturitě
BookCategory = ["Staré pověsti české", "Oliver Twist", "Stopařův průvodce Galaxií", "Pýcha a předsudek", "Zločin a trest", "Dekameron", "Lakomec", "Utrpení mladého Werthera", "Canterburské povídky", "Kupec benátský", "Na Větrné hůrce", "Sluha dvou pánů", "Romeo a Julie", "Tyrolské elegie", "Svatý Xaverius", "Jak je důležité míti Filipa", "Velký Gatsby", "Podivný případ se psem", "Pes baskervillský"]
#20 nejlepšísch seriálů podle csfd
SeriesCategory = ["Černobyl", "Bratrstvo neohrožených", "Narcos", "Tom a Jerry", "Simpsonovi", "Perníkový táta", "Byl jednou jeden život", "Sherlock", "Gangy z Birminghamu", "Hra o trůny", "Rick a Morty", "Knick Doktoři bez hranic", "Stranger Things", "Domek z karet", "Dámský gambit", "La casa de papel", "Teorie velkého třesku", "Přátelé", "Červený trpaslík", "Pat a mat"]


čárkyHáčky = {"a":["á","Á"], "e":["é","ě","É","Ě"], "i":["í","Í"], "o":["ó","Ó"], "u":["ů","Ů","ú","Ú"], "y":["ý","Ý"], "c":["č","Č"], "d":["ď","Ď"], "n":["ň","Ň"], "r":["ř","Ř"], "s":["š","Š"], "t":["ť","Ť"], "z":["ž","Ž"]}

pun = ["!", ",", "(", ")", "-", "[", "]", "{", "}", ";", ":", "'", "<", ">", ".", "/", "?", "@", "#", "$", "%", "^", "&", "*", "_", "~", 1, 2, 3, 4, 5, 6, 7, 8, 9, '§']



#hudba
backgroundMusic = os.path.join("Assets/music", "TragicStory.wav")
click = pygame.mixer.Sound(os.path.join("Assets/music", "click.mp3"))
chalk = pygame.mixer.Sound(os.path.join("Assets/music", "chalk.mp3"))
end = pygame.mixer.Sound(os.path.join("Assets/music", "chalkEnd.wav"))
beep = pygame.mixer.Sound(os.path.join("Assets/music", "beep.wav"))
chalkEnd = pygame.mixer.Sound(os.path.join("Assets/music", "win.wav"))


#obrázky
background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background.jpg")), (width,height))
hang11 = pygame.image.load(os.path.join("Assets", "obesenec11.png"))
hang10 = pygame.image.load(os.path.join("Assets", "obesenec10.png"))
hang9 = pygame.image.load(os.path.join("Assets", "obesenec9.png"))
hang8 = pygame.image.load(os.path.join("Assets", "obesenec8.png"))
hang7 = pygame.image.load(os.path.join("Assets", "obesenec7.png"))
hang6 = pygame.image.load(os.path.join("Assets", "obesenec6.png"))
hang5 = pygame.image.load(os.path.join("Assets", "obesenec5.png"))
hang4 = pygame.image.load(os.path.join("Assets", "obesenec4.png"))
hang3 = pygame.image.load(os.path.join("Assets", "obesenec3.png"))
hang2 = pygame.image.load(os.path.join("Assets", "obesenec2.png"))
hang1 = pygame.image.load(os.path.join("Assets", "obesenec1.png"))

#fonty
font = "Blackadder ITC"
hangmanFont = pygame.font.SysFont(font, 200)
textFont = pygame.font.SysFont(font, 80)
tajenkaFont = pygame.font.SysFont("Courier New", 70)
abcFont = pygame.font.SysFont("Courier New", 55)
answerFont = pygame.font.SysFont("Courier New", 30)
prohraFont = pygame.font.SysFont(font, 140)

#barvy
white = 255,255,255


#napsání tajenky z vybraného slova - dodání písmen
def WritingWord(word, guess):
	win.blit(background, (0,0))
	tajenka = ""
	for letter in word:
		if letter == " ":
			tajenka += " "
		elif letter in guess:
			tajenka += letter
		else:
			tajenka += "-"

	if len(tajenka)<26:
		puzzleText = tajenkaFont.render(tajenka, 1, white)
		win.blit(puzzleText, (width/2-(puzzleText.get_width()/2),30))
	else:
		parts = tajenka.split()
		partOne = ""
		partTwo = ""
		number = 0
		while number < len(parts):
			if len(partOne)+len(parts[number])<26:
				partOne += parts[number]+" "
				number += 1
			else:
				partTwo += parts[number]+" "
				number += 1
		partOneText = tajenkaFont.render(partOne,1, white)
		partTwoText = tajenkaFont.render(partTwo, 1, white)
		win.blit(partOneText, (width/2-(partOneText.get_width()/2),30))
		win.blit(partTwoText, (width/2-(partTwoText.get_width()/2),100))

	pygame.display.update()

#kreslení oběšence
def hangman(m):
	x= 560
	y= 140

	if m == 1:
		win.blit(hang1, (x, y))
	elif m == 2:
		win.blit(hang2, (x, y))
	elif m == 3:
		win.blit(hang3, (x, y))
	elif m == 4:
		win.blit(hang4, (x, y))
	elif m == 5:
		win.blit(hang5, (x, y))
	elif m == 6:
		win.blit(hang6, (x, y))
	elif m == 7:
		win.blit(hang7, (x, y))
	elif m == 8:
		win.blit(hang8, (x, y))
	elif m == 9:
		win.blit(hang9, (x, y))
	elif m == 10:
		win.blit(hang10, (x, y))
	elif m == 11:
		win.blit(hang11, (x, y))
	pygame.display.update()

#tlačítka na kategorie
class button():
	def __init__(self, x, y, text):
		self.text = text
		self.rect = self.text.get_rect()
		self.rect.topleft = (x,y)

	def draw(self):
		win.blit(self.text,(self.rect.x, self.rect.y))

	def clicked(self):
		return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

#úvod do hry a kategorie
def opening():
	win.blit(background, (0,0))
	hangmanText = hangmanFont.render("Hangman", 1, white)
	win.blit(hangmanText, (width/2-(hangmanText.get_width()/2), 60))
	pygame.display.update()

	categoryText = textFont.render("Choose a category:", 1, white)
	win.blit(categoryText, (50, 345))

	CityText = textFont.render("Cities",1, white)
	MovieText = textFont.render("Films",1, white)
	BookText = textFont.render("Books",1, white)
	SeriesText = textFont.render("Series",1, white)
	global city_button
	global book_button
	global movie_button
	global series_button
	city_button = button(180, 500, CityText)
	book_button = button(180+CityText.get_width()+40, 500, BookText)
	movie_button = button(180+CityText.get_width()+BookText.get_width()+40*2,500, MovieText)
	series_button = button(180+CityText.get_width()+BookText.get_width()+MovieText.get_width()+40*3,500, SeriesText)
	#tlačítka
	city_button.draw()
	book_button.draw()
	movie_button.draw()
	series_button.draw()
	pygame.display.update()

#výběr kategorie
def category():
	global c
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		if city_button.clicked():
			c = CityCategory
			pygame.mixer.Sound.play(click)
			break
		if book_button.clicked():
			c = BookCategory
			pygame.mixer.Sound.play(click)
			break
		if movie_button.clicked():
			c = MovieCategory
			pygame.mixer.Sound.play(click)
			break
		if series_button.clicked():
			c = SeriesCategory
			pygame.mixer.Sound.play(click)
			break

#abeceda
def alphabet(x,y):
	abcd = ""
	global abc
	for e in abc:
		if e in guess and e!=" ":
			abcd += " "
		else:
			abcd+=e
	abc = abcd


	aText = abcFont.render(abc[:10], 1, white)
	bText = abcFont.render(abc[10:20],1, white)
	cText = abcFont.render(abc[20:30], 1, white)
	dText = abcFont.render(abc[30:40],1,white)
	eText = abcFont.render(abc[40:50],1, white)
	fText = abcFont.render("    "+abc[50], 1, white)
	win.blit(aText, (x,y))
	win.blit(bText, (x,y+70))
	win.blit(cText, (x,y+2*70))
	win.blit(dText, (x,y+3*70))
	win.blit(eText, (x,y+4*70))
	win.blit(fText, (x,y+5*70))
	pygame.display.update()			

#jestli výhra nebo prohra
def control():
	global run
	#prohra
	if mistakes == 11:
			prohra()
	#výhra
	for e in word:
		if e not in guess:
			výhra = False
			break
		else:
			výhra = True
	if výhra:
		winn()
		
#kontrola správnosti
def chyba():
	global mistakes
	if letter not in word.lower():
			if letter not in čárkyHáčky:
				mistake = True
			else:
				for e in čárkyHáčky[letter]:
					if e in word:
						mistake = False
						for e in word:
							if e not in guess:
								pygame.mixer.Sound.play(beep)
								break
						break
					else:
						mistake = True
	else:
		for e in word:
			if e not in guess:
				pygame.mixer.Sound.play(beep)
				break
		mistake = False

	if mistake and mistakes !=10:
		pygame.mixer.Sound.play(chalk)
		mistakes += 1
	elif mistake:
		pygame.mixer.Sound.play(chalkEnd)
		mistakes +=1

#obrazovka výhry
def winn():
	global run
	win.blit(background, (0,0))
	winnText = hangmanFont.render("Výhra!!!",1, white)
	slovoText = answerFont.render("slovo: "+word, 1, white)
	win.blit(winnText,(width/2-winnText.get_width()/2, height/2-winnText.get_height()/2-80))
	win.blit(slovoText, (width/2-slovoText.get_width()/2, height/2-slovoText.get_height()/2+100))
	pygame.display.update()

	pygame.mixer.Sound.play(end)
	clicked = False
	while not clicked:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
				pygame.mixer.Sound.play(click)
				run = False
				time.sleep()
				clicked = True


#obrazovka prohra
def prohra():
	global run
	win.blit(background, (0,0))
	prohraText = prohraFont.render("KONEC HRY",1, white)
	slovoText = answerFont.render("slovo: "+word, 1, white)
	win.blit(prohraText,(width/2-prohraText.get_width()/2, height/2-prohraText.get_height()/2-60))
	win.blit(slovoText, (width/2-slovoText.get_width()/2, height/2-slovoText.get_height()/2+50))
	pygame.display.update()
	clicked = False
	while not clicked:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
				pygame.mixer.Sound.play(click)
				run = False
				time.sleep(0.5)
				clicked = True



#převod klinutí na písmeno
def posToLetter(x,y):
	#řádek
	if y>240 and y<305 :
		row = 0
	elif y>306 and y<371 :
		row = 1
	elif y>375 and y<437 :
		row = 2
	elif y>450 and y<520 :
		row = 3
	elif y>528 and y<580 :
		row = 4
	elif y>600 and y<650:
		row = 5

	#sloupek
	if x>125 and x<163 :
		column = 0
	elif x>185 and x<232 :
		column = 1
	elif x>254 and x<295 :
		column = 2
	elif x>319 and x<364 :
		column = 3
	elif x>389 and x<426 :
		column = 4

	pismena = [["a","b", "c", "d", "e"],["f","g", "h", "i", "j"],["k","l","m","n","o"],["p","q","r","s","t"],["u","v","w","x","y"],[" "," ","z"]]

	try:
		letter = pismena[row][column]
		return letter
	except:
		return 10







#okno
win = pygame.display.set_mode((width,height))
pygame.display.set_caption('Hangman')

pygame.mixer.music.load(backgroundMusic)
pygame.mixer.music.play(-1)


#game
while True:
	opening()
	category()
	win.blit(background, (0,0))
	pygame.display.update()

	#hádané slovo
	word = r.choice(c)

	#abeceda
	abc = "a b c d e f g h i j k l m n o p q r s t u v w x y z"

	#písmena, která už hráč hádal
	guess = [" "]

	#počet chyb
	mistakes = 0


	WritingWord(word, guess)
	alphabet(130,240)
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			
			if event.type == pygame.KEYDOWN:
				letter = pygame.key.name(event.key)
				letter = letter.lower()
				#písmena do guess
				if letter not in guess and letter not in pun:
					guess.append(letter)
					guess.append(letter.upper())
					if letter in čárkyHáčky:
						guess.extend(čárkyHáčky[letter])
					WritingWord(word, guess)
					alphabet(130,240)
					chyba()
					hangman(mistakes)
					control()
			#tlačítka abecedy
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = str(pygame.mouse.get_pos())
				pos = pos[1:-1]
				x,y = pos.split(",")
				letter = posToLetter(int(x),int(y))
				if letter !=10:
					#písmena do guessu
					if letter not in guess and letter not in pun:
						guess.append(letter)
						guess.append(letter.upper())
						if letter in čárkyHáčky:
							guess.extend(čárkyHáčky[letter])
						WritingWord(word, guess)
						alphabet(130,240)
						chyba()
						hangman(mistakes)
						control()




pygame.quit()