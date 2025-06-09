import cv2
import numpy as np
import math

def create_base_pattern(size=200):
    pattern = np.zeros((size, size, 3), dtype=np.uint8)
    points = np.array([[size // 2, 0], [size, size // 2], [size // 2, size], [0, size // 2]])
#    cv2.fillPoly(pattern, [points], (0, 255, 0))  # Green diamond
    cv2.circle(pattern, (size//2, size // 2), size // 3, (255,0,0), -1)
    return pattern

def animate_pattern(base, rows, cols, frame_num, speed=5):
    h, w, _ = base.shape
    canvas = np.zeros((rows * h, cols * w, 3), dtype=np.uint8)
    
    for i in range(rows):
        for j in range(cols):
            # Calculate movement
            x_offset = int(speed * math.sin((frame_num + i * 10) * 0.1))
            y_offset = int(speed * math.cos((frame_num + j * 10) * 0.1))
            
            # Calculate start and end positions
            y_start = i * h + y_offset
            x_start = j * w + x_offset
            y_end = y_start + h
            x_end = x_start + w

            # Clip values to ensure they stay within canvas bounds
            if y_start < 0:
                y_start = 0
                y_end = h
            if x_start < 0:
                x_start = 0
                x_end = w
            if y_end > canvas.shape[0]:
                y_end = canvas.shape[0]
                y_start = y_end - h
            if x_end > canvas.shape[1]:
                x_end = canvas.shape[1]
                x_start = x_end - w
            
            # Ensure valid dimensions for pasting
            if y_start >= 0 and x_start >= 0 and y_end <= canvas.shape[0] and x_end <= canvas.shape[1]:
                canvas[y_start:y_end, x_start:x_end] = base[:y_end-y_start, :x_end-x_start]

    return canvas

# Initialize the base pattern
base_pattern = create_base_pattern(100)

# Animation parameters
rows, cols = 6, 6
num_frames = 200

# OpenCV video writer to save animation (optional)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('escher_animation_fixed.avi', fourcc, 30.0, (600, 600))

# Animate
for frame_num in range(num_frames):
    animated_frame = animate_pattern(base_pattern, rows, cols, frame_num, speed=10)
    
    # Display the animation
    cv2.imshow('Escher Animation', animated_frame)
    
    # Write frame to video file
    out.write(animated_frame)
    
    # Break on pressing 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

out.release()
cv2.destroyAllWindows()

