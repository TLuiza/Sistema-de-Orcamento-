# app.py

from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from datetime import datetime 

# --- CONFIGURAÇÃO E FILTRO DE DATA ---

# Cria um filtro para usar a data de hoje no HTML
def today_filter(date_str):
    return datetime.now().strftime('%d/%m/%Y')

app = Flask(__name__)
# Registra o filtro 'today' para podermos usá-lo no template HTML
app.jinja_env.filters['today'] = today_filter 

# Configura a pasta onde as imagens enviadas serão salvas.
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tipos de arquivos permitidos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Função para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ROTAS DA APLICAÇÃO ---

# Rota da Página Inicial (o Formulário)
@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'GET':
        # Se for GET, apenas mostra o formulario.html
        return render_template('formulario.html')

    if request.method == 'POST':
        # 1. Coleta os dados do formulário
        nome_produto = request.form.get('nome_produto')
        descricao = request.form.get('descricao')
        metragem = request.form.get('metragem')
        valor_m2 = request.form.get('valor_m2')
        file = request.files.get('foto') 

        # 2. Valida e salva o arquivo de imagem
        filename = None
        # O try/except garante que a aplicação não quebre se o usuário não enviar uma imagem
        try: 
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
        
        # 3. Realiza o Cálculo do Orçamento
        try:
            m = float(metragem)
            v = float(valor_m2)
            valor_total = m * v
        except ValueError:
            valor_total = "Erro no cálculo: Verifique a metragem e o valor."
            m, v = metragem, valor_m2
            
        # 4. Envia os dados para a página de orçamento
        return render_template(
            'orcamento.html',
            nome=nome_produto,
            descricao=descricao,
            metragem=m,
            valor_m2=v,
            valor_total=valor_total,
            caminho_foto=os.path.join(UPLOAD_FOLDER, filename) if filename else None
        )


# --- EXECUÇÃO DA APLICAÇÃO ---
if __name__ == '__main__':
    # Roda o servidor web
    app.run(debug=True)