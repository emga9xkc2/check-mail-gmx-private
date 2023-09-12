import cv2
import numpy as np


PIXELS_EXTENSION = 22


class PuzleSolver:
    def __init__(self, piece_path, background_path):
        self.piece_path = piece_path
        self.background_path = background_path

    def get_position(self):
        template, x_inf, y_sup, y_inf = self.__piece_preprocessing()
        background = self.__background_preprocessing(y_sup, y_inf)

        res = cv2.matchTemplate(background, template, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        # cv2.imshow("Background", background)
        background = cv2.imread(self.background_path )
# Hiển thị ảnh sau khi tìm kiếm template (với vị trí của template được đánh dấu)
        cv2.rectangle(background, top_left, (top_left[0] + template.shape[1], top_left[1] + template.shape[0]), (0, 0, 255), 2)
        cv2.imwrite(r"C:\Users\Admin\Pictures\Screenshots\b2.jpg", background)


        # Chờ người dùng ấn phím bất kỳ để đóng cửa sổ hiển thị ảnh
        # cv2.waitKey(0)

        origin = x_inf
        end = (top_left[0] / 1.2307692307) + PIXELS_EXTENSION

        return end - origin

    def __background_preprocessing(self, y_sup, y_inf):
        background = self.__sobel_operator(self.background_path)
        background = background[y_sup:y_inf, :]
        background = self.__extend_background_boundary(background)
        background = self.__img_to_grayscale(background)

        return background

    def __piece_preprocessing(self):
        img = self.__sobel_operator(self.piece_path)
        x, w, y, h = self.__crop_piece(img)
        template = img[y:h, x:w]

        template = self.__extend_template_boundary(template)
        template = self.__img_to_grayscale(template)

        return template, x, y, h

    def __crop_piece(self, img):
        white_rows = []
        white_columns = []
        r, c = img.shape

        for row in range(r):
            for x in img[row, :]:
                if x != 0:
                    white_rows.append(row)

        for column in range(c):
            for x in img[:, column]:
                if x != 0:
                    white_columns.append(column)

        x = white_columns[0]
        w = white_columns[-1]
        y = white_rows[0]
        h = white_rows[-1]

        return x, w, y, h

    def __extend_template_boundary(self, template):
        extra_border = np.zeros((template.shape[0], PIXELS_EXTENSION), dtype=int)
        template = np.hstack((extra_border, template, extra_border))

        extra_border = np.zeros((PIXELS_EXTENSION, template.shape[1]), dtype=int)
        template = np.vstack((extra_border, template, extra_border))

        return template

    def __extend_background_boundary(self, background):
        extra_border = np.zeros((PIXELS_EXTENSION, background.shape[1]), dtype=int)
        return np.vstack((extra_border, background, extra_border))

    def __sobel_operator(self, img_path):
        scale = 1
        delta = 0
        ddepth = cv2.CV_16S

        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = cv2.GaussianBlur(img, (3, 3), 0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

        return grad

    def __img_to_grayscale(self, img):
        tmp_path = r"C:\Users\Admin\Pictures\Screenshots\sobel.png"
        cv2.imwrite(tmp_path, img)
        return cv2.imread(tmp_path, 0)

# solver = PuzleSolver(r"C:\Users\Admin\Pictures\Screenshots\c.png", r"C:\Users\Admin\Pictures\Screenshots\b.jpg")
# solution = solver.get_position()
# print(solution, 495 + solution)
# quit()
from playwright.sync_api import sync_playwright, Route, Request
from hplaywright import *




hpw = hplaywright()
p = hpw.openChrome()
p.goto("https://www.tencentcloud.com/account/register")
clicked = False
while 1:
    if not clicked:
        email = p.locatorPlaceholder("Please enter your email address")
        if email.displayed():
            email.type("adwqjhewjq@gmail.com")
            clicked = True
    else:
        c = p.locatorSelector(".tc-fg-item")
        if c.displayed():
            src = c.get_attribute("style")
            b = p.locatorSelector("#slideBg")
            if b.displayed():
                response = requests.get(src, stream=True)
                with open(r"C:\Users\Admin\Pictures\Screenshots\p.png", 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                src = b.get_attribute("style")
                response = requests.get(src, stream=True)
                with open(r"C:\Users\Admin\Pictures\Screenshots\b.jpg", 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                solver = PuzleSolver(r"C:\Users\Admin\Pictures\Screenshots\p.png", r"C:\Users\Admin\Pictures\Screenshots\b.jpg")
                solution = solver.get_position()
                print(solution)
                # c = p.locatorSelector(".yidun_slider")
                a_coordinates = c.bounding_box()
                if not a_coordinates:
                    continue

                a_x = int(a_coordinates['x'])
                a_y = int(a_coordinates['y'])

                new_x = a_x + int(solution)
                new_y = a_y

                delay = 0.1
                print(a_x,new_x )
                # Sử dụng phương thức mouse.move() để di chuyển chuột đến tọa độ mới
                mouse = p.mouse
                current_x, current_y = a_x, new_y
                step_x = (new_x - current_x) / 10
                step_y = (new_y - current_y) / 10
                # for i in range(10):
                #     mouse.move(current_x + step_x, current_y + step_y)
                #     time.sleep(delay)
                #     current_x, current_y = current_x + step_x, current_y + step_y
                mouse.move(a_x, a_y)

                # Sử dụng phương thức mouse.down() để giữ chuột và phương thức mouse.move() để di chuyển chuột đến tọa độ mới
                mouse.down()
                time.sleep(1)
                # mouse.move(new_x + solution - 10, new_y)
                out = False
                for i in range(10):
                    xmove = current_x + step_x
                    ymove = current_y + step_y
                    if xmove > new_x:
                        xmove = new_x
                        out = True
                    if ymove > new_y:
                        ymove = new_y
                    mouse.move(xmove, ymove)
                    if out:
                        break
                    time.sleep(delay)
                    current_x, current_y = current_x + step_x, current_y + step_y
                # Sử dụng phương thức mouse.up() để thả chuột
                mouse.up()
                # print("abc")
    time.sleep(1)
