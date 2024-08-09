from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.clock import Clock, mainthread
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.image import AsyncImage
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.utils import get_color_from_hex
from datetime import datetime
from kivy.uix.label import Label
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import NumericProperty
from kivymd.icon_definitions import md_icons
import kivy.resources
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty
from kivy.config import Config


import cv2
import mediapipe as mp
import numpy as np
import os, sys
import time
import threading

from keras.models import load_model



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if getattr(sys, 'frozen', False):
    # this is a Pyinstaller bundle
    kivy.resources.resource_add_path(sys._MEIPASS)
    kivy.resources.resource_add_path(os.path.join(sys._MEIPASS, 'materials'))
# working_dir = os.path.dirname(os.path.abspath('Unified_Model_01.h5'))
# LabelBase.register(name='app_font', fn_regular=f'{working_dir}\\font\\zh-cn.ttf')
LabelBase.register(name='app_font', fn_regular=resource_path("font/zh-cn.ttf"))

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

model_path_beginner = resource_path('Unfiied_Model_03_Beginner_Best.h5')
model_path_medium = resource_path('Medium_Model_Simple_02.h5')

pose_recognition_model_beginner = load_model(model_path_beginner)
pose_recognition_model_medium = load_model(model_path_medium)

pose_dict_beginner = {0 : "Bridge Pose",
             1 : "Butterfly Pose",
             2 : "Chair Pose",
             3 : "Childs Pose",  
             4 : 'Cobra Pose',
             5 : 'Corpse Pose',
             6 : 'Dolphin Pose',
             7 : 'Downward Facing Dog',
             8 : 'Garland Pose',
             9 : 'Happy Baby Pose',
             10 : 'Mountain Pose',
             11 : 'Plank Pose',
             12 : 'Seated Forward Bend Pose',
             13 : 'Sphinx Pose',
             14 : 'Tree Pose',
             15 : 'Triangle Pose',
             16 : 'Warrior Pose I',
             17 : 'Warrior Pose II'}

pose_dict_medium = {0 : 'Boat Pose',
                    1 : 'Cow Face Pose',
                    2 : 'Downward Facing Dog',
                    3 : 'Puppy Pose',
                    4 : 'Gate Pose',
                    5 : 'Half Pigeon Pose',
                    6 : 'Low Lunge Pose',
                    7 : 'Reclining Hand to Toe',
                    8 : 'Revolved Chair Pose',
                    9 : 'Sphinx Pose',
                    10 : 'Straight Forward Bend',
                    11 : 'Thread the Needle',
                    12 : 'Tree Pose',
                    13 : 'Warrior Pose III '}

