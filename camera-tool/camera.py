import sys
print(f"Python interpreter: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

import cv2
try:
    import mediapipe as mp
    print(f"MediaPipe version: {mp.__version__}")
except ImportError:
    print("Error: mediapipe package not found. Please install it using:")
    print("pip install mediapipe==0.10.8")
    exit(1)

import time
import mouse
import pyautogui

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera. Please make sure your camera is connected and not in use by another application.")
        exit(1)
        
    CAM_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    CAM_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
except Exception as e:
    print(f"Error initializing camera: {str(e)}")
    exit(1)

try:
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
except Exception as e:
    print(f"Error initializing MediaPipe: {str(e)}")
    cap.release()
    exit(1)

mode = 0
prev_x, prev_y = 0, 0
smoothing = 0.5

def count_fingers(hand_landmarks):
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []
    
    if hand_landmarks:
        if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        for id in range(1, 5):
            if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
    
    return fingers

def move_mouse(index_finger_x, index_finger_y, smooth=True):
    global prev_x, prev_y
    
    screen_x = int(SCREEN_WIDTH * (1 - index_finger_x))
    screen_y = int(SCREEN_HEIGHT * index_finger_y)
    
    if smooth:
        screen_x = int(prev_x + (screen_x - prev_x) * smoothing)
        screen_y = int(prev_y + (screen_y - prev_y) * smoothing)
    
    prev_x, prev_y = screen_x, screen_y
    
    mouse.move(screen_x, screen_y)

def handle_click_hand(fingers):
    if fingers[0] == 1:
        if not mouse.is_pressed('left'):
            mouse.press('left')
    else:
        if mouse.is_pressed('left'):
            mouse.release('left')
    
    if fingers[1] == 1 and fingers[2] == 1:
        if not mouse.is_pressed('right'):
            mouse.press('right')
    else:
        if mouse.is_pressed('right'):
            mouse.release('right')
    
    if sum(fingers) == 5:
        if not mouse.is_pressed('left'):
            mouse.press('left')
    elif sum(fingers) < 5 and not fingers[0]:
        if mouse.is_pressed('left'):
            mouse.release('left')

print("Hand tracking started. Use your hands to control:")
print("Right hand:")
print("- Move index finger to control cursor")
print("Left hand:")
print("- Raise thumb to left click")
print("- Raise index and middle fingers for right click")
print("- Raise all fingers to drag")
print("Press Ctrl+C to exit")

try:
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to get frame from camera")
            break
            
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand_type = results.multi_handedness[idx].classification[0].label
                index_finger = hand_landmarks.landmark[8]
                fingers = count_fingers(hand_landmarks)
                
                if hand_type == "Right":
                    move_mouse(index_finger.x, index_finger.y)
                else:
                    handle_click_hand(fingers)
        
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nExiting program...")
finally:
    if mouse.is_pressed('left'):
        mouse.release('left')
    if mouse.is_pressed('right'):
        mouse.release('right')
    cap.release()
    cv2.destroyAllWindows()
