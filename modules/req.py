import subprocess

def install_requirements():
    requirements = [        
        'requests',
        'json',
        'random',
        'time',
        'mnemonic',
        'colorama',
        'cryptocompare',
        'web3',
        'pushbullet.py',
        'watchdog',
        'eth-account',
        'uuid',
    ]

    for requirement in requirements:
        subprocess.run(['pip', 'install', requirement])

    print("Requirements installed successfully. Type ./run to run Script ")

if __name__ == "__main__":
    install_requirements()