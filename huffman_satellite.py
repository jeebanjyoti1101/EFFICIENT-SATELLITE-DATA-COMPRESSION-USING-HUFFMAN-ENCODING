import heapq
import collections
import sys
import matplotlib.pyplot as plt

class HuffmanEncoder:
    def __init__(self):
        # Dictionary to store Huffman codes for characters
        self.huffman_dict = {}

    # Main Huffman encoding implementation starts here
    def build_huffman_tree(self, freq):
        """
        Builds Huffman tree using frequency dictionary
        Args:
            freq: Dictionary of character frequencies
        Returns:
            Root node of Huffman tree
        """
        heap = [[weight, [char, ""]] for char, weight in freq.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        return heap[0]

    def encode(self, data):
        """
        Encodes input data using Huffman coding
        Args:
            data: String of comma-separated values
        Returns:
            Compressed binary string
        """
        # Convert input to string and split into parameters
        params = [str(p) for p in data.split(',')]
        # Calculate character frequencies
        freq = collections.Counter(''.join(params))
        # Build Huffman tree
        huffman_tree = self.build_huffman_tree(freq)
        # Create Huffman code dictionary
        self.huffman_dict = {char: code for char, code in huffman_tree[1:]}
        # Return encoded binary string
        return ''.join(self.huffman_dict[char] for char in ''.join(params))

    def calculate_parameter_sizes(self, data):
        """
        Calculates original and compressed sizes for each parameter
        Args:
            data: Input data string
        Returns:
            Dictionary with original and compressed sizes
        """
        params = [str(p) for p in data.split(',')]
        param_names = ['Temperature', 'Pressure', 'Altitude', 'Battery']
        
        # Calculate original sizes (8 bits per character)
        original_sizes = {name: len(param)*8 for name, param in zip(param_names, params)}
        
        # Calculate compressed sizes using Huffman codes
        compressed_sizes = {name: sum(len(self.huffman_dict[c]) for c in param) for name, param in zip(param_names, params)}
        
        return {'original': original_sizes, 'compressed': compressed_sizes}

    def visualize_compression(self, original_size, compressed_size, parameter_sizes, refresh=True):
        """
        Visualizes compression results using matplotlib
        Args:
            original_size: Total original size in bits
            compressed_size: Total compressed size in bits
            parameter_sizes: Dictionary of parameter sizes
            refresh: Whether to clear previous figure
        """
        if refresh:
            plt.clf()  # Clear previous figure
            plt.close('all')  # Close all existing figures
        
        # Create figure with two subplots
        plt.figure(figsize=(12, 6))
        
        # Plot original size breakdown
        plt.subplot(1, 2, 1)
        bottom = 0
        colors = ['red', 'blue', 'green', 'orange']
        parameters = ['Temperature', 'Pressure', 'Altitude', 'Battery']
        
        for i, (param, size) in enumerate(parameter_sizes['original'].items()):
            plt.bar('Original Size', size, bottom=bottom, color=colors[i], label=parameters[i])
            plt.text(0, bottom + size/2, f'{parameters[i]}: {size} bits', ha='center', va='center', color='white', fontsize=8)
            bottom += size
        
        # Plot compressed size breakdown
        plt.subplot(1, 2, 2)
        bottom = 0
        for i, (param, size) in enumerate(parameter_sizes['compressed'].items()):
            plt.bar('Compressed Size', size, bottom=bottom, color=colors[i], label=parameters[i])
            plt.text(0, bottom + size/2, f'{parameters[i]}: {size} bits', ha='center', va='center', color='white', fontsize=8)
            bottom += size
        
        # Add titles and labels
        plt.suptitle('Data Compression Breakdown')
        plt.ylabel('Size (bits)')
        plt.legend(loc='upper right')
        
        # Calculate and display compression metrics
        compression_ratio = original_size / compressed_size if compressed_size > 0 else 0
        savings_percent = ((original_size - compressed_size) / original_size) * 100 if original_size > 0 else 0
        
        plt.text(0.5, 1.1, f'Compression Ratio: {compression_ratio:.2f}x\nSpace Savings: {savings_percent:.2f}%', 
                horizontalalignment='center', verticalalignment='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.7), transform=plt.gcf().transFigure)
        
        plt.tight_layout()
        plt.show()
        plt.close()

if __name__ == "__main__":
    print("Enter satellite data (temperature, pressure, altitude, battery):")
    user_data = input().strip()
    
    encoder = HuffmanEncoder()
    encoded_data = encoder.encode(user_data)
    
    parameter_sizes = encoder.calculate_parameter_sizes(user_data)
    original_size = sum(parameter_sizes['original'].values())
    compressed_size = sum(parameter_sizes['compressed'].values())
    bandwidth = 1000  # bits per second
    
    print(f"\nOriginal Data: {user_data}")
    print(f"Encoded Data: {encoded_data}")
    print(f"\nOriginal Size: {original_size} bits")
    print(f"Compressed Size: {compressed_size} bits")
    print(f"Space Saved: {original_size - compressed_size} bits")
    print(f"Compression Ratio: {original_size / compressed_size:.2f}x")
    print(f"\nTransmission Time (Original): {original_size / bandwidth:.2f} seconds")
    print(f"Transmission Time (Compressed): {compressed_size / bandwidth:.2f} seconds")
    print(f"Time Saved: {(original_size - compressed_size) / bandwidth:.2f} seconds")
    
    encoder.visualize_compression(original_size, compressed_size, parameter_sizes)