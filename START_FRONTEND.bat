@echo off
echo Starting Frontend Server...
cd /d "E:\skill passport 360\frontend"
echo.
echo Installing dependencies if needed...
call npm install
echo.
echo Starting Vite dev server...
echo Frontend will be available at: http://localhost:3000
echo.
call npm run dev
pause

