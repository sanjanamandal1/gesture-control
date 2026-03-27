from setuptools import setup, find_packages

setup(
    name="gesture-control",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "mediapipe==0.10.13",
        "opencv-python",
        "pyautogui",
        "numpy",
        "scikit-learn",
        "pygetwindow",
        "pycaw",
        "comtypes",
        "imageio",
    ],
    python_requires=">=3.9",
)