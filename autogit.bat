@echo off
setlocal

:: Prompt the user for a commit message
set /p userMessage="Enter commit message (leave blank for default message): "

:: Check if the user entered a message
if "%userMessage%"=="" (
    :: No message entered, use the default message
    set commitMessage="commit_made_at_%time%_date:%date%"
) else (
    :: User entered a message, use it for the commit
    set commitMessage=%userMessage% on %time% date:%date%
)

:: Add all changes to the staging area
git add .

:: Commit with the determined message
git commit -m "%commitMessage%"

:: Push changes to the master branch
git push origin master

:: Pause the script to view the output
pause
