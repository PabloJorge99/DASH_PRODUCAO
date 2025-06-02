from flask import Flask, render_template

app = Flask(__name__)

# Dados organizados por semana (com grafia corrigida)
planos_por_semana = {
    "Semana 1": [
        {"id": "25101", "tipo": "plaina", "imagem": "plaina.png", "progresso_planejamento": 85, "progresso_producao": 45},
        {"id": "25201", "tipo": "rasthor", "imagem": "rasthor.png", "progresso_planejamento": 60, "progresso_producao": 30},
        {"id": "25111", "tipo": "plaina", "imagem": "plaina.png", "progresso_planejamento": 95, "progresso_producao": 75},
        {"id": "25221", "tipo": "rasthor", "imagem": "rasthor.png", "progresso_planejamento": 68, "progresso_producao": 39}
    ],
    "Semana 2": [
        {"id": "25301", "tipo": "plaina", "imagem": "plaina.png", "progresso_planejamento": 92, "progresso_producao": 78},
        {"id": "25401", "tipo": "rasthor", "imagem": "rasthor.png", "progresso_planejamento": 45, "progresso_producao": 20},
        {"id": "25131", "tipo": "plaina", "imagem": "plaina.png", "progresso_planejamento": 85, "progresso_producao": 45},
        {"id": "25241", "tipo": "rasthor", "imagem": "rasthor.png", "progresso_planejamento": 80, "progresso_producao": 35}
    ],
    "Semana 3": [
        {"id": "25501", "tipo": "plaina", "imagem": "plaina.png", "progresso_planejamento": 100, "progresso_producao": 95},
        {"id": "25601", "tipo": "rasthor", "imagem": "rasthor.png", "progresso_planejamento": 30, "progresso_producao": 10},
        {"id": "25151", "tipo": "plaina", "imagem": "plaina.png", "progresso_planejamento": 85, "progresso_producao": 55},
        {"id": "25261", "tipo": "rasthor", "imagem": "rasthor.png", "progresso_planejamento": 50, "progresso_producao": 30}
    ],
    "Semana 4": [
        {"id": "25701", "tipo": "plaina", "imagem": "plaina.png", "progresso_planejamento": 75, "progresso_producao": 60},
        {"id": "25801", "tipo": "rasthor", "imagem": "rasthor.png", "progresso_planejamento": 80, "progresso_producao": 25},
        {"id": "25771", "tipo": "plaina", "imagem": "plaina.png", "progresso_planejamento": 98, "progresso_producao": 20},
        {"id": "25881", "tipo": "rasthor", "imagem": "rasthor.png", "progresso_planejamento": 100, "progresso_producao": 25}
    ]
}

@app.route('/')
def dashboard():
    return render_template('dashboard.html', semanas=planos_por_semana)

if __name__ == '__main__':
    app.run(debug=True)
