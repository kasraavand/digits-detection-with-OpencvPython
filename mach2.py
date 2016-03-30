import cv2
import numpy as np


class detector():
    def __init__(self, *args, **kwargs):
        self.raw_pic_name = kwargs['raw_pic']
        self.detection_number = kwargs['detection']
        self.raw_pic = self.read_raw_image()
        self.detection_pic = self.get_dtection_image()
        self.detection_height = self.img1.shape[0]
        self.detection_widths = self.img1.shape[1]
        self.result = self.detect()
        # gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        # blur1 = cv2.GaussianBlur(gray1,(5,5),0)
        # ret1, thresh1 = cv2.threshold(blur1, 127, 255,0)

    def get_dtection_image(self):
        file_name = 'distinct_digits/{}.png'.format(self.detection_number)
        img = cv2.imread(file_name)
        return img

    def read_raw_image(self):
        img = cv2.imread(self.main_pic)
        return img

    def detect(self):
        gray2 = cv2.cvtColor(self.raw_pic, cv2.COLOR_BGR2GRAY)
        blur2 = cv2.GaussianBlur(gray2, (5, 5), 0)
        ret, thresh2 = cv2.threshold(blur2, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh2, 2, 1)

        for cnt in contours:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if (h > 27 and h < 35):
                tempim = self.raw_pic[y:y + h, x:x + w]
                new = cv2.resize(tempim, (self.detection_widths,
                                          self.detection_height))
                # new = np.float32(new)
                res = cv2.matchTemplate(self.detection_pic, new, 1)
                if res < 0.18:
                    cv2.rectangle(self.raw_pic, (x, y), (x + w, y + h), (0, 0, 255), 2)
        return self.raw_pic

    def show(self):
        cv2.imshow('result', self.result)
        cv2.waitKey(0)

    def write(self):
        cv2.imwrite('result.png', self.result)
