import subprocess

def install_requirements():
    requirements = [
        'pushbullet.py',
        'requests',
        'json',
        'random',
        'time',
        'mnemonic',
        'colorama',
        'cryptocompare',
        'web3',
        'watchdog',
        'eth-account',
        'uuid',
    ]

    for requirement in requirements:
        subprocess.run(['pip', 'install', requirement])

    print("Requirements installed successfully. Type ./run.sh to run Script ")

if __name__ == "__main__":
    install_requirements()