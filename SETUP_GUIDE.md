# 🚀 Skill Passport 360 - Setup Guide

Complete guide to set up the React + FastAPI stack for Skill Passport 360.

## 📋 Prerequisites

- **Node.js** 18+ (for React frontend)
- **Python** 3.11+ (for FastAPI backend)
- **npm** or **yarn** (package manager)

## 🔧 Backend Setup (FastAPI)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install additional Python dependencies from your existing project:**
   ```bash
   # Navigate to your existing project
   cd ../Evolvex-AI--main/Evolvex-AI--main
   pip install -r requirements.txt
   ```

5. **Run the FastAPI server:**
   ```bash
   cd ../../backend
   python main.py
   ```
   
   Or with uvicorn:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

6. **Verify backend is running:**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 🎨 Frontend Setup (React)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Verify frontend is running:**
   - Frontend: http://localhost:3000
   - Should automatically proxy API calls to http://localhost:8000

## 🔌 API Configuration

The frontend is configured to connect to the backend API at `http://localhost:8000`. This is set in:
- `frontend/src/lib/api.ts` - API base URL
- `frontend/vite.config.ts` - Proxy configuration

## ✅ Verify Everything Works

1. **Backend Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status": "healthy"}`

2. **Frontend Connection:**
   - Open http://localhost:3000 in browser
   - Check browser console for any errors
   - Dashboard should load with demo profile data

## 🐛 Troubleshooting

### Backend Issues

**Import errors from src modules:**
- Make sure the path to your existing `src` folder is correct in `backend/routers/*.py`
- The backend routers reference: `../../Evolvex-AI--main/Evolvex-AI--main/src`

**CORS errors:**
- CORS is already configured in `backend/main.py`
- If you still get CORS errors, check the `allow_origins` list

### Frontend Issues

**API connection errors:**
- Ensure backend is running on port 8000
- Check `frontend/src/lib/api.ts` for correct base URL
- Verify CORS is enabled in backend

**Module not found:**
- Run `npm install` again
- Delete `node_modules` and `package-lock.json`, then reinstall

**TypeScript errors:**
- Run `npm run build` to check for TypeScript issues
- Ensure all dependencies are installed

## 📁 Project Structure

```
skill-passport-360/
├── backend/
│   ├── main.py                 # FastAPI app entry
│   ├── requirements.txt        # Python dependencies
│   └── routers/                # API route modules
│       ├── resume.py
│       ├── career_score.py
│       ├── github.py
│       ├── interview.py
│       ├── learning.py
│       ├── analytics.py
│       ├── internship.py
│       └── profile.py
│
├── frontend/
│   ├── src/
│   │   ├── components/ui/      # Shadcn/ui components
│   │   ├── lib/
│   │   │   ├── api.ts         # Axios API client
│   │   │   └── utils.ts       # Utilities
│   │   ├── pages/
│   │   │   └── Dashboard.tsx  # Main dashboard
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
└── Evolvex-AI--main/          # Your existing project
    └── Evolvex-AI--main/
        └── src/               # Existing Python modules (used by backend)
```

## 🎯 Key Features Implemented

✅ **FastAPI Backend**
- RESTful API with 8 router modules
- CORS enabled for React frontend
- Integrates with existing Python ML models

✅ **React Frontend**
- Dark mode UI with Shadcn/ui
- Career Score radial gauge (Recharts)
- Skeleton loaders for ML processing
- Bento grid layout for Internship Matching & Upskilling
- All components connected to FastAPI endpoints

✅ **API Integration**
- Axios-based API client
- Type-safe API calls
- Error handling
- Loading states

## 🚀 Next Steps

1. **Test all endpoints** using the Swagger UI at http://localhost:8000/docs
2. **Customize the Dashboard** in `frontend/src/pages/Dashboard.tsx`
3. **Add more routes** by creating new router files in `backend/routers/`
4. **Extend components** by adding more Shadcn/ui components as needed

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Shadcn/ui Components](https://ui.shadcn.com/)
- [Recharts Documentation](https://recharts.org/)
- [TailwindCSS Documentation](https://tailwindcss.com/)


