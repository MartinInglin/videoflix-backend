source ./env/bin/activate

pip freeze > requirements.txt

git add .
git commit -m "$*"
git push

ssh m.inglin@34.65.54.74 "cd /home/m_inglin1985/projects/videoflix-backend && git pull"
