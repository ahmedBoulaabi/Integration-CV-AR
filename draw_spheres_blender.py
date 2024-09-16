import bpy

# Fetch the 'thlow' object
thlow = bpy.data.objects.get('thlow')
if not thlow:
    raise ValueError("Object 'thlow' not found in the scene.")

# Get the dimensions and location of 'thlow'
thlow_dimensions = thlow.dimensions
thlow_location = thlow.location

# Read the infection data from the text file
input_file_path = 'infection_data.txt'
infection_data = []
with open(input_file_path, 'r') as file:
    for line in file:
        cX_percent, cY_percent, size_percent = map(float, line.strip().split(','))
        infection_data.append({"center_percent": (cX_percent, cY_percent), "size_percent": size_percent})

def create_sphere(location, size):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=size, location=location)


# Loop through and create spheres
for infection in infection_data:
    x_percent, y_percent = infection["center_percent"]
    size_percent = infection["size_percent"]

    # Translate percentages to 3D coordinates within 'thlow'
    x_coord = thlow_location.x + ((x_percent / 100) * thlow_dimensions.x) - (thlow_dimensions.x / 2)
    y_coord = thlow_location.y + 0.8 # Y-coordinate remains constant

    # Invert the percentage for Z-axis
    z_coord = thlow_location.z + ((100 - y_percent) / 100) * thlow_dimensions.z - (thlow_dimensions.z / 2) + 0.8

    # Translate size percentage to actual size
    size = (size_percent / 100) * max(thlow_dimensions.x, thlow_dimensions.y, thlow_dimensions.z)

    # Create sphere
    create_sphere((x_coord, y_coord, z_coord), size)


