# GitHub Pages Setup Guide

This document explains how the Starlink DIY website is published to GitHub Pages.

## 🌐 Live Website

The website is automatically deployed to: **https://alkhazarof.github.io/starlink-diy/**

## 📋 Overview

The project uses GitHub Actions to automatically deploy the website from the `website/` directory to GitHub Pages whenever changes are pushed to the `main` branch.

## 🚀 Deployment Workflow

The deployment is handled by the `.github/workflows/deploy-website.yml` workflow file, which:

1. **Triggers** on:
   - Push events to the `main` branch that modify files in `website/**`
   - Manual workflow dispatch (via GitHub Actions UI)

2. **Deploys**:
   - Checks out the repository
   - Configures GitHub Pages
   - Uploads the `website/` directory as an artifact
   - Deploys to GitHub Pages

3. **Permissions**:
   - `contents: read` - Read repository contents
   - `pages: write` - Write to GitHub Pages
   - `id-token: write` - Required for GitHub Pages deployment

## 🔧 Initial Setup (One-Time Configuration)

To enable GitHub Pages for the first time, a repository administrator needs to:

1. Go to the repository **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. The workflow will automatically deploy on the next push to `main`

## 📝 Making Changes to the Website

1. **Edit files** in the `website/` directory:
   - `index.html` - Website content and structure
   - `style.css` - Styling and visual design
   - `script.js` - Interactive functionality
   - `README.md` - Website documentation

2. **Test locally** before committing:
   ```bash
   cd website
   python3 -m http.server 8000
   # Visit http://localhost:8000 in your browser
   ```

3. **Commit and push** changes:
   ```bash
   git add website/
   git commit -m "Update website content"
   git push
   ```

4. **Deployment** happens automatically:
   - If pushed to `main` branch: deploys immediately
   - If pushed to a feature branch: deploys after PR is merged to `main`

## 🔍 Monitoring Deployments

1. Go to the **Actions** tab in the GitHub repository
2. Look for "Deploy Website to GitHub Pages" workflows
3. Click on a workflow run to see deployment status and logs
4. The deployment URL is shown in the workflow output

## 🐛 Troubleshooting

### Website not updating after push

1. Check the **Actions** tab for workflow status
2. Verify that changes were pushed to the `main` branch
3. Ensure changes were made to files in the `website/` directory
4. Check workflow logs for errors

### 404 Page Not Found

1. Verify GitHub Pages is enabled in repository settings
2. Check that the source is set to **GitHub Actions**
3. Wait a few minutes after deployment completes
4. Clear browser cache and try again

### Workflow Permission Errors

1. Go to **Settings** → **Actions** → **General**
2. Under "Workflow permissions", ensure:
   - "Read and write permissions" is selected, OR
   - "Read repository contents and packages permissions" + Pages permissions are granted

## 📚 Workflow File Reference

The workflow file is located at: `.github/workflows/deploy-website.yml`

Key configuration:
```yaml
on:
  push:
    branches:
      - main
    paths:
      - 'website/**'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write
```

## 🔗 Related Documentation

- [Website README](../website/README.md) - Website structure and local development
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## ✅ Deployment Checklist

When setting up GitHub Pages for the first time:

- [ ] Repository Settings → Pages → Source set to "GitHub Actions"
- [ ] Workflow file exists at `.github/workflows/deploy-website.yml`
- [ ] Website files exist in `website/` directory
- [ ] Push to `main` branch or manually trigger workflow
- [ ] Verify deployment in Actions tab
- [ ] Visit https://alkhazarof.github.io/starlink-diy/ to confirm

## 🎯 Best Practices

1. **Always test locally** before pushing to main
2. **Use feature branches** for significant changes
3. **Review changes** in PR before merging to main
4. **Monitor deployments** in the Actions tab after merging
5. **Keep website files** in the `website/` directory only
6. **Optimize assets** (images, CSS, JS) for faster load times
7. **Test responsive design** on different screen sizes

---

*For questions or issues with deployment, check the Actions logs or open an issue in the repository.*
