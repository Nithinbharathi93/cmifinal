from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.button import Button
import cv2
import numpy as np
from kivy.graphics.texture import Texture


class VideoProcessor(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')


        self.capture = cv2.VideoCapture(0)  # Access the camera (change the parameter if using a different camera index)

        if not self.capture.isOpened():
            print("Error accessing the camera")
            return

        self.image = Image()
        layout.add_widget(self.image)

        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        layout.add_widget(buttons_layout)

        self.red_button = Button(text='Red', size_hint=(0.1, 1))
        self.red_button.bind(on_press=lambda x: self.set_red_values())
        buttons_layout.add_widget(self.red_button)

        self.blue_button = Button(text='Blue', size_hint=(0.1, 1))
        self.blue_button.bind(on_press=lambda x: self.set_blue_values())
        buttons_layout.add_widget(self.blue_button)

        self.green_button = Button(text='Green', size_hint=(0.1, 1))
        self.green_button.bind(on_press=lambda x: self.set_green_values())
        buttons_layout.add_widget(self.green_button)

        self.lower_green = np.array([40, 40, 40])
        self.upper_green = np.array([80, 255, 255])

        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Update at 30 fps

        return layout

    def process_frame(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_green, self.upper_green)
        frame[mask > 0] = (255, 255, 255)
        mask_inv = cv2.bitwise_not(mask)
        frame[mask_inv > 0] = (0, 0, 0)
        return frame

    def update(self, dt):
        ret, frame = self.capture.read()

        if ret:
            processed_frame = self.process_frame(frame)

            buf1 = cv2.flip(processed_frame, 0)
            buf2 = buf1.tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf2, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture

    def set_red_values(self):
        # Modify red values (adjust these values as needed)
        self.lower_green = np.array([0, 40, 40])
        self.upper_green = np.array([20, 255, 255])

    def set_blue_values(self):
        # Modify blue values (adjust these values as needed)
        self.lower_green = np.array([90, 40, 40])
        self.upper_green = np.array([130, 255, 255])

    def set_green_values(self):
        # Modify green values (adjust these values as needed)
        self.lower_green = np.array([40, 40, 40])
        self.upper_green = np.array([80, 255, 255])

    def on_stop(self):
        self.capture.release()

if __name__ == '__main__':
    VideoProcessor().run()
