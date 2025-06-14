import cv2
import numpy as np

write_to_vid = False

# Define ASCII characters in order of intensity
ASCII_CHARS = "@%#*+=-:. "
ASCII_CHARS = ASCII_CHARS[::-1]


def resize_image(image, new_width=100):
    """Resize image while maintaining aspect ratio."""
    height, width = image.shape[:2]
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # Adjust for character aspect ratio
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image


def gray_to_ascii_canvas(gray_image, canvas_size, font_scale=1, color=(255, 255, 255)):
    """Convert grayscale image to ASCII and render on an OpenCV canvas."""
    canvas = np.zeros((canvas_size[1], canvas_size[0], 3), dtype=np.uint8)

    h, w = gray_image.shape
    step_x = canvas_size[0] // w
    step_y = canvas_size[1] // h

    for i in range(h):
        for j in range(w):
            intensity = gray_image[i, j]
            char = ASCII_CHARS[(intensity // (256 // len(ASCII_CHARS)) - 1)]
            org = (j * step_x, (i + 1) * step_y)  # Bottom-left corner for text
            cv2.putText(canvas, char, org, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 1)
    return canvas


def process_image_to_ascii(image, canvas_size=(640, 480), new_width=100):
    """Convert image to ASCII art and return as OpenCV object."""
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = resize_image(gray_image, new_width)
    ascii_canvas = gray_to_ascii_canvas(resized_image, canvas_size)
    return ascii_canvas


# Example with webcam
cap = cv2.VideoCapture(0)

images = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to ASCII art
    ascii_frame = process_image_to_ascii(frame, canvas_size=(640, 480), new_width=100)
    images.append(ascii_frame)

    # Display the ASCII art
    cv2.imshow("ASCII Art", ascii_frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

if write_to_vid:
    print("Writing to video")
    #    video = cv2.VideoWriter('ascii.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))
    #    video.fourcc(*'H264')
    video = cv2.VideoWriter("ascii.avi", cv2.VideoWriter_fourcc(*"XVID"), 30, (640, 480))
    for image in images:
        video.write(image)

cap.release()
cv2.destroyAllWindows()
