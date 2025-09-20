# Security Guidelines

## 🔒 Environment Variables

**IMPORTANT**: Never commit `.env` files to the repository!

### Setup Instructions:

1. **Copy the example file**:
   ```bash
   cp .env.example .env
   ```

2. **Update the values** in `.env` with your actual credentials:
   - `SECRET_KEY`: Generate a secure random key
   - `MAIL_USERNAME`: Your actual email address
   - `MAIL_PASSWORD`: Your Gmail app password (not regular password!)
   - `DATABASE_URL`: Your database connection string

3. **Never commit the `.env` file** - it's already in `.gitignore`

## 🛡️ Security Best Practices

### Email Setup (Gmail)
1. Enable 2-Factor Authentication
2. Generate an App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App Passwords
   - Generate password for "Mail"
   - Use this in your `.env` file

### Production Deployment
- Use strong, unique SECRET_KEY
- Use environment variables or secure vaults for credentials
- Enable HTTPS
- Use production database (not SQLite)

## 🚫 What NOT to Commit

- `.env` files
- Database files (`.db`, `.sqlite`)
- Log files
- Cache directories
- IDE configuration files
- Any files containing passwords, API keys, or sensitive data

## ✅ Safe to Commit

- `.env.example` (template with dummy values)
- Source code files
- Static assets (images, CSS, JS)
- Documentation
- Configuration templates