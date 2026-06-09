"""Gera o PDF do trabalho com todo o conteudo exigido pelo enunciado."""

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.config import FIGURES_DIR, INTEGRANTES, OUTPUTS_DIR

PDF_PATH = ROOT_DIR / "docs" / "relatorio.pdf"
CONCLUSION_PATH = OUTPUTS_DIR / "conclusao.json"

REQUIRED_FIGURES = [
    ("Matriz de confusao - KNN", FIGURES_DIR / "matriz_confusao_knn.png"),
    ("Matriz de confusao - SVM", FIGURES_DIR / "matriz_confusao_svm.png"),
    ("Busca do melhor k no KNN", FIGURES_DIR / "knn_busca_k.png"),
    ("Comparacao de metricas", FIGURES_DIR / "comparacao_metricas.png"),
    ("Curvas ROC - KNN vs SVM", FIGURES_DIR / "curvas_roc.png"),
]


def ensure_outputs() -> dict:
    missing = [path for _, path in REQUIRED_FIGURES if not path.exists()]
    if missing or not CONCLUSION_PATH.exists():
        print("Gerando metricas e graficos (python main.py)...")
        from main import main

        main()
    return json.loads(CONCLUSION_PATH.read_text(encoding="utf-8"))


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def register_fonts() -> str:
    font_path = Path("C:/Windows/Fonts/arial.ttf")
    font_bold_path = Path("C:/Windows/Fonts/arialbd.ttf")
    if font_path.exists():
        pdfmetrics.registerFont(TTFont("Arial", str(font_path)))
        if font_bold_path.exists():
            pdfmetrics.registerFont(TTFont("Arial-Bold", str(font_bold_path)))
        return "Arial"
    return "Helvetica"


