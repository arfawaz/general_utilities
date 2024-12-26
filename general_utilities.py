import math


# Function to calculate the dimensions of output of each layer of CNN.
# Gives the dimension of input to first MLP layer also.
# Parameters: No parameters passed to fucntion while fucntion call. The values are prompted to be entered.
def cnn_builder():
    def parse_input(prompt, default=None, is_tuple=False, is_str=False):
        """
        Parses user input, allowing tuples or single integers.
        """
        value = input(prompt)
        if value.lower() == "default":
            return default
        try:
            # Allow tuple input
            if is_tuple:
                return tuple(map(int, value.strip("()").split(",")))
            elif is_str:
                return value.strip().lower()
            else:
                return int(value)
        except ValueError:
            raise ValueError(f"Invalid input. Expected {'a tuple or an integer' if is_tuple else 'an integer'}.")

    def calculate_output_size(input_size, kernel_size, stride, padding, dilation):
        """
        Calculate the output size for a convolutional layer.
        """
        return math.floor((input_size + 2 * padding - dilation * (kernel_size - 1) - 1) / stride + 1)

    # Step 1: Prompt the user for the number of layers
    num_layers = parse_input("Enter the number of CNN layers: ")

    # Initial input size
    batch_size = parse_input("Enter the batch size: ")
    channels = parse_input("Enter the number of channels (e.g., 3 for RGB): ")
    height = parse_input("Enter the input height: ")
    width = parse_input("Enter the input width: ")

    input_size = (batch_size, channels, height, width)

    print(f"\nInitial input size: {input_size}")

    for layer in range(num_layers):
        print(f"\n--- Layer {layer + 1} ---")

        # Prompt for parameters or use default values
        out_channels = parse_input("Enter number of output channels: ")
        kernel_size = parse_input("Enter kernel size (default=3): ", default=3, is_tuple=True)
        stride = parse_input("Enter stride (default=1): ", default=1, is_tuple=True)
        
        # Accept string inputs like 'same' or 'valid' for padding
        padding = parse_input("Enter padding (default=0, options: 'same', 'valid'): ", default=0, is_tuple=True, is_str=True)
        
        dilation = parse_input("Enter dilation (default=1): ", default=1, is_tuple=True)

        # Handle 'same' and 'valid' padding
        if isinstance(padding, str):
            if padding == "same":
                padding = (kernel_size[0] // 2, kernel_size[1] // 2)  # For 'same' padding, half kernel size for padding
            elif padding == "valid":
                padding = (0, 0)  # For 'valid' padding, no padding
            else:
                raise ValueError(f"Invalid padding option: {padding}. Choose 'same', 'valid', or an integer.")

        # Ensure tuples for kernel_size, stride, padding, and dilation
        if isinstance(kernel_size, int):
            kernel_size = (kernel_size, kernel_size)
        if isinstance(stride, int):
            stride = (stride, stride)
        if isinstance(padding, int):
            padding = (padding, padding)
        if isinstance(dilation, int):
            dilation = (dilation, dilation)

        # Update channel and spatial dimensions
        channels = out_channels
        height = calculate_output_size(height, kernel_size[0], stride[0], padding[0], dilation[0])
        width = calculate_output_size(width, kernel_size[1], stride[1], padding[1], dilation[1])

        # Check if the calculated dimensions are valid
        if height <= 0 or width <= 0:
            raise ValueError(f"Invalid configuration for layer {layer + 1}: Output dimensions are not positive.")

        # Print layer output size
        print(f"Output size after layer {layer + 1}: (batch_size={batch_size}, channels={channels}, height={height}, width={width})")

    # Calculate the input size for the MLP layer
    mlp_input_size = channels * height * width
    print(f"\nInput size for the MLP layer: {mlp_input_size}")

