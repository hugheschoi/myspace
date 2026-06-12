npm run build
cp '最新文档/confluence/简历/蔡壮炳-高级前端工程师简历.html' docs/.vitepress/dist/index.html
cd docs/.vitepress/dist
git init
git branch -M main
git add -A
git commit -m 'deploy resume homepage'
git push -f git@github.com:hugheschoi/hugheschoi.github.io.git main