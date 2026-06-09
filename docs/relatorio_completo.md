Disciplina de Inteligência Artificial , Professor Munif , Unicesumar 2026

# Trabalho Final - Predição de Diabetes (Pima Indians)

## Integrantes

- Pedro Henrique da Silva - RA: 23021607-2
- Victor Hugo Rodrigues de Oliveira - RA: 23418156-2
- Victor Hungo Silva Garcia - RA: 23030968-2

---

## Contextualização

O diabetes mellitus é uma doença crônica que afeta milhões de pessoas no mundo. A detecção precoce é fundamental para reduzir complicações e melhorar a qualidade de vida dos pacientes. Com o avanço da Inteligência Artificial, modelos de aprendizado de máquina podem apoiar a identificação de padrões em dados clínicos e auxiliar profissionais de saúde na triagem de risco.

## Problema investigado

Este trabalho investiga se é possível prever a presença de diabetes em pacientes da etnia Pima Indians com base em variáveis clínicas e demográficas, como glicose, pressão arterial, IMC e idade.

## Hipótese

Modelos de classificação supervisionada conseguem distinguir pacientes com e sem diabetes a partir dos atributos disponíveis. Espera-se que o SVM apresente bom desempenho após a padronização dos dados, enquanto o KNN pode ser sensível à escolha do número de vizinhos e à distribuição das classes.

## Dataset utilizado

| Item | Descrição |
|------|-----------|
| Nome | Pima Indians Diabetes Database |
| Origem | [Kaggle - UCI ML Repository](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database) |
| Registros | 768 amostras |
| Atributos | 8 variáveis numéricas |
| Variável alvo | Outcome (0 = sem diabetes, 1 = com diabetes) |

**Atributos principais:**

- Pregnancies: número de gestações
- Glucose: concentração de glicose no plasma
- BloodPressure: pressão arterial diastólica (mm Hg)
- SkinThickness: espessura da dobra cutânea do tríceps (mm)
- Insulin: insulina sérica (mu U/ml)
- BMI: índice de massa corporal
- DiabetesPedigreeFunction: função de pedigree diabético
- Age: idade em anos

## Preparação dos dados

1. Substituição de zeros inválidos por valores ausentes nas variáveis clínicas.
2. Imputação de valores ausentes pela mediana.
3. Padronização com StandardScaler.
4. Divisão estratificada em treino (80%) e teste (20%).

## Métodos de IA utilizados

| Parte da disciplina | Algoritmo | Detalhes |
|---------------------|-----------|----------|
| Parte 1 | KNN (k-Nearest Neighbors) | Melhor k = 13 |
| Parte 2 | SVM (Support Vector Machine) | kernel linear, C = 1, gamma = scale |

Ambos os modelos foram treinados com validação cruzada estratificada (5 folds).

## Avaliação dos modelos

Métricas utilizadas: acurácia, precisão, revocação (recall), F1-score e ROC-AUC.

| Modelo | Acurácia | Precisão | Revocação | F1-score | ROC-AUC |
|--------|----------|----------|-----------|----------|---------|
| KNN (k=13) | 71,4% | 60,9% | 51,9% | 0,56 | 0,79 |
| SVM (linear) | 70,1% | 59,1% | 48,1% | 0,53 | 0,81 |

### Gráficos

Insira aqui as imagens de `outputs/figures/`:

1. matriz_confusao_knn.png
2. matriz_confusao_svm.png
3. knn_busca_k.png
4. comparacao_metricas.png
5. curvas_roc.png

## Comparação dos resultados

O modelo com melhor desempenho geral foi o **KNN**, considerando F1-score (0,56 vs 0,53) e acurácia (71,4% vs 70,1%). O SVM apresentou ROC-AUC ligeiramente superior (0,81 vs 0,79), indicando melhor capacidade de separar as classes em termos de ranking de probabilidades.

O KNN obteve melhor revocação, identificando mais casos positivos de diabetes, enquanto o SVM teve precisão e revocação mais equilibradas com kernel linear. A busca de hiperparâmetros mostrou que k=13 foi o melhor para o KNN, e C=1 com kernel linear foi o melhor para o SVM.

## Conclusão

O projeto demonstra o fluxo completo de uma solução de Inteligência Artificial: definição do problema, preparação dos dados, treinamento, avaliação e comparação entre modelos. Os resultados mostram que ambos os algoritmos são capazes de classificar a presença de diabetes com desempenho razoável, com o KNN apresentando leve vantagem nas métricas principais de classificação.

As limitações incluem o tamanho reduzido do dataset e o desbalanceamento entre classes, o que impacta a revocação dos modelos. Trabalhos futuros podem explorar outras técnicas de balanceamento e engenharia de atributos.
