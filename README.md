# Cryptor
An application for encrypting and decrypting files and text with Graphical User Interface (GUI) <br> <br>
Features are available for three (3) different languages: <br>
- English
- Finnish
- Swedish

User may opt using default encryption paramaters for faster usage and convenience. <br> <br>
Dark mode is available is high contrast if not your prefered style for an application. <br> <br>

## Currently supported algorithms for encryption:
- AES
- RSA
- ChaCha20-Poly1305

## Currently supported algorithms for hashing:
- SHA-256
- SHA-512
- SHA3-512
- MD5

## Linux & bash setup

We recommend using Python virtual environment, to not mess up any global configurations. <br>
This can be set up with command:
```
python3 -m venv example/path/to/venv
```

And activating the newly created virtual environment with command:
```
source /path/to/venv/bin/activate
```

Install the required pip packages with command:
```
pip install -r requirements.txt
```
Navigate to the cryptor/ folder and activate the app:
```
python3 cryptor.py
```

## Windows setup
#TODO
