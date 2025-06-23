from PIL import Image

# Convert message to binary
def text_to_bin(message):
    return ''.join(format(ord(char), '08b') for char in message)

# Convert binary to text
def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

# Embed text into image with a delimiter
def embed_message(image_path, message, output_path):
    image = Image.open(image_path)
    binary_message = text_to_bin(message + "#####")  # Use '#####' as end marker
    data_index = 0

    if image.mode != 'RGB':
        image = image.convert('RGB')
    pixels = list(image.getdata())
    new_pixels = []

    for pixel in pixels:
        r, g, b = pixel
        if data_index < len(binary_message):
            r = (r & ~1) | int(binary_message[data_index])
            data_index += 1
        if data_index < len(binary_message):
            g = (g & ~1) | int(binary_message[data_index])
            data_index += 1
        if data_index < len(binary_message):
            b = (b & ~1) | int(binary_message[data_index])
            data_index += 1
        new_pixels.append((r, g, b))

    image.putdata(new_pixels)
    image.save(output_path)
    print("✅ Message embedded successfully!")

# Extract the hidden message
def extract_message(image_path):
    image = Image.open(image_path)
    binary_data = ""
    pixels = list(image.getdata())

    for pixel in pixels:
        for color in pixel[:3]:
            binary_data += str(color & 1)

    decoded_text = bin_to_text(binary_data)
    hidden_message = decoded_text.split("#####")[0]  # Stop at delimiter
    print("🕵️ Extracted message:", hidden_message)

# Run test
embed_message("input.png", "This is a secret message!", "output.png")
extract_message("output.png")
