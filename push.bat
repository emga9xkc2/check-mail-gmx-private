git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/emga9xkc2/check-mail-gmx-private.git
git push -u origin main


py "D:\Google Drive\My Data\python\obf\obfuscate-2023.py"

set mypath=%cd%



mkdir release
cd release


copy "%mypath%\README.md" "README.md"

xcopy /s /Y "%mypath%\setup" "setup\"
xcopy /s /Y "%mypath%\web" "web\"




git init
git add .
git commit -m "commit"
git branch -M main
git remote add origin https://github.com/emga9xkc2/check-mail-gmx.git
git push -u origin main
@rem git push -f origin main #chay xong nay` neu xay ra loi~ o tren
timeout /t 5
