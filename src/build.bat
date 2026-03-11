@echo off
echo Cleaning old build...
rmdir /s /q build
rmdir /s /q dist

echo Building yt-downloader...

pyinstaller --name "yt-downloader-gui" ^
  --windowed ^
  --icon=favicon.ico ^
  --add-data "assets;assets" ^
  --add-data "bin;bin" ^
  main.py

echo Build finished!
pause