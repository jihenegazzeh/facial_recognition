import os

def delete_image(save_dir, image_name):
    # Construct the path to the image
    image_path = os.path.join(save_dir, image_name + ".jpg")

    # Check if the file exists
    if os.path.exists(image_path):
        # Delete the image file
        os.remove(image_path)
        print("Image for", image_name, "deleted successfully.")
    else:
        print("Error: Image for", image_name, "doesn't exist. Please verify the name of the employee.")

if __name__ == "__main__":
    save_directory = r"C:\IT_TEST\source code\images"
    employee_name = input("Enter the name of the employee to delete their image: ")
    delete_image(save_directory, employee_name)
