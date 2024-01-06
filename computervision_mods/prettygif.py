from PIL import Image
import os

def convert_to_gif(input_folder, output_file, file_extension='.jpg', duration=100, loop=0):
    images = []

    for i in range(18,150):
        file_name = 'af2b479e-ec78-46b0-be35-6bbbd1691460-' + str(i) + '.jpg'
        file_path = os.path.join(input_folder, file_name)
        img = Image.open(file_path)
        images.append(img)


    images[0].save(
        output_file,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=loop
    )

# Example usage
input_folder = ' '
output_file = '  '

convert_to_gif(input_folder, output_file)
