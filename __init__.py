import requests
from PIL import Image
import io
import numpy as np
import torch
import os
import configparser
import time
from enum import Enum
from urllib.parse import urljoin

class Status(Enum):
    PENDING = "Pending"
    READY = "Ready"
    ERROR = "Error"

class ConfigLoader:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "config.ini")
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.set_x_key()

    def get_key(self, section, key):
        try:
            return self.config[section][key]
        except KeyError:
            raise KeyError(f"{key} not found in section {section} of config file.")

    def create_url(self, path):
        try:
            base_url = self.get_key('API', 'BASE_URL')
            return urljoin(base_url, path)
        except KeyError as e:
            raise KeyError(f"Error constructing URL: {str(e)}")

    def set_x_key(self):
        try:
            x_key = self.get_key('API', 'X_KEY')
            os.environ["X_KEY"] = x_key
        except KeyError as e:
            print(f"Error: {str(e)}")

class FluxPro11:
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "BFL"

    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "config.ini")
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.set_x_key()

    def set_x_key(self):
        try:
            os.environ["X_KEY"] = self.config['API']['X_KEY']
        except KeyError as e:
            print(f"Error: {str(e)}")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "ultra_mode": ("BOOLEAN", {"default": True}),
                "aspect_ratio": ([
                    "21:9", "16:9", "4:3", "1:1", "3:4", "9:16", "9:21"
                ], {"default": "16:9"}),
                "safety_tolerance": ("INT", {"default": 6, "min": 0, "max": 6}),
                "output_format": (["jpeg", "png"], {"default": "png"}),
                "raw": ("BOOLEAN", {"default": False})
            },
            "optional": {
                "seed": ("INT", {"default": -1})
            }
        }

    def generate_image(self, prompt, ultra_mode, aspect_ratio, 
                      safety_tolerance, output_format, raw, seed=-1):
        
        if ultra_mode:
            arguments = {
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "safety_tolerance": safety_tolerance,
                "output_format": output_format,
                "raw": raw
            }
            if seed != -1:
                arguments["seed"] = seed
                
            url = "https://api.bfl.ml/v1/flux-pro-1.1-ultra"
        else:
            width, height = self.get_dimensions_from_ratio(aspect_ratio)
            arguments = {
                "prompt": prompt,
                "width": width,
                "height": height,
                "safety_tolerance": safety_tolerance,
                "output_format": output_format
            }
            if seed != -1:
                arguments["seed"] = seed
                
            url = "https://api.bfl.ml/v1/flux-pro-1.1"

        try:
            headers = {"x-key": os.environ["X_KEY"]}
            
            # Debug prints
            print(f"Full URL: {url}")
            print(f"Arguments: {arguments}")
            
            response = requests.post(url, json=arguments, headers=headers)
            
            if response.status_code == 200:
                task_id = response.json().get("id")
                if task_id:
                    print(f"Task ID: {task_id}")
                    return self.get_result(task_id, output_format)
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return self.create_blank_image()
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return self.create_blank_image()

    def get_dimensions_from_ratio(self, aspect_ratio):
        regular_dimensions = {
            "1:1":  (1024, 1024),
            "4:3":  (1408, 1024),
            "3:4":  (1024, 1408),
            "3:2":  (1408, 928),
            "2:3":  (928, 1408),
            "16:9": (1408, 800),
            "9:16": (800, 1408),
            "21:9": (1408, 608),
            "9:21": (608, 1408)
        }
        width, height = regular_dimensions.get(aspect_ratio, (1408, 800))
        return width, height

    def create_blank_image(self):
        blank_img = Image.new('RGB', (512, 512), color='black')
        img_array = np.array(blank_img).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_array)[None,]
        return (img_tensor,)

    def get_result(self, task_id, output_format, attempt=1, max_attempts=10):
        if attempt > max_attempts:
            print(f"Max attempts reached for task_id {task_id}")
            return self.create_blank_image()

        get_url = f"https://api.bfl.ml/v1/get_result?id={task_id}"
        headers = {"x-key": os.environ["X_KEY"]}
        
        response = requests.get(get_url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            status = result.get("status")
            
            if status == "Ready":
                sample_url = result['result']['sample']
                img_response = requests.get(sample_url)
                img = Image.open(io.BytesIO(img_response.content))
                
                with io.BytesIO() as output:
                    img.save(output, format=output_format.upper())
                    output.seek(0)
                    img_converted = Image.open(output)
                    img_array = np.array(img_converted).astype(np.float32) / 255.0
                    return (torch.from_numpy(img_array)[None,],)
                    
            elif status == "Pending":
                print(f"Attempt {attempt}: Image not ready. Retrying in 5 seconds...")
                time.sleep(5)
                return self.get_result(task_id, output_format, attempt + 1)
                
        return self.create_blank_image()

NODE_CLASS_MAPPINGS = {
    "FluxPro11": FluxPro11
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxPro11": "Flux Pro 1.1 Ultra & Raw"
}