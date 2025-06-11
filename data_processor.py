import pandas as pd

class DataProcessor:
    def __init__(self):
        self.df_of = None
        self.df_soc = None
        self.df_oc = None
        self.soc_anterior = None  # Para comparar histórico
        
    def load_data(self):
        """Carrega os dados das planilhas"""
        self.df_of = pd.read_excel("data/ofs.xlsx")
        self.df_soc = pd.read_excel("data/soc.xlsx")
        self.df_oc = pd.read_excel("data/OC.xlsx")
        
        # Debug: Verificar colunas disponíveis
        print("\n🔍 Colunas disponíveis:")
        print("OFs:", list(self.df_of.columns))
        print("SOCs:", list(self.df_soc.columns))
        print("OCs:", list(self.df_oc.columns))
    
    def classificar_plano(self, plano):
    
        plano_str = str(plano)

        if len(plano_str) == 5:
            # Classificação por final
            if plano_str.endswith('1'):
                return "plaina", "plaina.png"
            elif plano_str.endswith('4'):
                return "tratador", "tratador.png"
            elif plano_str.endswith('7'):
                return "agco", "agco.png"
            elif plano_str.endswith('8'):
                return "carreta", "carreta.png"
            elif plano_str.endswith('9'):
                return "descompactador", "rasthor.png"
            else:
                return "outro", None

        elif len(plano_str) == 3:
            # Classificação por início
            if plano_str.startswith('6'):
                return "complemento", "complementos.png"
            elif plano_str.startswith('4'):
                return "urgente", "urgente.png"
            elif plano_str.startswith('1'):
                return "assistência", "assistencia.png"
            elif plano_str.startswith('2'):
                return "vendas", "vendas.png"
            elif plano_str.startswith('3'):
                return "engenharia", "engenharia.png"
            else:
                return "outro", None

        else:
            # Caso o plano tenha formato inesperado
            return "outro", None

    
    def verificar_oc_fechada(self, oc_row):
        """Verifica se OC está fechada baseado na coluna Q.Saldo"""
        if 'Q.Saldo' in oc_row.index:
            return oc_row['Q.Saldo'] == 0
        elif 'Q. Recebida' in oc_row.index and 'Q. Prevista' in oc_row.index:
            return oc_row['Q. Recebida'] >= oc_row['Q. Prevista']
        return False
    
    def calcular_soc_baixa(self, plano_id):
        """Calcula quantas SOCs estão em baixa comparando com histórico"""
        if self.soc_anterior is None:
            return 0  # Sem histórico para comparar
            
        # Conta SOCs atuais para o plano
        socs_atual = len(self.df_soc[self.df_soc['Plano'].astype(str) == str(plano_id)])
        
        
    
    def calcular_progresso_planejamento(self, plano_id):
        """
        - 25%: Plano existe na lista de OFs
        - 25%: SOC foi gerada para o plano
        - 25%: OC foi criada para o plano (aberta)
        - 25%: OC foi fechada (Q.Saldo = 0)
        """
        progresso = 0
        detalhes = {
            'plano_existe': False,
            'soc_gerada': False,
            'soc_baixa': 0,
            'total_soc': 0,
            'oc_criada': False,
            'oc_fechada': False,
            'total_oc': 0,
            'oc_fechadas': 0
        }
        
        # 1. Verifica se o plano existe na lista de OFs
        plano_of = self.df_of[self.df_of['Plano'].astype(str) == str(plano_id)]
        if len(plano_of) > 0:
            progresso += 25
            detalhes['plano_existe'] = True
        
        # 2. Verifica SOCs para o plano
        socs_plano = self.df_soc[self.df_soc['Plano'].astype(str) == str(plano_id)]
        if len(socs_plano) > 0:
            progresso += 25
            detalhes['soc_gerada'] = True
            detalhes['total_soc'] = len(socs_plano)
            
            
        
        # 3. Verifica OCs para o plano
        ocs_plano = self.df_oc[self.df_oc['Plano'].astype(str) == str(plano_id)]
        if len(ocs_plano) > 0:
            progresso += 25
            detalhes['oc_criada'] = True
            detalhes['total_oc'] = len(ocs_plano)
            
            # Verifica OCs fechadas (Q.Saldo = 0)
            ocs_fechadas = sum(1 for _, row in ocs_plano.iterrows() if self.verificar_oc_fechada(row))
            detalhes['oc_fechadas'] = ocs_fechadas
            
            if ocs_fechadas > 0:
                progresso += 25
        
        return min(100, progresso), detalhes
    
    def calcular_progresso_producao(self, plano_id):
        """Calcula progresso da produção baseado em OFs fechadas"""
        ofs_plano = self.df_of[self.df_of['Plano'].astype(str) == str(plano_id)]
        
        if len(ofs_plano) == 0:
            return 0, {'total_of': 0, 'of_fechada': 0}
        
        # Verifica OFs fechadas (Produzido >= Programado)
        ofs_fechadas = sum(
            1 for _, row in ofs_plano.iterrows() 
            if row['Produzido'] >= row['Programado']
        )
        
        progresso = (ofs_fechadas / len(ofs_plano)) * 100
        detalhes = {
            'total_of': len(ofs_plano),
            'of_fechada': ofs_fechadas
        }
        
        return round(progresso, 1), detalhes
    
    def save_current_soc_as_history(self):
        """Salva a SOC atual como histórico para próxima comparação"""
        if self.df_soc is not None:
            self.df_soc.to_excel("data/soc_anterior.xlsx", index=False)
    
    def get_dados_plano(self, plano_id):
        """Obtém todos os dados consolidados para um plano"""
        tipo, imagem = self.classificar_plano(plano_id)
        progresso_planejamento, detalhes_planejamento = self.calcular_progresso_planejamento(plano_id)
        progresso_producao, detalhes_producao = self.calcular_progresso_producao(plano_id)
        
        return {
            "id": plano_id,
            "tipo": tipo,
            "imagem": imagem,
            "progresso_planejamento": progresso_planejamento,
            "progresso_producao": progresso_producao,
            "detalhes_planejamento": detalhes_planejamento,
            "detalhes_producao": detalhes_producao
        }
