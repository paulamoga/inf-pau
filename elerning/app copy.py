from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = "cheie_secreta_bluelearn" 

# Configurație Bază de Date
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'elearning'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# --- LOGIN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Folosim request.form.get pentru siguranță
        user = request.form.get('username')
        pw = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Folosim numele corecte ale coloanelor din tabelul tău 'users'[cite: 3]
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pw))
        account = cursor.fetchone()
        cursor.close()
        conn.close()

        if account:
            session['user_id'] = account['id']
            session['user_name'] = account['username']
            return redirect(url_for('dashboard'))
        else:
            return "Utilizator sau parolă incorectă! <a href='/login'>Încearcă din nou</a>"
            
    return render_template('login.html')

# --- REGISTER ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Inserăm utilizatorul cu valorile implicite pentru XP și Level[cite: 3]
            cursor.execute("INSERT INTO users (username, password, xp, level) VALUES (%s, %s, 0, 1)", (user, pw))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return f"Eroare la înregistrare: {err}"
            
    return render_template('register.html')

# --- DASHBOARD ---
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT username, xp, level FROM users WHERE id = %s", (session['user_id'],))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', user=user_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Rulăm pe portul 5001
    app.run(debug=True, port=5001)