from flask import Flask, render_template, request
from data_processor import DataProcessor

app = Flask(__name__)
data_processor = DataProcessor()

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    # Carrega dados a cada requisição para pegar atualizações
    data_processor.load_data()
    
    semanas = {
        "Semana 1": [],
        "Semana 2": [],
        "Semana 3": [],
        "Semana 4": []
    }

    if request.method == 'POST':
        input_lotes = request.form.get('lotes', '')
        lotes = [l.strip() for l in input_lotes.split(',') if l.strip()][:16]

        for i, plano_id in enumerate(lotes):
            plano_data = data_processor.get_dados_plano(plano_id)
            
            semana = f"Semana {(i // 4) + 1}"
            semanas[semana].append(plano_data)
            
            # Debug detalhado
            print(f"\n📌 Plano {plano_id}:")
            print(f"🔹 Planejamento: {plano_data['progresso_planejamento']}%")
            print(f"   - SOCs: {plano_data['detalhes_planejamento']['total_soc']} "
                  f"({plano_data['detalhes_planejamento']['soc_baixa']} baixa)")
            print(f"   - OCs: {plano_data['detalhes_planejamento']['total_oc']} "
                  f"({plano_data['detalhes_planejamento']['oc_fechadas']} fechadas)")
            print(f"🔹 Produção: {plano_data['progresso_producao']}%")
            print(f"   - OFs: {plano_data['detalhes_producao']['total_of']} "
                  f"({plano_data['detalhes_producao']['of_fechada']} fechadas)")

        # Salva SOC atual como histórico para próxima comparação
        data_processor.save_current_soc_as_history()

    return render_template('dashboard.html', semanas=semanas)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host='0.0.0.0', port=port, debug=False) 
