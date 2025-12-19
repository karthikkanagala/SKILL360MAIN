# Skill Passport 360 - React Frontend

Modern React frontend built with Vite, TailwindCSS, and Shadcn/ui.

## Features

- 🎨 **Dark Mode UI** - High-end dark theme with Shadcn/ui components
- 📊 **Animated Data Viz** - Recharts for Career Score radial gauge and charts
- ⚡ **Skeleton Loaders** - Prevents broken UI during ML processing
- 📦 **Bento Grid Layout** - Modern card-based layout for Internship Matching and Upskilling Paths
- 🔌 **API Integration** - All components connected to FastAPI backend

## Getting Started

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

The app will run on `http://localhost:3000` and proxy API requests to `http://localhost:8000`.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── ui/          # Shadcn/ui components
│   ├── lib/
│   │   ├── api.ts       # Axios API client
│   │   └── utils.ts     # Utility functions
│   ├── pages/
│   │   └── Dashboard.tsx  # Main dashboard component
│   ├── App.tsx
│   └── main.tsx
└── package.json
```

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **Shadcn/ui** - UI components
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **React Router** - Navigation


