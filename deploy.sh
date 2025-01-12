#!/usr/bin/env sh

# abort on errors
if [ "$(git config --global --get user.email)" ]
  then
    if [ "$(git config user.email)" = "845299100@qq.com" ]
    then
      # build
      npm run build

      # navigate into the build output directory
      cd docs/.vitepress/dist

      # if you are deploying to a custom domain
      # echo 'www.example.com' > CNAME

      git init
      git branch -m main
      git add -A
      git commit -m 'deploy'

      # if you are deploying to https://<USERNAME>.github.io
      git push -f git@github.com:hugheschoi/hugheschoi.github.io.git main

    else
      echo "The git user is not hugheschoi"
    fi
    # if you are deploying to https://<USERNAME>.github.io/<REPO>
    # git push -f git@github.com:hugheschoi/documents.git main:gh-pages
else
  echo "Git user information is not configured"
fi
