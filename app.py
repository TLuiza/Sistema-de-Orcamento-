# app.py (CÓDIGO COMPLETO FINAL COM CÁLCULO 3D CORRIGIDO)

from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from datetime import datetime 

# --- CONFIGURAÇÃO E FILTRO DE DATA ---

def today_filter(date_str):
    return datetime.now().strftime('%d/%m/%Y')

app = Flask(__name__)
app.jinja_env.filters['today'] = today_filter 

# Configura a pasta onde as imagens enviadas serão salvas.
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tipos de arquivos permitidos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ROTAS DA APLICAÇÃO ---

@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'GET':
        return render_template('formulario.html')

    if request.method == 'POST':
        # 1. Coleta os dados do formulário
        nome_produto = request.form.get('nome_produto')
        descricao = request.form.get('descricao')
        
        # COLETANDO AS NOVAS VARIÁVEIS DO FORMULÁRIO (NENHUMA VARIÁVEL 'METRAGEM' AQUI)
        largura = request.form.get('largura')
        altura = request.form.get('altura')
        comprimento = request.form.get('comprimento')
        valor_m = request.form.get('valor_m') 
        
        file = request.files.get('foto') 

        # 2. Valida e salva o arquivo de imagem
        filename = None
        try: 
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
        
        # 3. Realiza o Cálculo do Orçamento: L * A * C * V/m
        valor_total = "Erro no cálculo: Verifique as dimensões e o Valor por Metro."
        volume = None
        
        try:
            # Converte os campos recém-coletados
            l = float(largura)
            a = float(altura)
            c = float(comprimento)
            v = float(valor_m)
            
            volume = l * a * c
            valor_total = volume * v
            
        except ValueError:
            # Caso algum campo não seja um número
            l, a, c, v = largura, altura, comprimento, valor_m
        
        # 4. Envia os dados para a página de orçamento
        return render_template(
            'orcamento.html',
            nome=nome_produto,
            descricao=descricao,
            largura=largura, 
            altura=altura,
            comprimento=comprimento,
            volume=volume if isinstance(volume, (int, float)) else None, 
            valor_m=valor_m,
            valor_total=valor_total,
            caminho_foto=os.path.join(UPLOAD_FOLDER, filename) if filename else None
        )


# --- EXECUÇÃO DA APLicação ---
if __name__ == '__main__':
    app.run(debug=True)