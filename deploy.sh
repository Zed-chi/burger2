#!/bin/bash
set -e

echo "=> Stopping App"
systemctl stop burger-shop
echo "=> App Stopped"
echo ""
echo "=> Pulling from Git"
git pull
echo "=> Githubbed"
echo ""
echo "=> Installing npm packages"
npm i
echo "=> npm packages installed"
echo ""
echo "=> Building frontend"
npx esbuild ./bundles-src/index.js --bundle --loader:.png=file --loader:.js=jsx --outdir=bundles 
echo "=> Frontend got builded"
echo ""
echo "=> Installing Deps for python app"
pip install -r requirements.txt
echo "=> Python app deps installed"
echo ""
echo "=> Trying to do some migrates"
python3 manage.py migrate
echo "=> Migration done"
echo ""
echo "=> Collecting static files"
(echo yes) | python3 manage.py collectstatic
echo "=> Static files collected"
echo ""
echo "=> Starting app"
systemctl start burger-shop
echo "=> App started"
echo "=> Bye"
echo ""

hash=$(git rev-parse --short HEAD)

curl --request POST \
     --url https://api.rollbar.com/api/1/deploy \
     --header 'X-Rollbar-Access-Token: e5d425a462ca441fb7de7f0f7c4095c8' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data "
{
  \"environment\": \"prod\",
  \"revision\": \"`hash`\"
}
"
