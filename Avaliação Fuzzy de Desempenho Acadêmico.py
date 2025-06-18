import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# --- Definição das variáveis fuzzy ---

# Entradas
notas = ctrl.Antecedent(np.arange(0, 11, 1), 'notas')
participacao = ctrl.Antecedent(np.arange(0, 11, 1), 'participacao')
projetos = ctrl.Antecedent(np.arange(0, 11, 1), 'projetos')

# Saída
desempenho = ctrl.Consequent(np.arange(0, 101, 1), 'desempenho')

# Funções de pertinência

# Notas
notas['baixa'] = fuzz.trapmf(notas.universe, [0, 0, 2.5, 5])
notas['media'] = fuzz.trimf(notas.universe, [2.5, 5, 7.5])
notas['alta'] = fuzz.trapmf(notas.universe, [5, 7.5, 10, 10])

# Participação
participacao['baixa'] = fuzz.trapmf(participacao.universe, [0, 0, 2, 4])
participacao['media'] = fuzz.trimf(participacao.universe, [2, 5, 8])
participacao['alta'] = fuzz.trapmf(participacao.universe, [6, 8, 10, 10])

# Projetos
projetos['simples'] = fuzz.trapmf(projetos.universe, [0, 0, 2, 5])
projetos['medio'] = fuzz.trimf(projetos.universe, [2, 5, 8])
projetos['complexo'] = fuzz.trapmf(projetos.universe, [5, 8, 10, 10])

# Desempenho
desempenho['insuficiente'] = fuzz.trapmf(desempenho.universe, [0, 0, 20, 40])
desempenho['regular'] = fuzz.trimf(desempenho.universe, [20, 45, 70])
desempenho['bom'] = fuzz.trimf(desempenho.universe, [55, 75, 95])
desempenho['excelente'] = fuzz.trapmf(desempenho.universe, [80, 95, 100, 100])

# --- Regras Fuzzy ---
regras = [
    ctrl.Rule(notas['baixa'] & participacao['baixa'], desempenho['insuficiente']),
    ctrl.Rule(notas['media'] & participacao['media'] & projetos['medio'], desempenho['regular']),
    ctrl.Rule(notas['alta'] & participacao['alta'] & projetos['complexo'], desempenho['excelente']),
    ctrl.Rule(notas['alta'] | participacao['alta'], desempenho['bom']),
    ctrl.Rule(projetos['complexo'], desempenho['bom']),
    ctrl.Rule(notas['baixa'] & projetos['simples'], desempenho['insuficiente']),
    ctrl.Rule(notas['media'] & participacao['alta'], desempenho['bom']),
    ctrl.Rule(notas['alta'] & participacao['baixa'], desempenho['regular']),
]

# Sistema e simulação
sistema_ctrl = ctrl.ControlSystem(regras)
simulador = ctrl.ControlSystemSimulation(sistema_ctrl)

# --- Função de entrada ---
def obter_entrada_usuario(prompt, minimo=0, maximo=10):
    while True:
        try:
            valor = float(input(prompt).replace(',', '.'))
            if minimo <= valor <= maximo:
                return valor
            else:
                print(f"Insira um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida, use apenas números.")
        except EOFError:
            print("Entrada cancelada.")
            return None

# --- Classificador do desempenho ---
def classificar_desempenho(valor):
    if valor < 40:
        return "insuficiente"
    elif valor < 70:
        return "regular"
    elif valor < 90:
        return "bom"
    else:
        return "excelente"

# --- Entrada do usuário ---
print("\n--- Avaliação Fuzzy de Desempenho Acadêmico ---")

nota = obter_entrada_usuario("Nota (0 a 10): ")
if nota is None: exit()

print("\nParticipação (0 a 10):")
print("  0 a 4   → baixa")
print("  4 a 7   → média")
print("  7 a 10  → alta")
part = obter_entrada_usuario("Digite o nível de participação: ")
if part is None: exit()

print("\nProjetos (0 a 10):")
print("  0 a 4   → simples")
print("  4 a 7   → médio")
print("  7 a 10  → complexo")
proj = obter_entrada_usuario("Digite a qualidade/complexidade dos projetos: ")
if proj is None: exit()

# --- Simulação ---
simulador.input["notas"] = nota
simulador.input["participacao"] = part
simulador.input["projetos"] = proj

try:
    simulador.compute()
    resultado = simulador.output["desempenho"]
    classificacao = classificar_desempenho(resultado)

    print(f"\nDesempenho calculado: {resultado:.2f} (em uma escala de 0 a 100)")
    print(f"Classificação: {classificacao}")

    # Níveis de avaliação
    print("\n--- Níveis de Avaliação ---")
    print("  0 a 39   → Insuficiente")
    print(" 40 a 69   → Regular")
    print(" 70 a 89   → Bom")
    print(" 90 a 100  → Excelente")

except ValueError as e:
    print("\nErro ao calcular o desempenho:", e)
