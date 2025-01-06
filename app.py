from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Nastavení pro SQLite databázi
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializace databáze a migrací
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model pro řádky v databázi
class Row(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jmeno = db.Column(db.String(100), nullable=False)
    vek = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Row('{self.id}', '{self.jmeno}', '{self.vek}')"

@app.route('/')
def index():
    # Získání všech řádků z databáze
    rows = Row.query.all()
    return render_template('index.html', data=rows)

@app.route('/add', methods=['POST'])
def add_row():
    jmeno = request.form['jmeno']
    vek = request.form['vek']
    
    # Vytvoření nového řádku a uložení do databáze
    new_row = Row(jmeno=jmeno, vek=vek)
    db.session.add(new_row)
    db.session.commit()  # Uložení změn do databáze
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['GET'])
def delete_row(id):
    row = Row.query.get(id)  # Získání řádku podle ID
    if row:
        db.session.delete(row)  # Odstranění řádku
        db.session.commit()  # Uložení změn do databáze
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
