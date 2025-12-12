# Development Preferences for Web Applications

## Tech Stack Preferences

### Backend Framework
- **Primary Choice**: FastAPI (Python)
- **Why**: FastAPI provides excellent performance, automatic API documentation, type hints, and async support
- **Key Features to Leverage**:
  - Automatic OpenAPI/Swagger documentation
  - Pydantic models for data validation
  - Async/await support for better performance
  - Built-in dependency injection
  - Excellent TypeScript client generation

### Frontend Framework
- **Primary Choice**: Next.js 15+ with App Router
- **Why**: Best-in-class React framework with excellent developer experience and production features
- **Key Features**:
  - Server-side rendering (SSR) and static generation
  - Built-in TypeScript support
  - Excellent performance optimizations
  - Great mobile web experience
  - Strong ecosystem and documentation

### Alternative Frontend Options (in order of preference)
1. **Remix** - Full-stack web framework with excellent data loading
2. **Vite + React** - For simpler apps that don't need SSR
3. **SvelteKit** - Lightweight alternative with great performance

## Architecture Patterns

### Backend Structure (FastAPI)
```python
# Recommended project structure
app/
├── main.py              # FastAPI app entry point
├── models/              # Pydantic models
├── api/                 # API route handlers
│   ├── auth.py         # Authentication endpoints
│   ├── webhooks.py     # Webhook handlers
│   └── notifications.py # Notification endpoints
├── core/               # Core business logic
├── services/           # External service integrations
├── middleware/         # Custom middleware
└── utils/              # Utility functions
```

### Frontend Structure (Next.js)
```
src/
├── app/                 # App Router pages
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Home page
│   └── api/            # API routes (if needed)
├── components/         # React components
├── lib/                # Utility libraries
├── hooks/              # Custom React hooks
├── types/              # TypeScript type definitions
└── styles/             # Global styles
```

## Key Implementation Guidelines

### 1. Authentication & Authorization
- **Frontend**: Use secure token-based authentication (JWT)
- **Backend**: Implement proper JWT validation and refresh token flows
- **Example FastAPI middleware**:
```python
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(401, "Invalid token")
        return await get_user_by_id(user_id)
    except JWTError:
        raise HTTPException(401, "Invalid token")
```

### 2. API Design
- **Use RESTful principles** with proper HTTP methods
- **Implement proper error handling** with standardized error responses
- **Use Pydantic models** for request/response validation
- **Version your APIs** (e.g., `/api/v1/`)
- **Implement proper CORS** settings

### 3. Database Integration
- **Recommended**: SQLAlchemy with async support or Prisma
- **Use database migrations** for schema changes
- **Implement proper connection pooling**
- **Example models**: Users, Sessions, AppData

### 4. Frontend Best Practices
- **Use TypeScript** for better type safety
- **Implement proper error handling** and loading states
- **Follow mobile-first responsive design**
- **Use React Query/SWR** for data fetching and caching
- **Implement proper SEO** with Next.js metadata API

### 5. Deployment Preferences
- **Backend**: Railway, Fly.io, or similar Python-friendly platforms
- **Frontend**: Vercel (optimal for Next.js) or Netlify
- **Database**: PostgreSQL (Supabase, Neon, or similar)
- **CDN**: Cloudflare for static assets
- **Environment**: Containerized deployments with Docker

## Modern Web Application Considerations

### Progressive Web App (PWA) Features
- **Service workers** for offline functionality
- **App manifest** for installability
- **Push notifications** for user engagement
- **Responsive design** for mobile-first experience

### Performance Optimization
```typescript
// Example Next.js optimizations
import { Suspense } from 'react'
import dynamic from 'next/dynamic'

// Code splitting for heavy components
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <div>Loading...</div>
})

// Optimize images
import Image from 'next/image'
<Image src="/hero.jpg" alt="Hero" width={800} height={600} priority />
```

### State Management
- **Small apps**: React Context + useReducer
- **Medium apps**: Zustand or Valtio
- **Large apps**: Redux Toolkit with RTK Query
- **Server state**: React Query or SWR

## Development Workflow

### 1. Local Development
- **Backend**: `uvicorn main:app --reload --port 8000`
- **Frontend**: `npm run dev`
- **Database**: Docker Compose for local services
- **Hot reloading** for both frontend and backend

### 2. Testing Strategy
- **Backend**: pytest with async support, factory boy for fixtures
- **Frontend**: Jest + React Testing Library + Playwright for E2E
- **API Testing**: httpx for integration tests
- **Coverage**: Aim for >80% coverage on critical paths

### 3. Code Quality
- **Backend**: black (formatting), mypy (type checking), ruff (linting)
- **Frontend**: prettier (formatting), ESLint (linting), TypeScript strict mode
- **Pre-commit hooks** with husky
- **Automated CI/CD** with GitHub Actions

