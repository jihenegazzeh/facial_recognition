import cv2
import os

def capture_image(save_dir):
    # Open default camera
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Read a frame from the camera
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    if ret:
        # Ask user to enter image name
        image_name = input("Enter the name of the employee: ")

        # Ensure the save directory exists
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Check if the file already exists
        image_path = os.path.join(save_dir, image_name + ".jpg")
        if os.path.exists(image_path):
            print("Error: Name already present.")
        else:
            # Save the image
            cv2.imwrite(image_path, frame)
            print("Image saved successfully at", image_path)
    else:
        print("Error: Failed to capture image.")

if __name__ == "__main__":
    save_directory = r"C:\IT_TEST\source code\images"
    capture_image(save_directory)