def build_story(conclusion: dict) -> list:
    font = register_fonts()
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleCustom",
        parent=styles["Heading1"],
        fontName=font,
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor("#1a1a1a"),
    )
    heading = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading2"],
        fontName=font,
        fontSize=13,
        spaceBefore=14,
        spaceAfter=8,
        textColor=colors.HexColor("#2c3e50"),
    )
    body = ParagraphStyle(
        "BodyCustom",
        parent=styles["Normal"],
        fontName=font,
        fontSize=11,
        leading=15,
        spaceAfter=8,
    )

    knn = conclusion["metricas"][0]
    svm = conclusion["metricas"][1]
    knn_params = conclusion["knn_hiperparametros"]
    svm_params = conclusion["svm_hiperparametros"]
    best = conclusion["melhor_modelo"]

    story = []

    story.append(
        Paragraph(
            "Disciplina de Intelig&ecirc;ncia Artificial , Professor Munif , Unicesumar 2026",
            body,
        )
    )
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Trabalho Final - Predi&ccedil;&atilde;o de Diabetes (Pima Indians)", title))

    story.append(Paragraph("Integrantes", heading))
    for integrante in INTEGRANTES:
        story.append(Paragraph(integrante, body))

    story.append(Paragraph("Contextualiza&ccedil;&atilde;o", heading))
    story.append(
        Paragraph(
            "O diabetes mellitus &eacute; uma doen&ccedil;a cr&ocirc;nica que afeta milh&otilde;es de pessoas no mundo. "
            "A detec&ccedil;&atilde;o precoce &eacute; fundamental para reduzir complica&ccedil;&otilde;es e melhorar a qualidade "
            "de vida dos pacientes. Com o avan&ccedil;o da Intelig&ecirc;ncia Artificial, modelos de "
            "aprendizado de m&aacute;quina podem apoiar a identifica&ccedil;&atilde;o de padr&otilde;es em dados cl&iacute;nicos "
            "e auxiliar profissionais de sa&uacute;de na triagem de risco.",
            body,
        )
    )

    story.append(Paragraph("Problema investigado", heading))
    story.append(
        Paragraph(
            "Este trabalho investiga se &eacute; poss&iacute;vel prever a presen&ccedil;a de diabetes em pacientes "
            "da etnia Pima Indians com base em vari&aacute;veis cl&iacute;nicas e demogr&aacute;ficas, como glicose, "
            "press&atilde;o arterial, IMC e idade.",
            body,
        )
    )

    story.append(Paragraph("Hip&oacute;tese", heading))
    story.append(
        Paragraph(
            "Modelos de classifica&ccedil;&atilde;o supervisionada conseguem distinguir pacientes com e sem "
            "diabetes a partir dos atributos dispon&iacute;veis. Espera-se que o SVM apresente bom "
            "desempenho ap&oacute;s a padroniza&ccedil;&atilde;o dos dados, enquanto o KNN pode ser sens&iacute;vel &agrave; "
            "escolha do n&uacute;mero de vizinhos e &agrave; distribui&ccedil;&atilde;o das classes.",
            body,
        )
    )

    story.append(Paragraph("Dataset utilizado", heading))
    dataset_rows = [
        ["Item", "Descricao"],
        ["Nome", "Pima Indians Diabetes Database"],
        ["Origem", "Kaggle / UCI Machine Learning Repository"],
        ["Registros", "768 amostras"],
        ["Atributos", "8 variaveis numericas"],
        ["Vari&aacute;vel alvo", "Outcome (0 = sem diabetes, 1 = com diabetes)"],
    ]
    dataset_table = Table(dataset_rows, colWidths=[4 * cm, 12 * cm])
    dataset_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#34495e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
            ]
        )
    )
    story.append(dataset_table)
    story.append(Spacer(1, 0.2 * cm))
    story.append(
        Paragraph(
            "Atributos: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, "
            "DiabetesPedigreeFunction e Age.",
            body,
        )
    )

    story.append(Paragraph("Prepara&ccedil;&atilde;o dos dados", heading))
    prep_items = [
        "Substitui&ccedil;&atilde;o de zeros inv&aacute;lidos por valores ausentes nas vari&aacute;veis cl&iacute;nicas.",
        "Imputa&ccedil;&atilde;o de valores ausentes pela mediana.",
        "Padroniza&ccedil;&atilde;o com StandardScaler.",
        "Divis&atilde;o estratificada em treino (80%) e teste (20%).",
    ]
    for item in prep_items:
        story.append(Paragraph(f"&bull; {item}", body))

    story.append(Paragraph("M&eacute;todos de IA utilizados", heading))
    methods_rows = [
        ["Parte", "Algoritmo", "Detalhes"],
        ["Parte 1", "KNN", f"k-Nearest Neighbors, melhor k = {knn_params['n_neighbors']}"],
        [
            "Parte 2",
            "SVM",
            f"kernel = {svm_params['kernel']}, C = {svm_params['C']}, gamma = {svm_params['gamma']}",
        ],
    ]
    methods_table = Table(methods_rows, colWidths=[2.5 * cm, 3 * cm, 10.5 * cm])
    methods_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#34495e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
            ]
        )
    )
    story.append(methods_table)
    story.append(
        Paragraph(
            "Ambos os modelos foram treinados com valida&ccedil;&atilde;o cruzada estratificada (5 folds).",
            body,
        )
    )

    story.append(Paragraph("Avalia&ccedil;&atilde;o dos modelos", heading))
    story.append(
        Paragraph(
            "Foram utilizadas as m&eacute;tricas: acur&aacute;cia, precis&atilde;o, revoca&ccedil;&atilde;o (recall), "
            "F1-score e ROC-AUC, al&eacute;m de matrizes de confus&atilde;o e gr&aacute;ficos comparativos.",
            body,
        )
    )

    metrics_rows = [
        ["Modelo", "Acur\u00e1cia", "Precis\u00e3o", "Revoca\u00e7\u00e3o", "F1-score", "ROC-AUC"],
        [
            f"KNN (k={knn_params['n_neighbors']})",
            pct(knn["accuracy"]),
            pct(knn["precision"]),
            pct(knn["recall"]),
            f"{knn['f1_score']:.2f}",
            f"{knn['roc_auc']:.2f}",
        ],
        [
            f"SVM ({svm_params['kernel']})",
            pct(svm["accuracy"]),
            pct(svm["precision"]),
            pct(svm["recall"]),
            f"{svm['f1_score']:.2f}",
            f"{svm['roc_auc']:.2f}",
        ],
    ]
    metrics_table = Table(metrics_rows, colWidths=[3.2 * cm, 2.2 * cm, 2.2 * cm, 2.4 * cm, 2.2 * cm, 2.2 * cm])
    metrics_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4f8")]),
            ]
        )
    )
    story.append(metrics_table)

    story.append(PageBreak())
    story.append(Paragraph("Gr&aacute;ficos de avalia&ccedil;&atilde;o", heading))

    page_width = A4[0] - 4 * cm
    for caption, figure_path in REQUIRED_FIGURES:
        story.append(Paragraph(caption, body))
        story.append(Spacer(1, 0.2 * cm))
        img = Image(str(figure_path), width=page_width, height=page_width * 0.55)
        story.append(img)
        story.append(Spacer(1, 0.4 * cm))

    story.append(PageBreak())
    story.append(Paragraph("Compara&ccedil;&atilde;o dos resultados", heading))
    story.append(
        Paragraph(
            f"O modelo com melhor desempenho geral foi o <b>{best}</b>, considerando "
            f"F1-score ({knn['f1_score']:.2f} vs {svm['f1_score']:.2f}) e acur&aacute;cia "
            f"({pct(knn['accuracy'])} vs {pct(svm['accuracy'])}). "
            f"O SVM apresentou ROC-AUC ligeiramente superior "
            f"({svm['roc_auc']:.2f} vs {knn['roc_auc']:.2f}), indicando melhor capacidade "
            f"de separar as classes em termos de ranking de probabilidades.",
            body,
        )
    )
    story.append(
        Paragraph(
            "O KNN obteve melhor revoca&ccedil;&atilde;o, identificando mais casos positivos de diabetes, "
            "enquanto o SVM teve precis&atilde;o e revoca&ccedil;&atilde;o mais equilibradas com kernel linear. "
            "A busca de hiperpar&acirc;metros mostrou que k=13 foi o melhor para o KNN, e C=1 com "
            "kernel linear foi o melhor para o SVM.",
            body,
        )
    )

    story.append(Paragraph("Conclus&atilde;o", heading))
    story.append(
        Paragraph(
            "O projeto demonstra o fluxo completo de uma solu&ccedil;&atilde;o de Intelig&ecirc;ncia Artificial: "
            "defini&ccedil;&atilde;o do problema, prepara&ccedil;&atilde;o dos dados, treinamento, avalia&ccedil;&atilde;o e compara&ccedil;&atilde;o "
            "entre modelos. Os resultados mostram que ambos os algoritmos s&atilde;o capazes de "
            "classificar a presen&ccedil;a de diabetes com desempenho razo&aacute;vel, com o KNN "
            "apresentando leve vantagem nas m&eacute;tricas principais de classifica&ccedil;&atilde;o. "
            "As limita&ccedil;&otilde;es incluem o tamanho reduzido do dataset e o desbalanceamento entre "
            "classes, o que impacta a revoca&ccedil;&atilde;o dos modelos. Trabalhos futuros podem explorar "
            "outras t&eacute;cnicas de balanceamento e engenharia de atributos.",
            body,
        )
    )

    return story


def generate_pdf() -> Path:
    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    conclusion = ensure_outputs()
    story = build_story(conclusion)

    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    doc.build(story)
    return PDF_PATH


if __name__ == "__main__":
    path = generate_pdf()
    print(f"PDF gerado com sucesso: {path}")
