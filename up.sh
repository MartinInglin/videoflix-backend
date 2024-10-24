pip freeze > requirements.txt
git add .
git commit -m "$*"
git push
ssh m.inglin@34.65.54.74 "cd videoflix-backend && sudo su m_inglin1985 && git pull"