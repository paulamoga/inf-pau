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

# --- AUTENTIFICARE (LOGIN) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form.get('username')
        pw_input = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE nume=%s AND parola=%s", (user_input, pw_input))
        account = cursor.fetchone()
        cursor.close()
        conn.close()

        if account:
            session['user_id'] = account['id']
            session['user_name'] = account['nume']
            return redirect(url_for('dashboard'))
        else:
            return "Eroare: Utilizator sau parolă incorectă! <a href='/login'>Încearcă din nou</a>"
            
    return render_template('login.html')

# --- ÎNREGISTRARE ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form.get('username')
        email = request.form.get('email')
        pw = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (nume, email, parola, xp, nivel) VALUES (%s, %s, %s, 0, 1)", (user, email, pw))
            conn.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return f"Eroare la baza de date: {err}"
        finally:
            cursor.close()
            conn.close()
            
    return render_template('register.html')

# --- DASHBOARD ---
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nume, xp, nivel FROM users WHERE id = %s", (session['user_id'],))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', user=user_data)

# --- LISTA DE LECȚII ---
@app.route('/lectii')
def lectii():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT nivel FROM users WHERE id = %s", (session['user_id'],))
    user_row = cursor.fetchone()
    nivel_user = user_row['nivel'] if user_row else 1

    cursor.execute("SELECT * FROM lectii")
    toate_lectiile = cursor.fetchall()
    
    cursor.execute("SELECT lectie_id FROM progres WHERE utilizator_id = %s", (session['user_id'],))
    terminate = [row['lectie_id'] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return render_template('lectii.html', 
                           lectii=toate_lectiile, 
                           nivel_actual=nivel_user, 
                           terminate=terminate)

# --- VIZUALIZARE CONȚINUT LECȚIE ---
@app.route('/view_lectie/<int:lectie_id>')
def view_lectie(lectie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lectii WHERE id = %s", (lectie_id,))
    lectie = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not lectie:
        return "Lecția nu există!", 404
        
    return render_template('view_lectie.html', lectie=lectie)

# --- PAGINA DE QUIZ ---
@app.route('/quiz/<int:lectie_id>')
def quiz(lectie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Folosim numele corecte din tabelul tău: 'intrebare', 'varianta1' etc.
    cursor.execute("SELECT * FROM intrebari WHERE lectie_id = %s", (lectie_id,))
    intrebarile = cursor.fetchall()
    
    cursor.execute("SELECT titlu FROM lectii WHERE id = %s", (lectie_id,))
    lectie = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('quiz.html', intrebari=intrebarile, lectie=lectie, lectie_id=lectie_id)

# --- PROCESARE QUIZ (CU LEVEL UP INTEGRAT) ---
@app.route('/submit_quiz/<int:lectie_id>', methods=['POST'])
def submit_quiz(lectie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # 1. Marcare progres
        cursor.execute("""
            INSERT INTO progres (utilizator_id, lectie_id, completata) 
            VALUES (%s, %s, 1) 
            ON DUPLICATE KEY UPDATE completata = 1
        """, (session['user_id'], lectie_id))
        
        # 2. Adăugare 10 XP
        cursor.execute("UPDATE users SET xp = xp + 10 WHERE id = %s", (session['user_id'],))
        
        # 3. Verificare prag nivel
        cursor.execute("SELECT xp, nivel FROM users WHERE id = %s", (session['user_id'],))
        user_stats = cursor.fetchone()
        
        # Dacă ajunge la 40 XP (toate lecțiile de nivel 1 gata)
        if user_stats and user_stats['xp'] >= 40 and user_stats['nivel'] == 1:
            cursor.execute("UPDATE users SET nivel = 2 WHERE id = %s", (session['user_id'],))
            print("FELICITĂRI: Nivelul 2 deblocat!")

        conn.commit()
    except Exception as e:
        print(f"Eroare la submit_quiz: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('lectii'))

# --- LOGOUT ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)