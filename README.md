# Humor Me [Incomplete ReadMe]

## Description
A small python application, built with pyside6. It fetches insult from [Evil Insults](https://evilinsult.com/api/#generate-insult-get).
Some insults are more ... potent than others. It also gets jokes from [jokeapi](https://jokeapi.dev/)


![./resources/images/img_1.png](/resources/images/img_1.png)

## Usage
When you run the main entry point `app.py` it creates a floating window stuck to the right side of your primary screen.

![./resources/images/img.png](/resources/images/img.png)

Double-clicking on the roast me floating element will fetch and insult or a joke. 
By defaults, insults get show every 1.25 minutes

Right-click on the bubble to close the window

![./resources/images/img_2.png](/resources/images/img_2.png)

`Note` To completely close the application, after closing the main window, also close the window from system tray.

## Personalization
Right-click on the bubble and go to the settings window. there you can customize your feed. 


## For Devs

### Running locally
...

- build resource file
```cmd
pyside6-rcc.exe .\resources\resources.qrc -o .\resources\resources.py 
```