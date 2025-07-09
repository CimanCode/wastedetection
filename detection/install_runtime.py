import subprocess
import importlib.util

def install_heavy_libs():
    if importlib.util.find_spec("torch") is None:
        subprocess.run(["pip", "install", "--no-cache-dir", "torch==2.2.2", "torchvision==0.17.2", "opencv-python-headless==4.8.1.78", "ultralytics==8.3.161"])
