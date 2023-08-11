from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import forms

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)
Migrate(app, db)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class Darbuotojas(db.Model):
    __tablename__ = 'darbuotojas'
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column('vardas', db.String)
    pavarde = db.Column('pavarde', db.String)
    departamento_id = db.Column(db.Integer, db.ForeignKey(
        'departamentas.id', ondelete='SET NULL'))


class Departamentas(db.Model):
    __tablename__ = 'departamentas'
    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column('pavadinimas', db.String)


@app.route('/darbuotojai')
def darbuotojai():
    darbuotojai = db.session.query(Darbuotojas, Departamentas).join(Departamentas).all()  #sujungiam darbuotojų ir dep. lenteles, kad gautume bendrą info.
    return render_template('darbuotojai.html', visi_darbuotojai=darbuotojai)


@app.route('/departamentai')
def departamentai():
    visi_departamentai = Departamentas.query.all()
    departamentai = []

    for departamentas in visi_departamentai:
        darbuotojai = []
        for elementas in db.session.query(Darbuotojas).filter(Darbuotojas.departamento_id == departamentas.id).all():
            darbuotojai.append(elementas)
        departamentai.append({
            'departamentas': departamentas,
            'darbuotojai': darbuotojai
        })

    return render_template('departamentai.html', visi_departamentai=departamentai)



@app.route('/departamentai/istrinti/<int:id>')
def istrinti_departamenta(id):
    departamentas = Departamentas.query.get(id)
    db.session.delete(departamentas)
    db.session.commit()
    return redirect(url_for('departamentai'))


@app.route('/darbuotojai/istrinti/<int:id>')
def istrinti_darbuotoja(id):
    darbuotojas = Darbuotojas.query.get(id)
    db.session.delete(darbuotojas)
    db.session.commit()
    return redirect(url_for('darbuotojai'))


@app.route('/darbuotojai/naujas', methods=['GET', 'POST'])
def sukurti_darbuotoja():
    forma = forms.DarbuotojasForm()
    if forma.validate_on_submit():
        naujas_darbuotojas = Darbuotojas(vardas=forma.vardas.data,
                                         pavarde=forma.pavarde.data, departamento_id=forma.departamentas.data.id)
        db.session.add(naujas_darbuotojas)
        db.session.commit()
        return redirect(url_for('darbuotojai'))
    return render_template('sukurti_darbuotoja.html', forma=forma)


@app.route('/departamentai/naujas', methods=['GET', 'POST'])
def sukurti_departamenta():
    forma = forms.DepartamentasForm()
    if forma.validate_on_submit():
        naujas_departamentas = Departamentas(
            pavadinimas=forma.pavadinimas.data)
        db.session.add(naujas_departamentas)
        db.session.commit()
        return redirect(url_for('departamentai'))
    return render_template('sukurti_departamenta.html', forma=forma)


@app.route("/darbuotojai/atnaujinti/<int:id>", methods=['GET', 'POST'])
def atnaujinti_darbuotoja(id):
    forma = forms.DarbuotojasForm()
    darbuotojas = Darbuotojas.query.get(id)
    if forma.validate_on_submit():
        darbuotojas.vardas = forma.vardas.data
        darbuotojas.pavarde = forma.pavarde.data
        darbuotojas.departamento_id = forma.departamentas.data.id
        db.session.commit()
        return redirect(url_for('darbuotojai'))
    return render_template("atnaujinti_darbuotoja.html", forma=forma, darbuotojas=darbuotojas)


@app.route("/departamentai/atnaujinti/<int:id>", methods=['GET', 'POST'])
def atnaujinti_departamenta(id):
    forma = forms.DepartamentasForm()
    departamentas = Departamentas.query.get(id)
    if forma.validate_on_submit():
        departamentas.pavadinimas = forma.pavadinimas.data
        db.session.commit()
        return redirect(url_for('departamentai'))
    return render_template("atnaujinti_departamenta.html", forma=forma, departamentas=departamentas)


if __name__ == '__main__':
    app.run(debug=True)
