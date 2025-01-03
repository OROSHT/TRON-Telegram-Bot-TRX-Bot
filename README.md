# TRON Telegram Bot Installation

This guide includes the steps to install and run your TRON Telegram bot.

## 1. Installing Python

If Python is not installed on your computer, [download Python 3.12.4 from here](https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe). Don't forget to check the "Add Python to PATH" option during the installation.

## 2. Installing Required Modules

Open the command prompt (cmd) and enter the following commands in order:

```bash
pip install aiogram
pip install aiosqlite
pip install httpx
pip install glqiwiapi
pip install tronapi
```

## 3. Creating a TronLink PRO Wallet

In this step, you need to create a TronLink PRO wallet on your mobile device (Android).

1. Download the TronLink PRO app.
2. Register.
3. Click the "Me" button.

4. Go to the "Public Account Management" section.

5. Click "Back Up Private Key" and enter the password you specified earlier.

6. Copy your private key and go to step 4.

## 4. Editing the config.py File

Open the `config.py` file located in the `data` folder and fill in the necessary information.

- If you want to use the Yoomoney payment system, the file includes a description of how to get tokens.
- If you do not specify the `key` parameter in a payment system, that payment system will be removed from the list and will not work.

## 5. Clearing the db.db File

You can optionally delete the `db.db` file. The bot will create a new file.

## 6. Bot Settings with @BotFather

1. Go to @BotFather.

2. Type `/mybots`.
3. Select your bot.

4. Click "Bot Settings".
5. Activate the "Inline Mode" option.

## 7. Run the start.bat File

Start your bot by opening the `start.bat` file.

## 8. Your Bot is Now Working!

Check and test all the functions of your bot.
