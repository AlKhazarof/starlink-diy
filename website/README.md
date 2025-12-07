# Starlink DIY Website

This is the promotional/informational website for the Starlink DIY project.

## 🌐 Live Website

The website is hosted on GitHub Pages at: `https://alkhazarof.github.io/starlink-diy/`

## 📁 Files

- `index.html` - Main HTML file with semantic structure
- `style.css` - Modern CSS with responsive design and animations
- `script.js` - Interactive JavaScript features

## ✨ Features

- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Modern UI**: Dark theme with gradient accents and smooth animations
- **Interactive Elements**: Smooth scrolling, copy-to-clipboard, mobile navigation
- **Accessibility**: Keyboard navigation, ARIA labels, semantic HTML
- **Performance**: Optimized animations, debounced scroll handlers
- **SEO**: Meta tags, Open Graph, Twitter Card support

## 🚀 Local Development

To run the website locally:

1. Navigate to the website directory:
   ```bash
   cd website
   ```

2. Open with a local server (choose one):
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Python 2
   python -m SimpleHTTPServer 8000
   
   # Node.js (if you have npx)
   npx serve
   
   # PHP
   php -S localhost:8000
   ```

3. Open your browser to `http://localhost:8000`

## 🎨 Customization

### Colors

The color scheme is defined in CSS variables at the top of `style.css`:

```css
:root {
    --primary-color: #00d4ff;
    --secondary-color: #7c3aed;
    --dark-bg: #0a0e27;
    /* ... */
}
```

### Content

Edit the `index.html` file to update content. The structure is organized into semantic sections:

- Hero section with project tagline
- Features showcase
- Getting Started guide
- Documentation links
- Contribute section
- Legal notice
- Footer

## 🌟 GitHub Pages Deployment

The website is automatically deployed to GitHub Pages using GitHub Actions. The deployment workflow is triggered on every push to the `main` branch that modifies files in the `website/` directory.

**Live URL**: `https://alkhazarof.github.io/starlink-diy/`

For detailed information about the deployment process, troubleshooting, and manual deployment, see the [GitHub Pages Setup Guide](../docs/github-pages-setup.md).

### Quick Deployment Info

- **Workflow File**: `.github/workflows/deploy-website.yml`
- **Trigger**: Push to `main` branch (changes to `website/**`)
- **Source**: `website/` directory
- **Deployment Time**: Usually 1-2 minutes after push

## 📱 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

To contribute to the website:

1. Make your changes
2. Test locally
3. Ensure responsive design works on mobile
4. Submit a pull request

## 📄 License

MIT License - Same as the main project
