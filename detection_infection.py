import cv2
import numpy as np

# Load the image from the file system
image_path = 'res_cam.png'
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    raise ValueError(f"The image at path {image_path} could not be loaded.")

# Get image dimensions
image_height, image_width = image.shape[:2]


# Convert the image to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Define the range of red color in RGB
lower_red = np.array([100, 0, 0])
upper_red = np.array([255, 100, 100])

# Create a mask to detect red areas
mask = cv2.inRange(image_rgb, lower_red, upper_red)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# List to hold the center points and sizes of the red regions as percentages
infection_locations_percentage = []

# Create a copy of the original image to draw on
image_with_infections = image.copy()

# Iterate over the contours to find the bounding box and center
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 100:  # Filter out too small areas
        M = cv2.moments(contour)
        # Calculate x, y coordinate of center
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        # Calculate the size of the area (radius of the equivalent circle)
        size = np.sqrt(area / np.pi)

        # Convert center coordinates and size to percentages
        cX_percent = (cX / image_width) * 100
        cY_percent = (cY / image_height) * 100
        size_percent = (size / max(image_width, image_height)) * 100

        # Store the center and size of the contour as percentages
        infection_locations_percentage.append((cX_percent, cY_percent, size_percent))

        # Draw circle on the image copy
        cv2.circle(image_with_infections, (cX, cY), int(size), (0, 255, 0), 2)

# Save the result image
output_path = 'infection_detected_image.png'
cv2.imwrite(output_path, image_with_infections)

# Print out the infection location details as percentages
print("Infection Locations (Center Coordinates and Size as Percentages):")
for idx, (cX_percent, cY_percent, size_percent) in enumerate(infection_locations_percentage):
    print(f"Infection {idx + 1}: Center=({cX_percent:.2f}%, {cY_percent:.2f}%), Size={size_percent:.2f}%")

    # Write the infection data to a text file
output_file_path = 'infection_data.txt'
with open(output_file_path, 'w') as file:
    for cX_percent, cY_percent, size_percent in infection_locations_percentage:
        file.write(f"{cX_percent},{cY_percent},{size_percent}\n")

