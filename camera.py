import cv2
import mediapipe as mp
import time
import mouse
import pyautogui  # For getting screen size

# Get screen size for scaling
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

cap = cv2.VideoCapture(0)
# Get camera resolution
CAM_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
CAM_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

mode = 0
prev_x, prev_y = 0, 0
smoothing = 0.5  # Smoothing factor for mouse movement (0-1)

def count_fingers(hand_landmarks):
    tip_ids = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky
    fingers = []
    
    if hand_landmarks:
        # Thumb
        if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Other fingers
        for id in range(1, 5):
            if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
    
    return fingers

def move_mouse(index_finger_x, index_finger_y, smooth=True):
    global prev_x, prev_y
    
    # Convert camera coordinates to screen coordinates
    screen_x = int(SCREEN_WIDTH * (1 - index_finger_x))  # Flip X for more intuitive control
    screen_y = int(SCREEN_HEIGHT * index_finger_y)
    
    if smooth:
        # Apply smoothing
        screen_x = int(prev_x + (screen_x - prev_x) * smoothing)
        screen_y = int(prev_y + (screen_y - prev_y) * smoothing)
    
    # Update previous positions
    prev_x, prev_y = screen_x, screen_y
    
    # Move mouse
    mouse.move(screen_x, screen_y)

print("Hand tracking started. Use your hand to control the mouse:")
print("- Move index finger to control cursor")
print("- Raise thumb to left click")
print("- Raise middle finger with index for right click")
print("- Raise all fingers to drag")
print("Press Ctrl+C to exit")

try:
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to get frame from camera")
            break
            
        # Convert to RGB and process
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        # Process hands
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get index finger tip position
                index_finger = hand_landmarks.landmark[8]  # Index finger tip
                
                # Move mouse based on index finger position
                move_mouse(index_finger.x, index_finger.y)
                
                # Get finger states
                fingers = count_fingers(hand_landmarks)
                
                # Mouse actions based on finger combinations
                if fingers[0] == 1:  # Thumb up
                    if not mouse.is_pressed('left'):
                        mouse.press('left')
                else:
                    if mouse.is_pressed('left'):
                        mouse.release('left')
                
                if fingers[1] == 1 and fingers[2] == 1:  # Index and middle up
                    if not mouse.is_pressed('right'):
                        mouse.press('right')
                else:
                    if mouse.is_pressed('right'):
                        mouse.release('right')
                
                # All fingers up for drag mode
                if sum(fingers) == 5:
                    if not mouse.is_pressed('left'):
                        mouse.press('left')
                elif sum(fingers) < 5 and not fingers[0]:  # Release if not all fingers and thumb not up
                    if mouse.is_pressed('left'):
                        mouse.release('left')
        
        time.sleep(0.05)  # Small delay to reduce CPU usage

except KeyboardInterrupt:
    print("\nExiting program...")
finally:
    # Make sure to release any pressed mouse buttons
    if mouse.is_pressed('left'):
        mouse.release('left')
    if mouse.is_pressed('right'):
        mouse.release('right')
    cap.release()
    cv2.destroyAllWindows()
