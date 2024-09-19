from PIL import Image, ImageFilter

# Load an image from file
bg_path = 'assets/Images/background.png'
image = Image.open(bg_path)

# Apply Gaussian blur with a specified radius
radius = 20  # You can change the radius to increase/decrease the blur effect
blurred_image = image.filter(ImageFilter.GaussianBlur(radius))

# Save the blurred image to a temporary file
blurred_image_path = 'assets/Images/blurred_background.png'
blurred_image.save(blurred_image_path)
