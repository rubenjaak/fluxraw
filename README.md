# ComfyUI Flux 1.1 Ultra & Raw Node

A ComfyUI custom node for Black Forest Labs' FLUX 1.1 [pro] API, supporting both regular and Ultra modes with optional Raw mode.

![image](https://github.com/user-attachments/assets/8b7f871e-8e2d-4317-8525-c2edde12515e)

## Features

- Support for FLUX 1.1 [pro] regular and Ultra modes
- Optional Raw mode for more natural-looking images
- Multiple aspect ratios support
- Configurable safety tolerance
- Support for both JPEG and PNG output formats
- Seed support for reproducible results

## Installation

1. Navigate to your ComfyUI custom nodes directory:
```bash
cd path/to/ComfyUI/custom_nodes/
```

2. Clone this repository:
```bash
git clone https://github.com/your-username/ComfyUI_Flux_1.1_RAW_API
```

## API Key Setup

1. Get your API key:
   - Visit [Black Forest Labs Login](https://api.bfl.ml/auth/login?message=Login+Failed.#)
   - Sign in or create an account
   - Navigate to your profile settings
   - Copy your API key

2. Open the file `config.ini` with text editor (inside the custom node folder)
   - Add your API key instead of: your_api_key_here:
```ini
[API]
X_KEY=your_api_key_here
BASE_URL=https://api.bfl.ml
```

**Important Notes:**
- Keep your API key secret and never share it
- Make sure there are no extra spaces around your API key
- The `config.ini` file should be in the same directory as the node's Python files
- If you update your API key, you'll need to restart ComfyUI

Example of a correctly formatted `config.ini`:
```ini
[API]
X_KEY=bfl_1234567890abcdef1234567890abcdef
BASE_URL=https://api.bfl.ml
```

3. Restart ComfyUI

## Usage

### Node Parameters

- **prompt**: Text prompt describing the desired image
- **ultra_mode**: Enable Ultra mode for higher resolution output
- **aspect_ratio**: Choose from multiple aspect ratios:
  - 21:9 (Ultrawide)
  - 16:9 (Widescreen)
  - 4:3 (Standard)
  - 1:1 (Square)
  - 3:4 (Portrait)
  - 9:16 (Vertical)
  - 9:21 (Tall)
- **safety_tolerance**: 0-6 (0 being most strict, 6 being least strict)
- **output_format**: Choose between JPEG and PNG
- **raw**: Enable Raw mode for less processed, more natural-looking images
- **seed**: Optional seed for reproducible results (-1 for random)

### Mode Differences

#### Regular Mode
- Resolution based on aspect ratio (up to 1440px)
- Standard image processing

#### Ultra Mode
- Higher resolution output (up to 4MP)
- Support for Raw mode
- Advanced image processing

## Requirements

- ComfyUI
- Black Forest Labs API key
- Python packages:
  - requests
  - Pillow
  - numpy
  - torch

## API Reference

This node uses the Black Forest Labs FLUX 1.1 [pro] API. For more information, visit:
- [Black Forest Labs](https://blackforestlabs.ai/)
- [FLUX 1.1 Ultra Documentation](https://fal.ai/models/fal-ai/flux-pro/v1.1-ultra)

## Troubleshooting

Common issues:
1. "Error: X_KEY not found in section API of config file"
   - Check if your `config.ini` file exists and is properly formatted
   - Verify the API key is correctly copied without extra spaces
   - Make sure the file is in the correct directory

2. "404 Not Found" error
   - Verify your API key is valid and active
   - Check if you have access to the FLUX 1.1 API
   - Make sure your account is in good standing

## Credits

- Black Forest Labs for the FLUX API
- ComfyUI team for the base framework

## Support

For issues and feature requests, please use the [GitHub issues page](https://github.com/your-username/ComfyUI_Flux_1.1_RAW_API/issues).

