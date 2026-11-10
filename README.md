# BlueCart Shopping Cart

BlueCart is a starter online shop built with Python Flask, HTML, CSS, JavaScript and Supabase.

## Files
- `app.py` — Flask routes and Supabase server connection
- `templates/index.html` — shop page and cart drawer
- `static/style.css` — blue-and-white responsive styling
- `static/app.js` — product loading, cart and checkout
- `schema.sql` — Supabase tables and sample products
- `.env.example` — environment variable template

## Supabase setup
1. Create a Supabase project.
2. Open its SQL Editor and run `schema.sql`.
3. Copy the Project URL and service-role key from Project Settings / API.
4. Copy `.env.example` to `.env` and fill in those values.

**Never commit `.env` or expose the service-role key in browser code or GitHub.** The key is used only by Flask on the server.

## Run on Windows
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000.

## Push to GitHub
```powershell
git init
git add .
git status
git commit -m "Initial BlueCart project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/bluecart-shopping-cart.git
git push -u origin main
```
Check `git status` to ensure `.env` is not staged before committing.

## Important
This is a learning starter, not a production payment system. It does not process payments. Add authentication, abuse protection, secure transactional order creation, and a payment provider before accepting real orders.