image_dict = {"Downward Facing Dog" : "materials/Yogaposes/DownwardFacingDogPose.jpg",
              "Child Pose" : "materials/Yogaposes/Childspose.jpg",
              "Mountain Pose" : "materials/Yogaposes/Mountainpose.jpg",
              "Warrior Pose I" : "materials/Yogaposes/WarriorIPose.jpg",
              "Warrior Pose II" : "materials/Yogaposes/WarriorIIPose.jpg",
              "Warrior Pose III" : "materials/Yogaposes/WarriorIIIPose.jpg",
              "Tree Pose" : "materials/Yogaposes/TreePose.jpg",
              "Dolphin Pose" : "materials/Yogaposes/DolphinPose.jpg",
              "Cobra Pose" : "materials/Yogaposes/CobraPose.jpg",
              "Seated Forward Bend Pose" : "materials/Yogaposes/SeatedForwardBendPose.jpg",
              "Bridge Pose" : "materials/Yogaposes/BridgePose.jpg",
              "Triangle Pose" : "materials/Yogaposes/TrianglePose.jpg",
              "Happy Baby Pose" : "materials/Yogaposes/HappyBabyPose.jpg",
              "Sphinx Pose" : "materials/Yogaposes/SphinxPose.jpg",
              "Corpse Pose" : "materials/Yogaposes/CorpsePose.jpg",
              "Chair Pose" : "materials/Yogaposes/ChairPose.jpg",
              "Garland Pose" : "materials/Yogaposes/GarlandPose.jpg",
              "Butterfly Pose" : "materials/Yogaposes/ButterflyPose.jpg",
              "Plank Pose" : "materials/Yogaposes/PlankPose.jpg",
              "Low Lunge Pose" : "materials/Yogaposes/LowLungePose.jpg",
              "Thread the Needle" : "materials/Yogaposes/ThreadTheNeedlePose.jpg",
              "Puppy Pose" : "materials/Yogaposes/PuppyPose.jpg",
              "Half Pigeon Pose" : "materials/Yogaposes/HalfPigeonPose.jpg",
              "Boat Pose" : "materials/Yogaposes/BoatPose.jpg",
              "Cow Face Pose" : "materials/Yogaposes/CowFacePose.jpg",
              "Reclining Hand to Toe" : "materials/Yogaposes/RecliningHandToBigToePose.jpg",
              "Revolved Chair Pose" : "materials/Yogaposes/RevolvedChairPose.jpg",
              "Standing Forward Bend" : "materials/Yogaposes/StandingForwardBendPose.jpg",
              "Stretching" : "materials/Yogaposes/Stretching.jpg",
              "Breathing" : "materials/Yogaposes/Breathing.jpg",
              "Prepare for Downward facing Dog" : "materials/Restposes/restdfd.jpg",
              "Camera Frame" : "materials/Yogaposes/Camerascreen.png",
              "Pose Frame" : "materials/Yogaposes/Posewindow.png",
              "Rest" : "materials/Yogaposes/Rest.jpg",
              "Prepare for Downward facing Dog" : "materials/Restposes/restdfd.jpg",
              "Prepare for Child Pose" : "materials/Restposes/restcp.jpg",
              "Prepare for Warrior Pose I" : "materials/Restposes/restw1.jpg",
              "Prepare for Warrior Pose II" : "materials/Restposes/restw2.jpg",
              "Prepare for Warrior Pose III" : "materials/Restposes/restw3.jpg",
              "Prepare for Tree Pose" : "materials/Restposes/resttp.jpg",
              "Prepare for Dolphin Pose" : "materials/Restposes/restdp.jpg",
              "Prepare for Cobra Pose" : "materials/Restposes/restcbrp.jpg",
              "Prepare for Seated forward Bend" : "materials/Restposes/restsefbp.jpg",
              "Prepare for Bridge Pose" : "materials/Restposes/restbrp.jpg",
              "Prepare for Triangle Pose" : "materials/Restposes/resttrp.jpg",
              "Prepare for Happy Baby Pose" : "materials/Restposes/resthbp.jpg",
              "Prepare for Sphinx Pose" : "materials/Restposes/restsxp.jpg",
              "Prepare for Corpse Pose" : "materials/Restposes/restcrpp.jpg",
              "Prepare for Chair Pose" : "materials/Restposes/restchp.jpg",
              "Prepare for Garland Pose" : "materials/Restposes/restglp.jpg",
              "Prepare for Butterfly Pose" : "materials/Restposes/restbfp.jpg",
              "Prepare for Plank Pose" : "materials/Restposes/restplp.jpg",
              "Prepare for Low Lunge Pose" : "materials/Restposes/restllp.jpg",
              "Prepare for Thread the Needle" : "materials/Restposes/restttnp.jpg",
              "Prepare for Puppy Pose" : "materials/Restposes/restpp.jpg",
              "Prepare for Half Pigeon Pose" : "materials/Restposes/resthpp.jpg",
              "Prepare for Boat Pose" : "materials/Restposes/restdfd.jpg",
              "Prepare for Cow Face Pose" : "materials/Restposes/restcfp.jpg",
              "Prepare for Reclining Hand to Toe" : "materials/Restposes/restrhtbtp.jpg",
              "Prepare for Revolved Chair Pose" : "materials/Restposes/restrcp.jpg",
              "Prepare for Standing Forward Bend" : "materials/Restposes/restsfbp.jpg"}
              
              
              
              

pose_difficulty = None

pre_session_check = False

class BackgroundImage(RelativeLayout):
    def __init__(self, source, **kwargs):
        super(BackgroundImage, self).__init__(**kwargs)

        self.image = AsyncImage(source=source, allow_stretch=True, keep_ratio=True)
        self.add_widget(self.image)

        Window.bind(on_resize=self.on_window_resize)
        self.on_window_resize(Window, Window.width, Window.height)

    def on_window_resize(self, instance, width, height):
        self.image.size = (width, height)
        self.image.pos = self.pos

class MainMenu(Screen):
    
    def on_kv_post(self, base_widget):
        Window.maximize()
    
    def quit_app(self):
        App.get_running_app().stop()

    def next_menu(self):
        global pre_session_check
        if pre_session_check is False:
            self.manager.transition = FadeTransition()
            self.manager.current = 'pre-session'
        else:
            self.manager.transition = FadeTransition()
            self.manager.current = 'session-library'

    pass

