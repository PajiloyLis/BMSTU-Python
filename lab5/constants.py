import numpy as np

FPS = 30

# Время полета до планет
TIME_TO_JUP = 9.5
TIME_TO_SATURN = 19.5

# Основные размерности
GELIOCENTER = np.array([300, 600])
AU = 50
STD_SIZE = 30
SUN_D = 30
EARTH_PERIOD = 6

# Дата начала
START_YEAR = 1977
START_MONTH = 8

# Отношения периодов обращения
REL_MERCURY_PERIOD = 365.3 / 88
REL_VENUS_PERIOD = 365.3 / 224.7
REL_EARTH_PERIOD = 1
REL_MARS_PERIOD = 365.3 / 687
REL_JUPITER_PERIOD = 365.3 / (11 * 365.3 + 314)
REL_SATURN_PERIOD = 365.3 / (29 * 365.3 + 168)
REL_URANUS_PERIOD = 365.3 / (84 * 365.4 + 4)
REL_NEPTUN_PERIOD = 365.3 / (164*365.3 + 292)

# Координаты относительно солнца в начале
MERCURY_DIST = np.array([AU * 0.387, 0])
VENUS_DIST = np.array([AU * 0.723, 0])
EARTH_DIST = np.array([AU, 0])
MARS_DIST = np.array([AU * 1.52, 0])
JUPITER_DIST = np.array([AU*2, 4.8*AU])
SATURN_DIST = np.array([AU * 9, 0])
URANUS_DIST = np.array([AU*19.1914, 0])
NEPTUN_DIST = np.array([AU*30.1, 0])

# Угловая скорость Земли
ANGLE = 2*np.pi/(FPS*EARTH_PERIOD)