### 4. Deployment Pipeline
- **Staging environment** for testing
- **Environment-specific configs** using environment variables
- **Automated testing** before production deployment
- **Health checks** and monitoring

## Security Considerations

### Authentication & Authorization
- **Use secure password hashing** (bcrypt, argon2)
- **Implement proper session management**
- **Use HTTPS everywhere**
- **Implement rate limiting** for API endpoints
- **Validate all inputs** on both client and server

### Data Protection
- **Encrypt sensitive data** at rest
- **Use environment variables** for secrets
- **Implement proper logging** (avoid logging sensitive data)
- **Regular security audits** of dependencies

### Frontend Security
```typescript
// Example secure headers in Next.js
export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <meta httpEquiv="Content-Security-Policy" content="default-src 'self'" />
        <meta httpEquiv="X-Content-Type-Options" content="nosniff" />
        <meta httpEquiv="X-Frame-Options" content="DENY" />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

## Error Handling Patterns

### Frontend
```typescript
import { useErrorBoundary } from 'react-error-boundary'

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <h2>Something went wrong:</h2>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  )
}

// Usage
<ErrorBoundary FallbackComponent={ErrorFallback}>
  <MyComponent />
</ErrorBoundary>
```

### Backend
```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "type": "http_exception"
            }
        }
    )
```

## Recommended Libraries & Tools

### Backend Libraries
- **Core**: fastapi, uvicorn, pydantic, sqlalchemy
- **Auth**: python-jose, passlib, python-multipart
- **Database**: asyncpg (PostgreSQL), alembic (migrations)
- **HTTP**: httpx, aiofiles
- **Monitoring**: structlog, sentry-sdk
- **Testing**: pytest, pytest-asyncio, factory-boy

### Frontend Libraries
- **Core**: react, next.js, typescript
- **Styling**: tailwindcss, framer-motion
- **Data Fetching**: @tanstack/react-query, axios
- **Forms**: react-hook-form, zod
- **UI Components**: shadcn/ui, headlessui
- **Testing**: @testing-library/react, playwright

### Development Tools
- **Code Quality**: prettier, eslint, black, mypy
- **Containerization**: Docker, docker-compose
- **CI/CD**: GitHub Actions, GitLab CI
- **Monitoring**: Sentry, LogRocket
- **Documentation**: Swagger UI (auto-generated), Storybook

## Monitoring & Analytics

### Application Monitoring
- **Error tracking**: Sentry for both frontend and backend
- **Performance monitoring**: Web Vitals, API response times
- **Uptime monitoring**: UptimeRobot or similar
- **Database monitoring**: Connection pool metrics, query performance

### User Analytics
- **Privacy-first analytics**: Plausible or PostHog
- **User behavior**: Hotjar or LogRocket
- **A/B testing**: Optimizely or native implementation
- **Feature flags**: LaunchDarkly or similar

### Logging Strategy
```python
import structlog

logger = structlog.get_logger()

@app.post("/api/users")
async def create_user(user: UserCreate):
    logger.info("Creating user", email=user.email)
    try:
        # ... create user logic
        logger.info("User created successfully", user_id=new_user.id)
        return new_user
    except Exception as e:
        logger.error("Failed to create user", error=str(e), email=user.email)
        raise HTTPException(500, "Internal server error")
```

This setup provides a robust, scalable foundation for building modern web applications with Python and JavaScript technologies, emphasizing security, performance, and maintainability.

# Project Guidelines

 ## Git Commit Guidelines
 - **DO NOT** cite or reference Claude Code in any git commits
 - Git commit messages should be written as if authored by the developer
 - No mentions of AI assistance, Claude, or automated generation in commit messages

 ## Python Environment Setup
 - **Use uv for virtual environment management**
 - **Python version**: Python 3.11
 - **Virtual environment location**: `.venv` directory

 ### Setting up the environment:
 ```bash
 # If .venv doesn't exist, create it with uv
 uv venv --python 3.11

 # If .venv already exists, just use it
 source .venv/bin/activate  # On Unix/macOS
 # or
 .venv\Scripts\activate  # On Windows
 ```

 ### Installing dependencies:
 ```bash
 # Use uv for pip installing any dependencies
 uv pip install <package-name>

 # For requirements.txt
 uv pip install -r requirements.txt
 ```

 ### Important notes:
 - Always check if `.venv` already exists before creating a new one
 - Use the existing `.venv` if present to maintain consistency
 - All Python dependencies should be installed using `uv pip install`

 ## Streamlit Development Guidelines
 - **DO NOT** launch or relaunch Streamlit apps automatically
 - The user will launch Streamlit apps separately when needed
 - Focus on writing and editing the Streamlit code without running it
 - Assume the app is being run in a separate terminal/process by the user

## Claude Code or Codex or Gemini
- Do not sign git commits with Authored by Claude Code or anything mentioning Claude or Codex or Gemini
