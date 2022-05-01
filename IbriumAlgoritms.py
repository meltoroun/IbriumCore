import cv2
from tkinter import filedialog
import IbriumCore as core


img = cv2.imread(filedialog.askopenfilename())
core.recognize_loss(img)
core.filtration(img, 4)
vis = core.concatenation(img)


while True:
    cv2.imshow("IBRIUM TEAM - ALG", vis)
    cv2.namedWindow("IBRIUM TEAM - ALG")
    key = cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()