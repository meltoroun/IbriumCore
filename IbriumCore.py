from cmath import pi, tan
import cv2
import imutils
import numpy


# Распознование теплопотерь на снимке
def recognize_loss(img):
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_grey = cv2.GaussianBlur(img_grey, (3, 3), 0)
    thresh = 100
    ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
    heat_loss, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, heat_loss, -1, (1, 1, 150), -10)
    cv2.drawContours(img, heat_loss, -1, (0, 255, 255), 1)
        

# Фильтрация недействительного источника теплопотерь
def filtration(img, f_mode=4):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(gray, 1, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 45))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    contours = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    for c in contours:
        p = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * p, True)
        if len(approx) == f_mode:
            cv2.drawContours(img, [approx], -1, (0, 255,), -10)
            cv2.drawContours(img, [approx], -1, (255, 255, 255), 4)


# Примерный расчет периметра зон теплопотерь
def heat_loss_perimetr_calc(heat_loss):
    for heat in heat_loss:
        perimetr = cv2.contourArea(heat)
    return perimetr
    

# Расчет ширины обзора по горизонтали/вертикали (метры)
def view_width_calc(fov_hor, fov_vert, k):
    x1 = 2*tan((pi*fov_hor)/(2*180))*k
    x2 = 2*tan((pi*fov_vert)/(2*180))*k 
    print(x1, x2)
    return x1, x2


# Расчет минимального размера объекта (сторона квадрата) - S(приходящийся на один пиксель детектора) (см)
def min_obj_size_calc(x1, px_hor):
    s = (x1/px_hor)*100
    return s


# Расчет отношения D:S
def ds_calc(k, s):
    ds = (k/s)*100
    return ds


# Расчет пространственного разрешения или мгновенный угол поля зрения(iFov - Instantaneous Field of View) (мрад)
def ifov_calc(fov_hor, px_hor):
    iFoV = (fov_hor/px_hor)*(pi*180)*10
    return iFoV

# Расчет dT
def dt_calc(d, t):
    dT = d-t
    return dT


# Расчет теплопотерь (на метр квадратный)
def heat_calc(rctg, dT, R):
    q = (rctg*dT)/R
    return q


# Копирайтер изображений 
def copiraiter(img):
    img_copy = img
    return img_copy


# Конкатенация двух изображений для игнорирования температурной шкалы (Fluke only)
def concatenation(img, img_copy=0, x=700, y=640, xis=1):
    img = img[0:x, 0:y]
    if img_copy == 0:
        img_copy = img
    vis = numpy.concatenate((img, img_copy), axis=xis)
    return vis[0:740, 700:1300]


# Визуализация 3D
def vizualizator_3d():
    return 1


# Конвертация 3D
def convertation_3d():
    return 1


# Выдача основных статусов
def status_manager(r, g, b):
    recommend_sys(1) if (r == 150) else recommend_sys(2)
    recommend_sys(0) if (r == 0 and g == 255 and b == 255) else recommend_sys(4)


# Рекомендательный блок
def recommend_sys(rec_status):
    match rec_status:
        case 0:
            text = "Это окно"
            return text
        case 1:
            text = "Теплопотери. Щель/соединение:\n" \
                   "Монтаж теплозащитных конструкций\n" \
                   "(пена, минеральная вата), вспенивание, герметизация"
            return text
        case 2:
            text = "Нет теплопотерь"
            return text
        case 4:
            text = "Неожиданная ошибка"
            return text