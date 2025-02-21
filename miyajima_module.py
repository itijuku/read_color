import cv2
import numpy as np
import picamera2
import time
from PIL import Image


class get_color:
    def __init__(self) -> None:
        self.file_name = "input.jpg"
        self.del_range = 3500
        self.picam2 = picamera2.Picamera2()

        # self.lower_w = np.array([10,20,100])
        # self.upper_w = np.array([30,57,220])
    
        # self.lower_green = np.array([60,64,0])
        # self.upper_green = np.array([90,255,255])
        
        # self.lower_y = np.array([20,90,0])
        # self.upper_y = np.array([45,255,255])
    
        # self.lower_red1 = np.array([0,64,0])
        # self.upper_red1 = np.array([2,255,255])
        # self.lower_red2 = np.array([150,64,0])
        # self.upper_red2 = np.array([179,255,255])
    

    def get_image(self):
        if not(".jpg" in self.file_name):
            self.file_name = str(self.file_name) + ".jpg"
        self.picam2.start_preview()
        config = self.picam2.create_preview_configuration(main={"size":(1919,600)})
        self.picam2.configure(config)
        self.picam2.start()

        # time.sleep(2)
        self.picam2.capture_file(self.file_name)

        self.picam2.stop
        self.file = self.file_name
        im = Image.open(self.file_name)
        im.crop((0, 450, 1919, 575)).save(self.file_name, quality=95)
        image = cv2.imread(self.file_name)

        return _cognition(image,self.del_range)
        



class _cognition():
    def __init__(self,image,del_range):
        self.color_data = []
        self.len_block = []

        self.image = image

        self.del_range = del_range

        self.lower_w = np.array([5,5,100])
        self.upper_w = np.array([30,60,220])
    
        self.lower_green = np.array([60,64,0])
        self.upper_green = np.array([90,255,255])
        
        self.lower_y = np.array([20,90,0])
        self.upper_y = np.array([45,255,255])
    
        self.lower_red1 = np.array([0,64,0])
        self.upper_red1 = np.array([2,255,255])
        self.lower_red2 = np.array([150,64,0])
        self.upper_red2 = np.array([179,255,255])
        
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        

        
        mask_red1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        mask_red2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        mask_y = cv2.inRange(hsv, self.lower_y, self.upper_y)
        
        mask_green = cv2.inRange(hsv, self.lower_green, self.upper_green)
        mask_w = cv2.inRange(hsv, self.lower_w, self.upper_w)

        
        # maskdata = cv2.bitwise_or(mask_red, mask_blue)

        self.x_data = []
        self.y_data = []
        self.mask = cv2.bitwise_and(image,image, mask=mask_w)
        contours, hierarchy = cv2.findContours(
        mask_w, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = list(filter(lambda x: cv2.contourArea(x) > self.del_range, contours))#小さいの削除
        cv2.drawContours(self.image, contours, -1, color=(0, 0, 255), thickness=2)
        # for i in contours:
        self.len_block.append(len(contours))
        x, y, w, h = cv2.boundingRect(contours[0])
        self.x_data.append(x)
        self.y_data.append(y)
            
            
        
        self.mask = cv2.bitwise_and(self.image, self.image, mask=mask_red)
        contours, hierarchy = cv2.findContours(
        mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = list(filter(lambda x: cv2.contourArea(x) > self.del_range, contours))#小さいの削除
        cv2.drawContours(self.image, contours, -1, color=(0, 0, 255), thickness=2)
        # for i in contours:
        self.len_block.append(len(contours))
        x, y, w, h = cv2.boundingRect(contours[0])
        self.x_data.append(x)
        self.y_data.append(y)
        
            
        self.mask = cv2.bitwise_and(self.image, self.image, mask=mask_green)
        contours, hierarchy = cv2.findContours(
        mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = list(filter(lambda x: cv2.contourArea(x) > self.del_range, contours))#小さいの削除
        cv2.drawContours(self.image, contours, -1, color=(0, 0, 255), thickness=2)
        # for i in contours:
        self.len_block.append(len(contours))
        x, y, w, h = cv2.boundingRect(contours[0])
        self.x_data.append(x)
        self.y_data.append(y)
        
        self.mask = cv2.bitwise_and(self.image, self.image, mask=mask_y)
        contours, hierarchy = cv2.findContours(
        mask_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = list(filter(lambda x: cv2.contourArea(x) > self.del_range, contours))#小さいの削除
        cv2.drawContours(self.image, contours, -1, color=(0, 0, 255), thickness=2)
        # for i in contours:
        self.len_block.append(len(contours))
        x, y, w, h = cv2.boundingRect(contours[0])
        self.x_data.append(x)
        self.y_data.append(y)
        self.color_data = self._mainloop()
        
    def show_image(self):
        cv2.namedWindow("image", cv2.WINDOW_NORMAL)

        cv2.imshow("image",self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def _hantei(self,i) -> str:
        if i==0:return "w"
        elif i==1:return "r"
        elif i==2:return "g"
        elif i==3:return "y"
        
    def _mainloop(self) -> None:
        const_place = [] # 75,412,748,1094,1398,1617
        ue = 1689
        sita = 61
        for i in range(6):
            const_place.append((((ue - sita) / 5)*(i))+ sita)


        sort_data = list(self.x_data)
        sort_data.sort()

        end_data=["","","",""]



        for i in range(len(self.x_data)):
            if sort_data[0] == self.x_data[i]:
                end_data[0] = self._hantei(i)
                
            elif sort_data[1] == self.x_data[i]:
                end_data[1] = self._hantei(i)
                
            elif sort_data[2] == self.x_data[i]:
                end_data[2] = self._hantei(i)
                
            elif sort_data[3] == self.x_data[i]:
                end_data[3] = self._hantei(i)
        hiitasa = []
        for i in range(len(const_place)):
            sa = 1000000000
            for j in range(len(self.x_data)):
                if sa > abs(const_place[i] - self.x_data[j]):
                    sa = abs(const_place[i] - self.x_data[j])
            hiitasa.append(sa)


        sort_hiitasa = list(hiitasa)
        sort_hiitasa.sort()
        nanimonai = []
        for i in range(len(hiitasa)):
            if sort_hiitasa[len(sort_hiitasa)-1] == hiitasa[i] or sort_hiitasa[len(sort_hiitasa) - 2] == hiitasa[i]:
                nanimonai.append(i)




        end_data_list = []
        zure = 0
        for i in range(len(end_data) + 2):
            if not ((i) in nanimonai):
                end_data_list.append(end_data[i - zure])
            else:

                zure += 1
                end_data_list.append("")
        return end_data_list
        

                

            
        
                
            
                
                


        
if __name__ == "__main__":
    main = get_color()
    main.get_image()
    


