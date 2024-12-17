git config --local user.email "github-action@users.noreply.github.com"
git config --local user.name "GitHub Action"
git remote set-url origin https://github-action:$GITHUB_TOKEN@github.com/${{ github.repository_owner }}/${{ github.event.repository.name }}.git
git add .
git commit -m "Update ${pkgname}-version"
git push origin main
