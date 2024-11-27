def message_to_bin(message):
    """Converts a message to a binary string."""
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    return binary_message

def bin_to_message(binary_message):
    """Converts a binary string back to the original message."""
    chars = [chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)]
    return ''.join(chars)

def hide_message_in_image(image_path, message, output_image_path):
    """Hides the message in the image and saves the new image."""
    # Open the image file in binary mode
    with open(image_path, 'rb') as image_file:
        image_data = bytearray(image_file.read())

    # Convert message to binary
    binary_message = message_to_bin(message) + '1111111111111110'  # Add a delimiter (end of message marker)
    
    # Check if the image has enough space for the message
    if len(binary_message) > len(image_data) * 8:
        raise ValueError("Message is too large to fit in the image")

    # Modify the LSB of the image data to hide the message
    data_index = 0
    for bit in binary_message:
        # Get the byte value of the image data at the current index
        byte_value = image_data[data_index]
        
        # Set the LSB to the current bit
        image_data[data_index] = (byte_value & 0xFE) | int(bit)
        
        # Move to the next byte in the image data
        data_index += 1

    # Write the modified image data to a new file
    with open(output_image_path, 'wb') as output_file:
        output_file.write(image_data)

    print(f"Message hidden in image and saved to {output_image_path}.")

def extract_message_from_image(image_path):
    """Extracts the hidden message from an image."""
    with open(image_path, 'rb') as image_file:
        image_data = bytearray(image_file.read())

    # Extract the LSBs to recover the hidden message
    binary_message = ''
    for byte_value in image_data:
        binary_message += str(byte_value & 1)

    # Find the delimiter (end of message marker) and stop extracting at that point
    end_marker = '1111111111111110'
    message_end = binary_message.find(end_marker)
    if message_end == -1:
        raise ValueError("No hidden message found in the image")

    # Convert the binary message to the original message
    binary_message = binary_message[:message_end]
    original_message = bin_to_message(binary_message)

    return original_message

# Example usage:
if __name__ == "__main__":
    # User input for secret message
    secret_message = input("Enter the secret message: ")

    # Path of the input image (use the provided image path)
    input_image_path = r"/Users/janafayed/Downloads/input image .bmp"  # Replace with your image path
    
    output_image_path = r"/Users/janafayed/Downloads/output image .bmp"  # Path where the output image will be saved

    try:
        # Hide the message in the image
        hide_message_in_image(input_image_path, secret_message, output_image_path)
        
        # Extract the hidden message from the modified image
        extracted_message = extract_message_from_image(output_image_path)
        print(f"Extracted Message: {extracted_message}")
    
    except ValueError as e:
        print(f"Error: {e}")