class Session(Screen):
    global pose_difficulty
    pose_list = []
    app = None
    breath_time_ref = 20
    pose_time_ref = 15
    stretch_time_ref = 60
    prepare_time_ref = 10
    long_rest_ref = 1
    time_left = 2
    timer_active = False
    first_pose = True
    current_pose_index = 0
    
    
    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
    
    def timer(self):
        i = 0
        while not self.timer_flag.is_set():
            time.sleep(1) # Clock that waits 1 second before updating
            print(self.time_left)
                
            if self.time_left > 0:
                self.time_left -= 1
                # self.update_timer_label(self.time_left)
                self.ids.timer_label.text = str(self.time_left)
            else:
                if self.first_pose is True:
                    self.ids.pose_label.text = self.pose_list[self.current_pose_index]
                    self.time_left = self.stretch_time_ref
                    self.ids.timer_label.text = str(self.time_left)
                    self.update_image(self.current_pose_index)
                    self.first_pose = False
                else: 
                    self.current_pose_index = self.current_pose_index + 1
                    if self.current_pose_index < len(self.pose_list):
                        self.ids.pose_label.text = self.pose_list[self.current_pose_index]
                        if self.pose_list[self.current_pose_index] == "Stretching":
                            print('stretching index', self.current_pose_index)
                            self.time_left = self.stretch_time_ref
                            self.ids.timer_label.text = str(self.time_left)
                            self.update_image(self.current_pose_index)
                        elif self.pose_list[self.current_pose_index] == "Breathing":
                            self.time_left = self.breath_time_ref
                            self.ids.timer_label.text = str(self.time_left)
                            self.update_image(self.current_pose_index)
                        elif 'Prepare for' in self.pose_list[self.current_pose_index]:
                            self.time_left = self.prepare_time_ref
                            self.ids.timer_label.text = str(self.time_left)
                            self.update_image(self.current_pose_index)
                        elif self.pose_list[self.current_pose_index] == "Long Rest":
                            self.time_left = self.long_rest_ref
                            self.ids.timer_label.text = str(self.time_left)
                        else:
                            self.time_left = self.pose_time_ref
                            self.update_image(self.current_pose_index)
                            self.ids.timer_label.text = str(self.time_left)
                        
                    # break
                    
                    else:       
                        self.activation_trigger()
                        self.change_screens(pose_difficulty)
                        
    @mainthread
    def change_screens(self, pose_difficulty):
        post_session_screen = self.manager.get_screen('post-session')
        post_session_screen.pose_difficulty = pose_difficulty
        self.manager.current = 'post-session'
    
    @mainthread
    def update_image(self, i):
        try:
            print(image_dict[self.pose_list[i]])
            self.pose_capture.source = image_dict[self.pose_list[i]]
        except:
            self.pose_capture.source = image_dict["Downward Facing Dog"]
            print({"No Image"})

        new_height = 200  
        self.ids.pose_frame.height = new_height


                    
    def timer_event(self):
        self.timer_thread.join()
        print("Do something since the timer has ended")

    def on_enter(self):
        global pose_difficulty

        self.current_pose_index = 0
        self.first_pose = True

        self.ids.calibration_state.text = "Calibration Phase"
        self.ids.session_start_button.text = "Start Calibration"

        if self.ids.session_start_button.disabled:
            self.ids.session_start_button.disabled = False

        self.time_left = 2
        self.prediction_flag = True
        self.frame_capture = self.ids.camera_frame
        self.pose_capture = self.ids.pose_frame
        self.calibration_check = True

        if pose_difficulty == "beginner15":
            self.pose_list = ["Stretching", "Breathing", "Mountain Pose", "Prepare for Downward facing Dog", "Downward Facing Dog", "Prepare for Child Pose", "Child Pose", "Prepare for Warrior Pose I", "Warrior Pose I", "Prepare for Warrior Pose I", "Warrior Pose I", "Prepare for Warrior Pose II", "Warrior Pose II", "Prepare for Warrior Pose II", "Warrior Pose II", "Prepare for Tree Pose", "Tree Pose", "Prepare for Tree Pose", "Tree Pose", "Prepare for Dolphin Pose", "Dolphin Pose", "Rest", "Stretching"]
        elif pose_difficulty == "beginner30":
            self.pose_list = ["Stretching", "Breathing", "Mountain Pose", "Prepare for Downward facing Dog", "Downward Facing Dog", "Prepare for Child Pose", "Child Pose", "Prepare for Warrior Pose I", "Warrior Pose 1", "Prepare for Warrior Pose I", "Warrior Pose 1", "Prepare for Warrior Pose II", "Warrior Pose II", "Prepare for Warrior Pose II", "Warrior Pose II", "Prepare for Tree Pose", "Tree Pose", "Prepare for Tree Pose", "Tree Pose", "Prepare for Dolphin Pose", "Dolphin Pose", "Long Rest", "Prepare for Cobra Pose", "Cobra Pose", "Prepare for Seated Forward Pose", "Seated Forward Pose", "Prepare for Bridge Pose", "Bridge Pose", "Prepare for Triangle Pose", "Triangle Pose", "Prepare for Triangle Pose", "Triangle Pose", "Prepare for Happy Baby Pose", "Happy Baby Pose", "Prepare for Sphinx Pose", "Sphinx Pose", "Prepare for Corpse Pose", "Corpse Pose", "Prepare for Chair Pose", "Chair Pose", "Prepare for Garland Pose", "Garland Pose", "Prepare for Butterfly Pose", "Butterfly Pose", "Prepare for Plank Pose", "Plank Pose", "Rest", "Stretching"]
        elif pose_difficulty == "normal15":
            self.pose_list = ["Stretching", "Breathing", "Downward Facing Dog", "Prepare for Tree Pose", "Tree Pose", "Prepare for Tree Pose", "Tree Pose", "Prepare for Warrior Pose III", "Warrior Pose III", "Prepare for Warrior Pose III", "Warrior Pose III", "Prepare for Sphinx Pose", "Sphinx Pose", "Prepare for Low Lunge Pose", "Low Lunge Pose", "Prepare for Thread the Needle", "Thread the Needle ", "Prepare for Thread the Needle", "Thread the Needle", "Prepare for Puppy Pose", "Puppy Pose", "Rest", "Stretching"]
        elif pose_difficulty == "normal30":
            self.pose_list = ["Stretching", "Breathing", "Downward Facing Dog", "Prepare for Tree Pose", "Tree Pose", "Prepare for Tree Pose", "Tree Pose", "Prepare for Warrior Pose III", "Warrior Pose III", "Prepare for Warrior Pose III", "Warrior Pose III", "Prepare for Sphinx Pose", "Sphinx Pose", "Prepare for Low Lunge Pose", "Low Lunge Pose", "Prepare for Thread the Needle", "Thread the Needle ", "Prepare for Thread the Needle", "Thread the Needle", "Prepare for Puppy Pose", "Puppy Pose", "Long Rest", "Prepare for Half Pigeon Pose", "Half Pigeon Pose", "Prepare for Half Pigeon Pose", "Half Pigeon Pose", "Prepare for Cow Face Pose", "Cow face Pose", "Prepare for Cow Face Pose", "Cow Face Pose", "Prepare for Boat Pose", "Boat Pose", "Prepare for Reclining Hand to Toe", "Reclining Hand to Toe", "Prepare for Reclining Hand to Toe", "Reclining Hand to Toe", "Prepare for Gate Pose", "Gate Pose", "Prepare for Gate Pose", "Gate Pose", "Prepare for Revolved Chair Pose", "Revolved Chair Pose", "Prepare for Revolved Chair Pose", "Revolved Chair Pose", "Prepare for Standing Forward Bend", "Standing Forward Bend", "Rest", "Stretching"]
        else:
            pose_difficulty = "beginner15"
            self.pose_list = ["Stretching", "Breathing", "Mountain Pose", "Prepare for Downward facing Dog", "Downward Facing Dog", "Prepare for Child Pose", "Child Pose", "Prepare for Warrior Pose I", "Warrior Pose I", "Prepare for Warrior Pose I", "Warrior Pose I", "Prepare for Warrior Pose II", "Warrior Pose II", "Prepare for Warrior Pose II", "Warrior Pose II", "Prepare for Tree Pose", "Tree Pose", "Prepare for Tree Pose", "Tree Pose", "Prepare for Dolphin Pose", "Dolphin Pose", "Rest", "Stretching"]
    
        print('Quick Test') 
        print(f'Camera: {self.app.CAMERA_ID}') 

    def on_leave(self):
        # This function just makes sure that all threads are exited on page exit.
        if hasattr(self, 'prediction_event') and self.prediction_event:
            self.prediction_event.cancel()

        if hasattr(self, 'capture') and self.capture:
            if self.capture.isOpened:
                self.capture.release()
        
        if hasattr(self, 'timer_flag') and self.timer_flag:
            self.timer_flag.set()

        if hasattr(self, 'calibration_event') and self.calibration_event:
            self.calibration_event.cancel()
        self.frame_capture.source = image_dict['Camera Frame']
        self.pose_capture.source = image_dict['Pose Frame']
        self.ids.pose_label.text = ""
            
    # Closes off all running threads and functions if still active so the application can exit without freezing.
    def on_stop(self):
        if hasattr(self, 'prediction_event') and self.prediction_event:
            self.prediction_event.cancel()

        if hasattr(self, 'capture') and self.capture:
            self.capture.release()
            if self.capture.isOpened:
                self.capture.release()
        
        if hasattr(self, 'timer_flag') and self.timer_flag:
            self.timer_flag.set()

        if hasattr(self, 'calibration_event') and self.calibration_event:
            self.calibration_event.cancel()

    def activation_trigger(self):
        if self.calibration_check:
            self.calibration_trigger()
            self.ids.session_start_button.text = "Calibrating"
            self.ids.session_start_button.disabled = True
            self.ids.pose_label.text = "Calibration Phase"
        else:
            self.ids.calibration_state.text = ''
            if self.ids.session_start_button.disabled:
                self.ids.session_start_button.disabled = False
            
            self.session_trigger()

        # use below for testing w/o calibration
        # self.session_trigger()
        
        
       
         
           
    @mainthread
    def calibration_count(self, visible_landmarks):
        self.ids.calibration_state.text = 'Calibration: ' + str(visible_landmarks) + " / 33 keypoints detected"

    def calibration_trigger(self):
        self.capture = cv2.VideoCapture(int(self.app.CAMERA_ID))
        self.calibration_event = Clock.schedule_interval(self.calibration, 1.0/33)

    def calibration(self, dt):
        if hasattr(self, 'capture') and self.capture:
            ret, frame = self.capture.read()
        if ret and self.calibration_check:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)
            if results.pose_landmarks:
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                
                new_width = 1900  # Adjust to your desired width
                new_height = 1100  # Adjust to your desired height
                frame = cv2.resize(frame, (new_width, new_height))
                
                
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                frame_flip = cv2.flip(frame, -1)
                texture.blit_buffer(frame_flip.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
                self.frame_capture.texture = texture
                visibility = 0.5
                visible_landmarks = sum(1 for landmark in results.pose_landmarks.landmark if landmark.visibility >= visibility)
                self.calibration_count(visible_landmarks)
                print(visible_landmarks)
                
                if visible_landmarks == 33:
                    self.calibration_check = False
                    
                    self.ids.camera_frame.size = (new_width, new_height)
            else:
                
                new_width = 1900  # Adjust to your desired width
                new_height = 1100  # Adjust to your desired height
                frame = cv2.resize(frame, (new_width, new_height))
                
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                frame_flip = cv2.flip(frame, -1)
                texture.blit_buffer(frame_flip.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
                self.frame_capture.texture = texture
                
                self.ids.camera_frame.size = (new_width, new_height)
        else:   
            if hasattr(self, 'capture') and self.capture:
                if self.capture.isOpened:
                    self.capture.release()
            if hasattr(self, 'calibration_event') and self.calibration_event:
                self.calibration_event.cancel()
                self.activation_trigger()
            




    def session_trigger(self):
        if self.prediction_flag is True:
            print('Prediction Flag True Statement')
            self.capture = cv2.VideoCapture(int(self.app.CAMERA_ID)) 
            self.ids.session_start_button.text = "Pause"
            self.prediction_flag = False
            self.prediction_event = Clock.schedule_interval(self.pose_estimation, 1.0 / 33)
            # self.ids.timer_label.text = str(self.time_left)
            # self.ids.pose_label.text = "Stretching"
            self.timer_flag = threading.Event()
            self.timer_thread = threading.Thread(target=self.timer, daemon=True).start()
        else:
            print('Prediction Flag False Statement')
            self.ids.session_start_button.text = "Resume"
            self.timer_flag.set()
            if self.capture:
                if self.prediction_event:
                    self.prediction_event.cancel()
                if self.capture.isOpened:
                    self.capture.release()
            self.prediction_flag = True
            self.frame_capture.texture = None
            self.ids.prediction_label.text = "None"
            self.ids.probability_label.text = "0.00"
            
        #TODO: Resuming the timer
        # if self.time_left > 0:
        #     self.start_timer(self.time_left)


    def pose_estimation(self, dt):
        global pose_difficulty
        normalized_landmarks_list = None
        class_name = 'None'
        max_probabilities = 0
        ret, frame = self.capture.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)

            height, width, _ = frame.shape
            if results.pose_landmarks:
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                landmarks = [(landmark.x if landmark is not None else None, landmark.y if landmark is not None else None) for landmark in results.pose_landmarks.landmark]
                detected_landmarks = [(x, y) for x, y in landmarks if x is not None and y is not None]
                undetected_landmarks = [(x, y) for x, y in landmarks if x is None and y is None]
                # landmark_locations = [1 if x is not None and y is not None else 0 for x, y in landmarks]
                # detected_landmarks_count = len(detected_landmarks)
                # undetected_landmarks_count = len(undetected_landmarks)
                normalized_landmarks = [(x / width if x is not None else None, y / height if y is not None else None) for x, y in landmarks]
                normalized_landmarks_list = np.array(normalized_landmarks)
                normalized_landmarks_list = normalized_landmarks_list.flatten().tolist()
                
                new_width = 1900  # Adjust to your desired width
                new_height = 1100  # Adjust to your desired height
                frame = cv2.resize(frame, (new_width, new_height))

                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                frame_flip = cv2.flip(frame, -1)
                texture.blit_buffer(frame_flip.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
                self.frame_capture.texture = texture
                self.ids.camera_frame.size = (new_width, new_height)
                
            else:
                
                new_width = 1900  # Adjust to your desired width
                new_height = 1100  # Adjust to your desired height
                frame = cv2.resize(frame, (new_width, new_height))
                
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                frame_flip = cv2.flip(frame, -1)
                texture.blit_buffer(frame_flip.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
                self.frame_capture.texture = texture
                self.ids.camera_frame.size = (new_width, new_height)

            if normalized_landmarks_list is not None:
                np.set_printoptions(precision=4, suppress=True)
                # print('Expected Input Shape: ', pose_recognition_model.input_shape)
                np_list = np.array(normalized_landmarks_list)
                np_list = np_list.reshape(1, -1)
                if pose_difficulty == 'beginner15' or pose_difficulty == 'beginner30':
                    predictions = pose_recognition_model_beginner.predict(np_list)
                elif pose_difficulty == "normal15" or pose_difficulty == "normal30":
                    predictions = pose_recognition_model_medium.predict(np_list)
                all_prediction_classifiers = predictions.argmax(axis=1)
                predicted_class = np.argmax(predictions, axis=1)
                predicted_class_int = predicted_class[0]
                if pose_difficulty == 'beginner15' or pose_difficulty == 'beginner30':
                    class_name = pose_dict_beginner[predicted_class_int]
                elif pose_difficulty == "normal15" or pose_difficulty == "normal30":
                    class_name = pose_dict_medium[predicted_class_int]
               
                # print(all_prediction_classifiers)
                # print(predicted_class)
                # print(predictions)
                max_probabilities = np.max(predictions, axis=1)
                converted_max = max_probabilities.item()
                rounded_max = round(converted_max, 5)
                self.ids.prediction_label.text = class_name
                if self.current_pose_index < len(self.pose_list):
                    if class_name == self.pose_list[self.current_pose_index]:
                        self.ids.prediction_label.color = [0,1,0,1]
                        
                    elif self.pose_list[self.current_pose_index] == "Stretching" or self.pose_list[self.current_pose_index] == "Breathing" or 'Prepare for' in self.pose_list[self.current_pose_index]:
                        self.ids.prediction_label.color = [0,0,0,1]
                   
                    else:
                        self.ids.prediction_label.color = [1, 0, 0, 1]
                # self.ids.prediction_label.text = class_name
                self.ids.probability_label.text = str(rounded_max)

                print(class_name)
                print(max_probabilities)

    
class SessionLibrary(Screen):
    def set_difficulty(self, difficulty):
        global pose_difficulty
        pose_difficulty = difficulty
        print(pose_difficulty)
    def on_enter(self):
        global pose_difficulty
        pose_difficulty = 'beginner15'
    

class PoseLibrary(Screen):
    pass


class DataTable(GridLayout):
    def __init__(self, **kwargs):
        super(DataTable, self).__init__(**kwargs)
        self.cols = 3
        self.spacing = 10

        self.add_widget(Label(text='Date'))
        self.add_widget(Label(text='Difficulty'))
        self.add_widget(Label(text='Time'))

    def add_row(self, difficulty, time):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.add_widget(Label(text=date))
        self.add_widget(Label(text=difficulty))
        self.add_widget(Label(text=str(time)))
        
    def reload_data(self, data_table):
        # Clear existing widgets
        self.clear_widgets()

        # Add headers
        self.add_widget(Label(text='Date'))
        self.add_widget(Label(text='Difficulty'))
        self.add_widget(Label(text='Time'))

        # Add rows from data_table
        for row in data_table:
            self.add_row(row['difficulty'], row['time'])


class History(Screen):
    data_table = []
    
    def add_data_row(self, difficulty, time):
        
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current date and time
        date = current_date
        print(f"Received: Difficulty: {difficulty}, Time: {time}, Date: {date}")
        
        
        
        self.data_table.append({
            'date': current_date,
            'difficulty': difficulty,
            'time': time
        })
        
        self.ids.data_table.reload_data(self.data_table)
        

        # Optionally, you can print the data table to check if the row is added
        print("Data Table:", self.data_table)


class Setting(Screen):
    pass


class About(Screen):
    pass


class Instruction(Screen):
    pass


class InstructionAdv(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.adjust_self)
        Window.bind(size=self.adjust_to_window)

    def adjust_self(self, *args):
        # Adjustments that depend on the widget's own size
        pass

    def adjust_to_window(self, instance, value):
        # Adjust size of the carousel
        self.ids.image_carousel4.size = (Window.width * 0.5, Window.height * 0.8)
        # Position the carousel in the center
        self.ids.image_carousel4.pos = (Window.width * 0.74 - self.ids.image_carousel4.width / 2,
                                        Window.height * 0.45 - self.ids.image_carousel4.height / 2)
    
    def on_enter(self):
        start_button = self.ids['start_button']


class PreSession(Screen):
    def on_enter(self):
       
        start_button = self.ids['start_button']
        start_button.disabled = True
        
    def enable_start_button(self, active):
        global pre_session_check
        pre_session_check = True
        self.ids.start_button.disabled = not active


class PostSession(Screen):
    def on_enter(self):
        global pose_difficulty
        print("Pose difficulty:", pose_difficulty)

        # Assign a value to postsessionmessage based on pose_difficulty
        if pose_difficulty == "beginner15":
            self.ids.postsessionmessage.text = "Congratulations on completing the 15 minute Beginner Session!"
        elif pose_difficulty == "beginner30":
            self.ids.postsessionmessage.text = "Congratulations on completing the 30 minute Beginner Session!"
        elif pose_difficulty == "normal15":
            self.ids.postsessionmessage.text = "Congratulations on completing the 15 minute Normal Session!"
        elif pose_difficulty == "normal30":
            self.ids.postsessionmessage.text = "Congratulations on completing the 30 minute Normal Session!"
        else:
            pose_difficulty = "beginner15"  # Assign a default value
            self.ids.postsessionmessage.text = "Congratulations on completing the 15 minute Beginner Session!"

        print("Post session message:", self.ids.postsessionmessage.text) 


class CustomImageCarousel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.adjust_self)
        Window.bind(size=self.adjust_to_window)

    def adjust_self(self, *args):
        # Adjustments that depend on the widget's own size
        pass

    def adjust_to_window(self, instance, value):
        # Adjust size of the carousel
        self.ids.image_carousel.size = (Window.width * 0.8, Window.height * 0.8)
        # Position the carousel in the center
        self.ids.image_carousel.pos = (Window.width / 2 - self.ids.image_carousel.width / 2,
                                        Window.height / 2 - self.ids.image_carousel.height / 2)

class CustomImageCarousel2(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.adjust_self)
        Window.bind(size=self.adjust_to_window)

    def adjust_self(self, *args):
        # Adjustments that depend on the widget's own size
        pass

    def adjust_to_window(self, instance, value):
        # Adjust size of the carousel
        self.ids.image_carousel2.size = (Window.width * 0.5, Window.height * 0.8)
        # Position the carousel in the center
        self.ids.image_carousel2.pos = (Window.width * 0.74 - self.ids.image_carousel2.width / 2,
                                        Window.height * 0.45 - self.ids.image_carousel2.height / 2)
        
class CustomImageCarousel3(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.adjust_self)
        Window.bind(size=self.adjust_to_window)

    def adjust_self(self, *args):
        # Adjustments that depend on the widget's own size
        pass
    
        
    def adjust_to_window(self, instance, value):
        # Adjust size of the carousel
        self.ids.image_carousel3.size = (Window.width * 0.8, Window.height * 0.8)
        # Position the carousel in the center
        self.ids.image_carousel3.pos = (Window.width / 2 - self.ids.image_carousel3.width / 2,
                                        Window.height / 2 - self.ids.image_carousel3.height / 2)
        
class CustomImageCarousel4(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.adjust_self)
        Window.bind(size=self.adjust_to_window)

    def adjust_self(self, *args):
        # Adjustments that depend on the widget's own size
        pass
    
        
    def adjust_to_window(self, instance, value):
        # Adjust size of the carousel
        self.ids.image_carousel4.size = (Window.width * 0.8, Window.height * 0.8)
        # Position the carousel in the center
        self.ids.image_carousel4.pos = (Window.width / 2 - self.ids.image_carousel4.width / 2,
                                        Window.height / 2 - self.ids.image_carousel4.height / 2)

class CustomWidget(Widget):
    pass

class CameraSelection(Screen):
    cam_index = 0
    cam_list = {}
    app = None
    
    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        
        if len(self.cam_list) == 0:
            file = open('camera_list.txt', 'r')
            line = file.readline()
            index = 0
            while line:
                    line = line.rstrip()  # strip trailing spaces and newline
                    cam_id, cam_name = line.split("//", 1)
                    self.cam_list[cam_id.rstrip()] = cam_name.lstrip()
                    index += 1
                    line = file.readline()
            file.close()

        print(self.cam_list)
        
        # Set default camera
        self.app.CAMERA_ID = list(self.cam_list.keys())[0]
        self.ids.selected_camera.text = f"Current Camera: {self.cam_list[self.app.CAMERA_ID]}"
        
        cam_dict = [
            {
                "text": f"{self.cam_list[cam]}",
                "leading_icon": "webcam",
                "on_release": lambda x = cam: self.menu_callback(x)
            } for cam in self.cam_list
        ]
        
        self.menu = MDDropdownMenu(
            caller=self.ids.select_camera_button, 
            items=cam_dict
        )
        self.menu.bind(on_release=self.menu_callback)
    
    def menu_callback(self, selection):
        print(f"set to {self.cam_list[selection]}")
        self.cam_index = selection
        self.ids.selected_camera.text = f"Selected Camera: {self.cam_list[self.cam_index]}"
        self.menu.dismiss()
    
    def apply_selection(self):
        self.app.CAMERA_ID = self.cam_index
        self.ids.selected_camera.text = f"Current Camera: {self.cam_list[self.cam_index]}"
        print(f"Applied {self.cam_index}, {self.cam_list[self.cam_index]}")

class YogaApp(MDApp):
    CAMERA_ID = 0
    
    def get_hex_color(self, hex_value):
        return get_color_from_hex(hex_value)
    
    def get_current_date(self):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Current Date: {current_date}")
        return current_date
    
    def build(self):
        self.icon = 'ico/yoga.ico'
        self.sound = SoundLoader.load('background_music.mp3')
        self.sound.loop = True
        self.sound.play()  # Automatically start playing music
        self.volume = 1.0
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main-menu'))
        sm.add_widget(SessionLibrary(name='session-library'))
        sm.add_widget(Session(name='session'))
        sm.add_widget(CameraSelection(name='camera-selection'))
        sm.add_widget(PoseLibrary(name='pose-library'))
        sm.add_widget(History(name='history'))
        sm.add_widget(Setting(name='settings'))
        sm.add_widget(About(name='about'))
        sm.add_widget(Instruction(name='instructions'))
        sm.add_widget(InstructionAdv(name='instructions-adv'))
        sm.add_widget(PreSession(name='pre-session'))
        sm.add_widget(PostSession(name='post-session'))
        sm.current = 'main-menu'
        
        return sm
    
    def play_stop_music(self):
        if self.sound.state == 'play':
            self.sound.stop()
        else:
            self.sound.play()

    def set_volume(self, volume):
        self.volume = volume
        if self.sound:
            self.sound.volume = volume
   
    
    
        
        
if __name__ == '__main__':

    YogaApp().run()
        