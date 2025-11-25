from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto


app = Flask(__name__)

varastot = {}
app_state = {'counter': 0}


def get_next_id():
    app_state['counter'] += 1
    return app_state['counter']


@app.route('/')
def index():
    return render_template('index.html', varastot=varastot)


@app.route('/create', methods=['GET', 'POST'])
def create_varasto():
    if request.method == 'POST':
        nimi = request.form.get('nimi', 'Varasto')
        kuvaus = request.form.get('kuvaus', '')
        tilavuus = float(request.form.get('tilavuus', 10))
        alku_saldo = float(request.form.get('alku_saldo', 0))

        varasto_id = get_next_id()
        varastot[varasto_id] = {
            'nimi': nimi,
            'kuvaus': kuvaus,
            'varasto': Varasto(tilavuus, alku_saldo)
        }
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/varasto/<int:varasto_id>')
def view_varasto(varasto_id):
    if varasto_id not in varastot:
        return redirect(url_for('index'))
    return render_template(
        'view.html',
        varasto_id=varasto_id,
        data=varastot[varasto_id]
    )


@app.route('/varasto/<int:varasto_id>/edit', methods=['GET', 'POST'])
def edit_varasto(varasto_id):
    if varasto_id not in varastot:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nimi = request.form.get('nimi', varastot[varasto_id]['nimi'])
        default_kuvaus = varastot[varasto_id].get('kuvaus', '')
        kuvaus = request.form.get('kuvaus', default_kuvaus)
        varastot[varasto_id]['nimi'] = nimi
        varastot[varasto_id]['kuvaus'] = kuvaus
        return redirect(url_for('view_varasto', varasto_id=varasto_id))

    return render_template(
        'edit.html',
        varasto_id=varasto_id,
        data=varastot[varasto_id]
    )


@app.route('/varasto/<int:varasto_id>/add', methods=['POST'])
def add_to_varasto(varasto_id):
    if varasto_id not in varastot:
        return redirect(url_for('index'))

    maara = float(request.form.get('maara', 0))
    varastot[varasto_id]['varasto'].lisaa_varastoon(maara)
    return redirect(url_for('view_varasto', varasto_id=varasto_id))


@app.route('/varasto/<int:varasto_id>/remove', methods=['POST'])
def remove_from_varasto(varasto_id):
    if varasto_id not in varastot:
        return redirect(url_for('index'))

    maara = float(request.form.get('maara', 0))
    varastot[varasto_id]['varasto'].ota_varastosta(maara)
    return redirect(url_for('view_varasto', varasto_id=varasto_id))


@app.route('/varasto/<int:varasto_id>/delete', methods=['POST'])
def delete_varasto(varasto_id):
    if varasto_id in varastot:
        del varastot[varasto_id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False)
