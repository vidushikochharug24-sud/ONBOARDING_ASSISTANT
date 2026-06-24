# Onboarding Assistant - React Frontend

A modern, enterprise-grade React frontend for the Codebase Onboarding Assistant application. Built with React 19, Vite, and styled with a Cisco-inspired design system.

## Features

- **Landing Page**: Marketing landing page showcasing the app's capabilities
- **Authentication**: Secure login and signup with JWT token management
- **Dashboard**: Main app interface with sidebar navigation
- **Codebase Analysis**: Support for GitHub URLs, ZIP files, and documentation uploads
- **Guide Generation**: Automatic generation of onboarding guides using AI
- **Guide Management**: View, copy, and download generated guides
- **Enterprise Design**: Professional dark theme with Cisco blue accent colors

## Tech Stack

- **React 19**: Latest React with modern hooks
- **Vite**: Lightning-fast build tool and dev server
- **React Router DOM 7**: Client-side routing
- **Axios**: HTTP client for API requests
- **React Markdown**: Markdown rendering for guides

## Getting Started

### Prerequisites

- Node.js 16+ (recommended 18+)
- npm or yarn package manager

### Installation

1. Install dependencies:
```bash
npm install
```

2. Ensure the backend API is running at `http://localhost:5001`

### Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173` by default.

### Building

Create a production build:
```bash
npm run build
```

The optimized production files will be in the `dist/` directory.

### Linting

Run the linter to check code quality:
```bash
npm run lint
```

## Project Structure

```
src/
├── components/          # Reusable React components
│   ├── LoadingSpinner.jsx
│   ├── Sidebar.jsx
│   ├── GuideTabs.jsx
│   ├── GuideDisplay.jsx
│   └── NewAnalysisForm.jsx
├── pages/              # Page components for routing
│   ├── Landing.jsx
│   ├── Login.jsx
│   ├── Signup.jsx
│   └── Dashboard.jsx
├── styles/             # CSS files organized by component/page
│   ├── global.css
│   ├── landing.css
│   ├── auth.css
│   ├── dashboard.css
│   ├── sidebar.css
│   ├── new-analysis.css
│   ├── tabs.css
│   ├── guide-display.css
│   ├── loading.css
│   └── ...
├── utils/              # Utility functions
│   ├── api.js          # Axios instance with interceptors
│   └── auth.js         # Authentication helpers (localStorage management)
├── App.jsx             # Root router component
└── main.jsx            # React DOM entry point
```

## Design System

### Color Palette

- **Navy Dark**: `#0d1b2a` - Main background
- **Navy Main**: `#1b2a3b` - Secondary background
- **Navy Light**: `#152032` - Sidebar background
- **Cisco Blue**: `#00bceb` - Primary accent
- **Cisco Blue (Hover)**: `#049fd9` - Interactive state
- **White**: `#ffffff` - Text/foreground
- **Text Light**: `#e0e0e0` - Secondary text
- **Border Color**: `#1e3a5f` - Subtle borders
- **Error Red**: `#ff4444` - Error states
- **Success Green**: `#4ade80` - Success states

### Typography

- **Font Family**: System fonts (Inter, Roboto, Helvetica)
- **Headings**: Bold, 600-700 weight
- **Body**: Regular, 14-16px size

### Components

- **Buttons**: Solid Cisco blue with white text, sharp corners, no pills
- **Forms**: Clean input fields with subtle borders, blue focus state
- **Cards**: Subtle blue borders with hover glow effect
- **Badges**: Colored tags for source types (GitHub, ZIP, PDF)

## API Integration

The frontend communicates with the backend API at `http://localhost:5001/api`. 

### Authentication Flow

1. User signs up/logs in
2. Backend returns JWT token
3. Token stored in `localStorage` as `"token"`
4. Token sent with every API request as `Authorization: Bearer {token}`
5. If token expires, user is redirected to login

### Key API Endpoints

- `POST /api/auth/signup` - Create new account
- `POST /api/auth/login` - Login to existing account
- `GET /api/analyze/guides` - Fetch user's guides
- `POST /api/analyze/github` - Analyze GitHub repository
- `POST /api/analyze/zip` - Analyze ZIP file
- `POST /api/storage/upload` - Upload file to storage

## Environment Variables

Currently, the backend URL is hardcoded to `http://localhost:5001`. 

To make it configurable, create a `.env` file:
```
VITE_API_BASE_URL=http://localhost:5001
```

Then update `src/utils/api.js`:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api';
```

## Styling Approach

The frontend uses a **utility-first CSS approach** with:

- **CSS Variables** for colors (defined in `styles/global.css`)
- **Component-scoped CSS** files for modularity
- **Responsive Design** using media queries
- **No CSS frameworks** - pure CSS for maximum control and minimal bundle size

### CSS Variables Usage

```css
:root {
  --navy-dark: #0d1b2a;
  --cisco-blue: #00bceb;
  /* ... more variables */
}

/* Usage in components */
button {
  background-color: var(--cisco-blue);
  color: var(--white);
}
```

## Browser Support

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance Optimizations

- **Code Splitting**: Routes are lazily loaded via React Router
- **Production Build**: Minified and gzipped assets
- **CSS Optimization**: Unused CSS is removed during build
- **Image Optimization**: SVG icons used where possible

## Debugging

### Development Tools

- React DevTools browser extension recommended
- Vite's built-in HMR (Hot Module Replacement) for instant updates
- Browser console for error messages

### Common Issues

**API Connection Errors**
- Ensure backend is running on `http://localhost:5001`
- Check browser console for CORS errors
- Verify token is being sent in request headers

**Build Errors**
- Clear `node_modules` and `dist` directories
- Run `npm install` again
- Check for syntax errors in component files

**Styling Issues**
- Verify CSS files are imported in components
- Check CSS variable names in `styles/global.css`
- Use browser DevTools to inspect computed styles

## Future Enhancements

- [ ] Dark/Light mode toggle
- [ ] Real-time collaboration features
- [ ] Advanced guide editor with formatting options
- [ ] Guide versioning and history
- [ ] Team workspace management
- [ ] Custom branding/theming
- [ ] Offline support with service workers
- [ ] Mobile-responsive improvements

## Contributing

When adding new features:

1. Create components in appropriate folder (`components/` or `pages/`)
2. Style with dedicated CSS file in `styles/`
3. Add necessary utility functions in `utils/`
4. Update routing in `App.jsx` if needed
5. Test locally with `npm run dev`
6. Build to verify no errors: `npm run build`

## License

Proprietary - All rights reserved

## Support

For issues or questions, contact the development team.
