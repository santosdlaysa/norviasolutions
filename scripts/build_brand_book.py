from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'output', 'pdf')
os.makedirs(OUT, exist_ok=True)
PDF = os.path.join(OUT, 'Norvia_Solutions_Brand_Book_Completo_v1.0.pdf')
REFERENCE = os.path.join(ROOT, 'public', 'ceb2e993-1cdb-4053-a3f4-0d4cc834d3e6.png')

INK = HexColor('#0F1D18')
PANEL = HexColor('#15251E')
PANEL2 = HexColor('#1A2C24')
BONE = HexColor('#EDEBE3')
MUTED = HexColor('#9A9A9B')
LINE = HexColor('#7D9B80')
GREEN = HexColor('#7FCB8F')
LIME = HexColor('#B5D978')
GOLD = HexColor('#F0D179')
BLUE = HexColor('#8FB8E8')
PINK = HexColor('#F2A0B6')
PURPLE = HexColor('#B9A7E6')

pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', r'C:\Windows\Fonts\arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Consolas', r'C:\Windows\Fonts\consola.ttf'))
pdfmetrics.registerFont(TTFont('Consolas-Bold', r'C:\Windows\Fonts\consolab.ttf'))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle('Kicker', fontName='Consolas', fontSize=7.5, leading=10, textColor=LIME, tracking=1.2, spaceAfter=8))
styles.add(ParagraphStyle('CoverTitle', fontName='Arial-Bold', fontSize=34, leading=37, textColor=BONE, spaceAfter=12))
styles.add(ParagraphStyle('H1N', fontName='Arial-Bold', fontSize=24, leading=28, textColor=BONE, spaceAfter=13))
styles.add(ParagraphStyle('H2N', fontName='Arial-Bold', fontSize=14, leading=18, textColor=LIME, spaceBefore=9, spaceAfter=7))
styles.add(ParagraphStyle('BodyN', fontName='Arial', fontSize=10.2, leading=16, textColor=BONE, spaceAfter=8))
styles.add(ParagraphStyle('SmallN', fontName='Arial', fontSize=8.2, leading=12, textColor=MUTED, spaceAfter=5))
styles.add(ParagraphStyle('MonoN', fontName='Consolas', fontSize=8.2, leading=12, textColor=LIME, spaceAfter=4))
styles.add(ParagraphStyle('QuoteN', fontName='Arial-Bold', fontSize=17, leading=23, textColor=BONE, spaceBefore=12, spaceAfter=14))
styles.add(ParagraphStyle('TableN', fontName='Arial', fontSize=8.3, leading=11, textColor=BONE))
styles.add(ParagraphStyle('TableHead', fontName='Arial-Bold', fontSize=8.3, leading=11, textColor=INK))

def P(text, style='BodyN'):
    return Paragraph(text, styles[style])

def cell(text, style='TableN'):
    return P(text, style)

def page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(INK)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setStrokeColor(colors.Color(0.45, 0.65, 0.5, alpha=0.28))
    canvas.setLineWidth(0.35)
    canvas.rect(8*mm, 8*mm, A4[0]-16*mm, A4[1]-16*mm, fill=0, stroke=1)
    if doc.page > 1:
        canvas.setFont('Consolas', 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(17*mm, 13*mm, 'NORVIA SOLUTIONS  /  BRAND BOOK 1.0')
        canvas.drawRightString(A4[0]-17*mm, 13*mm, f'{doc.page:02d}')
    canvas.restoreState()

def cover_bg(canvas, doc):
    page_bg(canvas, doc)
    canvas.saveState()
    canvas.setFillColor(PANEL)
    canvas.circle(165*mm, 245*mm, 75*mm, fill=1, stroke=0)
    canvas.setStrokeColor(GREEN)
    canvas.setLineWidth(1)
    canvas.line(25*mm, 54*mm, 185*mm, 54*mm)
    canvas.setFont('Consolas', 8)
    canvas.setFillColor(LIME)
    canvas.drawString(25*mm, 42*mm, 'ESTUDIO DE SOFTWARE  //  v1.0')
    canvas.restoreState()

class Book(BaseDocTemplate):
    def __init__(self, filename):
        BaseDocTemplate.__init__(self, filename, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=22*mm, bottomMargin=21*mm)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='normal')
        self.addPageTemplates([PageTemplate(id='normal', frames=frame, onPage=page_bg), PageTemplate(id='cover', frames=frame, onPage=cover_bg)])

def section(title, kicker, intro, blocks):
    story = [P(kicker, 'Kicker'), P(title, 'H1N'), P(intro, 'BodyN'), Spacer(1, 5)]
    for heading, text in blocks:
        story += [P(heading, 'H2N'), P(text, 'BodyN')]
    return story

def card_grid(items, cols=2):
    rows = []
    for i in range(0, len(items), cols):
        row = []
        for title, text, color in items[i:i+cols]:
            row.append([P(title, 'H2N'), P(text, 'SmallN')])
        while len(row) < cols: row.append('')
        rows.append(row)
    t = Table(rows, colWidths=[(A4[0]-50*mm)/cols]*cols, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PANEL), ('BOX', (0,0), (-1,-1), .4, LINE),
        ('INNERGRID', (0,0), (-1,-1), .35, HexColor('#385344')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10), ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

def table(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIME), ('TEXTCOLOR', (0,0), (-1,0), INK),
        ('BACKGROUND', (0,1), (-1,-1), PANEL), ('GRID', (0,0), (-1,-1), .35, HexColor('#48684E')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8), ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    return t

story = []
# Cover
story.append(P('NORVIA', 'CoverTitle'))
story.append(P('SOLUTIONS', 'H1N'))
story.append(Spacer(1, 17*mm))
story.append(P('BRAND BOOK', 'Kicker'))
story.append(P('Sistema completo de marca', 'QuoteN'))
story.append(P('Estratégia, identidade visual, sistema de produto, design system e aplicações.', 'BodyN'))
story.append(Spacer(1, 65*mm))
story.append(P('Versão 1.0  |  Julho de 2026', 'SmallN'))
story.append(PageBreak())

# Contents
story += [P('NAVEGAÇÃO', 'Kicker'), P('Índice', 'H1N'), P('Um sistema para manter a Norvia reconhecível em cada ponto de contato.', 'BodyN')]
contents = [('01', 'Estratégia da marca', 'Fundamentos, posicionamento, público e linguagem.'), ('02', 'Sistema de identidade', 'Logo, monograma, grid, versões e regras.'), ('03', 'Sistema visual', 'Cores, tipografia, ícones, ilustrações e motion.'), ('04', 'Design system', 'Componentes, layouts e princípios de interface.'), ('05', 'Produtos', 'Como cada produto ganha personalidade.'), ('06', 'Aplicações', 'Canais digitais, papelaria e ambientes.'), ('07', 'Manual completo', 'Checklist, governança e arquivos finais.')]
story.append(table([[cell('PARTE', 'TableHead'), cell('CONTEÚDO', 'TableHead'), cell('ESCOPO', 'TableHead')]] + [[cell(a), cell(b), cell(c)] for a,b,c in contents], [16*mm, 52*mm, 92*mm]))
story.append(Spacer(1, 12))
story.append(P('Como usar este livro', 'H2N'))
story.append(P('Este documento é a fonte de verdade da marca Norvia Solutions. Ele orienta decisões de design, comunicação, produto e apresentação comercial. Quando uma aplicação não estiver descrita, preserve os princípios: clareza, precisão, contraste, respiro e consistência.', 'BodyN'))
story.append(PageBreak())

# Part 1
story += section('Estratégia da marca', 'PARTE 01  /  FUNDAMENTOS', 'A Norvia existe para transformar complexidade em produtos digitais claros, confiáveis e preparados para evoluir.', [
('História', 'A Norvia Solutions nasceu com o propósito de transformar problemas complexos em soluções digitais elegantes. A empresa atua no desenvolvimento de software sob medida, plataformas SaaS, aplicativos móveis, automações, inteligência artificial e sistemas corporativos de alta performance. Mais do que executar demandas, a Norvia trabalha como parceira tecnológica: entende o contexto, estrutura a solução e constrói um produto que pode evoluir.'),
('Manifesto', 'Acreditamos que tecnologia é uma ferramenta para ampliar o potencial humano. Não desenvolvemos sistemas apenas para automatizar tarefas. Construímos plataformas que ajudam empresas a crescer, tomar decisões melhores e criar novas oportunidades. Cada linha de código deve ter um propósito. Cada interface deve ser simples. Cada detalhe deve transmitir confiança. Criamos tecnologia que acompanha a evolução dos nossos clientes.'),
('Propósito', 'Transformar ideias em produtos digitais que geram valor real.'),
('Missão', 'Projetar e desenvolver soluções digitais modernas, escaláveis e inteligentes que impulsionem o crescimento de empresas e empreendedores.'),
('Visão', 'Ser reconhecida como uma das principais software houses do Brasil, referência em inovação, qualidade técnica e experiência do usuário.'),
])
story.append(PageBreak())
story += [P('VALORES', 'Kicker'), P('O que nunca negociamos', 'H1N'), P('Valores são critérios de decisão. Eles aparecem no código, no atendimento, na interface e na forma de crescer.', 'BodyN')]
story.append(card_grid([
('Engenharia acima da complexidade', 'Soluções simples são melhores que soluções complicadas. Complexidade deve ser justificada, isolada e administrada.', GREEN),
('Transparência', 'Comunicação clara. Processos claros. Tecnologia clara. O cliente entende o que está sendo construído e por quê.', GREEN),
('Evolução contínua', 'Sempre melhorar, nunca acomodar. Cada entrega é uma base mais forte para a próxima.', GREEN),
('Performance', 'Software deve ser rápido, leve e escalável. Desempenho é parte da experiência, não um detalhe posterior.', GREEN),
('Qualidade', 'Código limpo, arquitetura sólida, documentação e testes formam a confiança que sustenta o produto.', GREEN),
('Inovação', 'Experimentar, pesquisar e criar com propósito. Inovação é resolver melhor, não apenas usar o novo.', GREEN),
('Parceria', 'Não somos apenas fornecedores. Somos parceiros tecnológicos responsáveis pelo resultado compartilhado.', GREEN),
('Responsabilidade', 'Tecnologia deve respeitar pessoas, dados, contexto e impacto. Toda decisão técnica tem uma consequência.', GREEN),
], 2))
story.append(PageBreak())
story += [P('ARQUÉTIPOS E PERSONALIDADE', 'Kicker'), P('A marca combina criação e conhecimento: imagina possibilidades e tem domínio para torná-las reais.', 'BodyN')]
story.append(card_grid([('O Criador', 'Arquétipo principal. A Norvia existe para construir, inventar, desenvolver e dar forma a ideias. Busca originalidade com função.', GREEN), ('O Sábio', 'Arquétipo secundário. Conhecimento, precisão, método e estratégia orientam cada escolha técnica.', LIME)], 2))
story.append(Spacer(1, 12))
story += [P('Se a Norvia fosse uma pessoa', 'H2N'), P('Inteligente. Elegante. Moderna. Objetiva. Confiável. Criativa. Técnica. Minimalista. Ela fala com segurança, mas não precisa provar que sabe tudo. Explica o complexo sem diminuir o interlocutor e transforma decisões técnicas em clareza de negócio.', 'BodyN'), P('Tom de voz', 'H2N'), P('Claro, humano, técnico e elegante. Nunca exagerado, informal demais ou cheio de buzzwords. A Norvia prefere evidências a promessas, frases precisas a adjetivos vazios e orientação prática a discurso genérico.', 'BodyN')]
story.append(table([[cell('EVITAR', 'TableHead'), cell('PREFERIR', 'TableHead')], [cell('Nós revolucionamos completamente seu negócio.', 'TableN'), cell('Desenvolvemos soluções digitais escaláveis para acelerar a evolução do seu negócio.', 'TableN')], [cell('Tecnologia de ponta para resultados incríveis.', 'TableN'), cell('Arquitetura sólida, interfaces claras e métricas que mostram o avanço.', 'TableN')]], [75*mm, 85*mm]))
story.append(PageBreak())
story += [P('PÚBLICO E POSICIONAMENTO', 'Kicker'), P('A Norvia atende organizações que precisam de tecnologia sob medida e querem construir uma vantagem que permaneça.', 'BodyN')]
story.append(card_grid([('Agronegócio', 'Operação, dados, rastreabilidade e eficiência no campo e na gestão.', GREEN), ('Restaurantes', 'Pedidos, operação, fidelização e visão de negócio em tempo real.', GOLD), ('Clínicas e saúde', 'Fluxos confiáveis, experiência do paciente e cuidado com dados.', PINK), ('Indústria e energia', 'Integração, monitoramento, automação e decisões baseadas em dados.', BLUE), ('Startups', 'MVPs, plataformas e arquitetura preparada para aprender e escalar.', PURPLE), ('Logística e comércio', 'Orquestração de processos, visibilidade e redução de atrito.', LIME)], 2))
story.append(Spacer(1, 10))
story += [P('Posicionamento', 'H2N'), P('A Norvia Solutions não compete pelo menor preço. Compete por qualidade, arquitetura, escalabilidade, experiência do usuário e confiança. Entrega soluções que permanecem relevantes por muitos anos e acompanham o crescimento dos clientes.', 'BodyN'), P('Slogans', 'H2N'), P('Building Digital Excellence  |  Engineering the Future  |  Software that moves business  |  Code. Design. Innovation.  |  Transformando ideias em soluções inteligentes.', 'BodyN')]
story.append(PageBreak())

# Part 2
story += section('Sistema de identidade', 'PARTE 02  /  MARCA', 'A identidade Norvia é construída sobre dois sinais: a estrutura do código e a abertura para novas possibilidades.', [
('Conceito 1 - Módulo e núcleo', 'O monograma entre chaves representa um sistema organizado. O ponto verde é o núcleo: uma ideia, um dado, uma decisão ou uma pessoa no centro da tecnologia.'),
('Conceito 2 - Linha de código e topografia', 'A letra N surge como um caminho técnico. A linha indica precisão e continuidade; a topografia adiciona profundidade e conexão com contextos reais.'),
('Conceito 3 - Portal de vetores', 'O N modular funciona como passagem: um portal entre problema e solução, conceito e produto, negócio e tecnologia.'),
('Escolha recomendada', 'O sistema principal deve usar o monograma entre chaves como assinatura institucional. O N de vetores funciona como símbolo de apoio para favicon, avatar, selo de produto e contextos pequenos.'),
])
if os.path.exists(REFERENCE):
    story.append(Image(REFERENCE, width=168*mm, height=95*mm))
    story.append(P('Painel de referência visual aprovado para a direção da marca.', 'SmallN'))
story.append(PageBreak())
story += [P('CONSTRUÇÃO', 'Kicker'), P('A marca deve parecer construída, não decorada. O grid organiza proporção, respiro e repetição.', 'BodyN')]
story.append(card_grid([('Unidade x', 'Use a espessura do traço principal como unidade. Espaços internos mínimos devem respeitar 2x.', GREEN), ('Núcleo', 'O ponto deve permanecer opticamente centralizado no monograma e nunca competir com as chaves.', GREEN), ('Proporção', 'O símbolo isolado pode ser usado em proporção 1:1. A assinatura horizontal usa símbolo + separador + wordmark.', GREEN), ('Área de proteção', 'Reserve no mínimo 1x ao redor de toda a marca. Em aplicações críticas, prefira 2x.', GREEN), ('Tamanho mínimo', 'Impressão: 18 mm de largura na assinatura. Tela: 120 px. Símbolo: 16 px apenas em contextos controlados.', GREEN), ('Alinhamento', 'A linha de base do wordmark e a altura óptica do símbolo devem formar um conjunto estável.', GREEN)], 2))
story.append(PageBreak())
story += [P('VERSÕES DA MARCA', 'Kicker'), P('A marca se adapta ao contexto sem perder sua assinatura.', 'BodyN')]
story.append(table([[cell('VERSÃO', 'TableHead'), cell('USO', 'TableHead'), cell('REGRAS', 'TableHead')], [cell('Principal'), cell('Apresentações, propostas, site, documentos e fachadas.'), cell('Símbolo marfim, wordmark marfim, SOLUTIONS em verde. Fundo escuro preferencial.')], [cell('Secundária'), cell('Cards, assinaturas, materiais compactos e redes.'), cell('Assinatura horizontal com redução de espaçamento controlada.')], [cell('Monograma'), cell('Favicon, avatar, app icon, selo e espaços quadrados.'), cell('Usar com área de proteção. Não adicionar texto ilegível em tamanhos pequenos.')], [cell('Portal de vetores'), cell('Produto, tecnologia, campanha e aplicações premium.'), cell('Usar como símbolo auxiliar, nunca substituir a marca institucional sem contexto.')]], [32*mm, 54*mm, 74*mm]))
story.append(Spacer(1, 14))
story += [P('Uso correto', 'H2N'), P('Contraste suficiente; respiro preservado; cores oficiais; proporções intactas; aplicação coerente com o contexto.', 'BodyN'), P('Uso incorreto', 'H2N'), P('Não esticar, inclinar, contornar, aplicar sombra pesada, alterar cores sem função, remover o núcleo ou sobrepor a fundos com ruído.', 'BodyN')]
story.append(PageBreak())

# Part 3
story += section('Sistema visual', 'PARTE 03  /  LINGUAGEM', 'O sistema visual equilibra profundidade tecnológica e calor humano. O escuro dá foco; o verde sinaliza vida, avanço e inteligência.', [
('Paleta base', 'Ink #0F1D18; Panel #15251E; Panel 2 #1A2C24; Bone #EDEBE3; Muted #9A9A9B; Line rgba(237,235,227,0.13).'),
('Paleta de acentos', 'Campo #7FCB8F; Café #CF9662; Rosa #F2A0B6; Lilás #B9A7E6; Céu #8FB8E8; Sol #F0D179.'),
('Regra de uso', 'A base deve ocupar a maior área. Acentos servem para identificar produto, estado, ação ou caminho. Não use todos os acentos na mesma composição sem uma hierarquia explícita.'),
])
story.append(table([[cell('TOKEN', 'TableHead'), cell('HEX', 'TableHead'), cell('FUNÇÃO', 'TableHead')], [cell('--ink'), cell('#0F1D18'), cell('Fundo principal, contraste e profundidade.')], [cell('--panel'), cell('#15251E'), cell('Superfícies, cards e navegação.')], [cell('--bone'), cell('#EDEBE3'), cell('Texto principal e marca.')], [cell('--campo'), cell('#7FCB8F'), cell('Produto Agronet, sucesso e natureza.')], [cell('--sol'), cell('#F0D179'), cell('Produto Doce Preço, destaque e ação.')], [cell('--ceu'), cell('#8FB8E8'), cell('Produto DAEX, cloud e dados.')]], [38*mm, 30*mm, 92*mm]))
story.append(PageBreak())
story += [P('TIPOGRAFIA', 'Kicker'), P('A tipografia combina uma voz editorial limpa com uma camada monoespaçada que lembra código e documentação.', 'BodyN')]
story.append(card_grid([('Archivo', 'Tipografia principal. Use em títulos, textos, navegação e apresentações. Preferência por peso regular e semibold.', GREEN), ('Spline Sans Mono', 'Tipografia de detalhe. Use em labels, metadados, números, tags, versões e expressões técnicas.', LIME)], 2))
story.append(Spacer(1, 15))
story.append(P('HIERARQUIA RECOMENDADA', 'Kicker'))
story.append(table([[cell('NÍVEL', 'TableHead'), cell('TAMANHO', 'TableHead'), cell('USO', 'TableHead')], [cell('Display'), cell('40-56 px'), cell('Capa, hero, afirmações curtas.')], [cell('H1'), cell('28-36 px'), cell('Título de seção e página.')], [cell('H2'), cell('18-24 px'), cell('Subseção, card principal.')], [cell('Body'), cell('16-18 px'), cell('Texto corrido e explicações.')], [cell('Mono'), cell('11-13 px'), cell('Labels, tokens, navegação técnica.')]], [35*mm, 35*mm, 90*mm]))
story.append(PageBreak())
story += [P('ÍCONE, ILUSTRAÇÃO E MOTION', 'Kicker'), P('A linguagem visual deve ser funcional antes de ser ornamental.', 'BodyN')]
story.append(card_grid([('Ícones', 'Traço fino, cantos suaves, terminais abertos quando possível. Use a mesma espessura e uma geometria simples.', GREEN), ('Ilustrações', 'Prefira diagramas, fluxos, topografias e módulos. Evite imagens genéricas de tecnologia.', GREEN), ('Gradientes', 'Use gradientes discretos entre verde e azul, ou verde e dourado, para estados de evolução.', GOLD), ('Sombras', 'Sombras profundas e suaves, com baixa opacidade. A superfície deve parecer física, não brilhante.', GREEN), ('Motion', 'Movimentos curtos, precisos e com finalidade: entrada, confirmação, transição e feedback.', BLUE), ('Textura', 'Linhas topográficas e grids devem ficar em baixa opacidade, funcionando como camada de profundidade.', PURPLE)], 2))
story.append(PageBreak())

# Part 4
story += section('Design system', 'PARTE 04  /  PRODUTO DIGITAL', 'O design system transforma a marca em decisões reutilizáveis para produtos, sites e ferramentas internas.', [
('Princípio 1 - Clareza antes de ornamentação', 'Todo componente deve responder rapidamente: o que é, o que posso fazer e o que aconteceu.'),
('Princípio 2 - Estado sempre visível', 'Carregando, sucesso, alerta, erro e vazio precisam ter linguagem, cor e ação claras.'),
('Princípio 3 - Densidade com respiro', 'Informação operacional pode ser densa, mas nunca deve perder alinhamento, contraste e agrupamento.'),
('Princípio 4 - Acessibilidade', 'Contraste, foco, tamanho de toque, navegação por teclado e leitura em telas pequenas são requisitos.'),
])
story.append(table([[cell('COMPONENTE', 'TableHead'), cell('ESTILO', 'TableHead'), cell('COMPORTAMENTO', 'TableHead')], [cell('Botão primário'), cell('Fundo verde, texto ink, raio 8 px.'), cell('Ação principal única por área; hover clareia; foco tem anel visível.')], [cell('Botão secundário'), cell('Transparente, linha muted, texto bone.'), cell('Ação alternativa; nunca competir visualmente com o primário.')], [cell('Card'), cell('Panel, borda discreta, raio 12 px.'), cell('Agrupa uma ideia; pode receber acento por produto.')], [cell('Input'), cell('Panel 2, linha line, placeholder muted.'), cell('Label sempre visível; erro explica como corrigir.')], [cell('Badge'), cell('Pílula compacta, cor semântica.'), cell('Usar para estado, categoria ou contexto, não para parágrafo.')]], [35*mm, 58*mm, 67*mm]))
story.append(PageBreak())
story += [P('LAYOUTS DE REFERÊNCIA', 'Kicker'), P('A marca deve funcionar em diferentes escalas, do dashboard à landing page.', 'BodyN')]
story.append(card_grid([('Dashboard', 'Navegação lateral escura, header leve, métricas agrupadas e um único acento dominante por contexto.', GREEN), ('Landing page', 'Hero com promessa clara, prova de valor, módulos de solução, casos e chamada para conversa.', GREEN), ('Navbar', 'Marca à esquerda, navegação curta ao centro e ação principal à direita. Evite menus superlotados.', GREEN), ('Footer', 'Assinatura, links essenciais, contato e versão. O rodapé é uma confirmação de confiança.', GREEN), ('Mobile', 'Priorizar leitura, ação e contexto. Cards empilham; tabelas viram blocos; navegação reduz.', GREEN), ('Empty state', 'Explique o estado, o próximo passo e a razão. Vazio não deve parecer erro.', GREEN)], 2))
story.append(PageBreak())

# Part 5
story += section('Produtos', 'PARTE 05  /  PORTFÓLIO', 'Cada produto pode ter sua própria cor e personalidade sem deixar de parecer parte do ecossistema Norvia.', [
('Arquitetura de marca', 'A Norvia é a marca-mãe. O produto ganha nome, cor de acento, ícone funcional e linguagem contextual. A assinatura deve aparecer em ambientes institucionais e de confiança.'),
('Regra de diferenciação', 'Produto diferencia por cor e vocabulário; Norvia unifica por base escura, tipografia, grid, espaçamento, comportamento e qualidade de interface.'),
('Experiência compartilhada', 'Login, navegação, mensagens de erro, suporte, documentação e rodapé devem transmitir o mesmo sistema.'),
])
story.append(table([[cell('PRODUTO', 'TableHead'), cell('ACENTO', 'TableHead'), cell('PERSONALIDADE', 'TableHead'), cell('PROMESSA', 'TableHead')], [cell('Agronet'), cell('#7FCB8F'), cell('Natural, operacional, inteligente'), cell('Conectar informação e decisão no campo.')], [cell('CafeControll'), cell('#CF9662'), cell('Acolhedor, preciso, ágil'), cell('Organizar a operação para servir melhor.')], [cell('Organiza Ela'), cell('#F2A0B6'), cell('Humano, cuidadoso, claro'), cell('Transformar rotina em leveza.')], [cell('Doce Preço'), cell('#F0D179'), cell('Direto, comercial, otimista'), cell('Dar clareza para preço e margem.')], [cell('Lumera Fest'), cell('#B9A7E6'), cell('Criativo, vibrante, social'), cell('Fazer experiências acontecerem.')], [cell('DAEX'), cell('#8FB8E8'), cell('Técnico, conectado, confiável'), cell('Tornar dados acionáveis.')]], [32*mm, 25*mm, 50*mm, 53*mm]))
story.append(PageBreak())

# Part 6
story += section('Aplicações', 'PARTE 06  /  PONTOS DE CONTATO', 'A identidade ganha valor quando é reconhecível no mundo real: na tela, no papel, na roupa e no espaço.', [
('Instagram', 'Avatar com monograma. Feed com fundo ink, títulos curtos e acento por tema. Carrosséis usam módulos, linhas e números para explicar tecnologia sem parecer aula genérica.'),
('LinkedIn', 'Tom institucional e consultivo. Mostrar bastidores de engenharia, decisões de produto, aprendizados e resultados. A marca aparece com assinatura principal.'),
('GitHub', 'README com banner escuro, monograma, descrição objetiva, stack e links. Usar tipografia mono para comandos e tokens.'),
('Papelaria', 'Cartão em fundo ink com acabamento fosco; verso com monograma e contato. Papel timbrado com linha de construção e assinatura discreta.'),
('Fachada', 'Logo principal em marfim ou iluminação branca quente sobre superfície escura. Evitar excesso de informação.'),
('Notebook e uniforme', 'Monograma isolado em áreas pequenas. Assinatura horizontal em aplicações amplas. Acabamento sem brilho excessivo.'),
])
story.append(PageBreak())
story += [P('APLICAÇÃO DIGITAL', 'Kicker'), P('Uma peça Norvia deve ser identificada mesmo antes de o usuário ler o nome.', 'BodyN')]
story.append(card_grid([('Hero', 'Título de uma frase. Complemento de duas linhas. Uma ação. Fundo profundo com textura quase invisível.', GREEN), ('Post técnico', 'Label mono, título editorial, diagrama simples, conclusão prática. Acento usado para marcar a categoria.', BLUE), ('Case', 'Problema, decisão, resultado. Mostrar processo e evidência, não apenas imagem final.', GOLD), ('Anúncio', 'Uma mensagem, uma ação, uma composição. Não misturar campanhas de produtos sem arquitetura.', PINK)], 2))
story.append(PageBreak())

# Part 7
story += section('Manual completo', 'PARTE 07  /  GOVERNANÇA', 'O manual não termina no PDF. Ele continua em arquivos, componentes, decisões e revisão constante.', [
('Fonte de verdade', 'Manter uma pasta central com logos, tokens, templates, componentes e versões aprovadas. Cada arquivo deve ter nome, formato e data.'),
('Aprovação', 'Novas aplicações devem ser revisadas por design e produto. Mudanças de cor, assinatura ou tom de voz precisam de justificativa.'),
('Evolução', 'Revisar o sistema a cada ciclo relevante de produto. Evoluir não significa alterar a assinatura sem necessidade; significa tornar o sistema mais útil.'),
])
story.append(table([[cell('ENTREGA', 'TableHead'), cell('FORMATO', 'TableHead'), cell('STATUS RECOMENDADO', 'TableHead')], [cell('Logo principal, secundária e monograma'), cell('SVG, PDF, PNG transparente'), cell('Exportar em claro, escuro e monocromático.')], [cell('Tokens de cor e tipografia'), cell('CSS, JSON, Figma variables'), cell('Sincronizar com o design system.')], [cell('Ícones e templates'), cell('SVG, Figma, PPTX'), cell('Manter nomes e versões consistentes.')], [cell('Mockups e aplicações'), cell('PDF, PNG, apresentação'), cell('Usar apenas para comunicação aprovada.')], [cell('Manual'), cell('PDF para impressão e tela'), cell('Atualizar índice, versão e changelog.')]], [54*mm, 43*mm, 63*mm]))
story.append(PageBreak())
story += [P('CHECKLIST DE LANÇAMENTO', 'Kicker'), P('Antes de publicar qualquer peça, confirme os pontos abaixo.', 'BodyN')]
story.append(card_grid([('Marca', 'A versão está correta? A área de proteção foi respeitada? O contraste é suficiente?', GREEN), ('Mensagem', 'Existe uma ideia principal? O texto é claro, humano e objetivo?', GREEN), ('Sistema', 'Cores, tipo, espaçamento, ícones e estados seguem os tokens?', GREEN), ('Produto', 'O acento diferencia sem quebrar a família Norvia?', GREEN), ('Acessibilidade', 'O conteúdo é legível, navegável e compreensível em diferentes telas?', GREEN), ('Arquivo', 'Nome, formato, versão e destino estão corretos?', GREEN)], 2))
story.append(Spacer(1, 16))
story.append(P('Encerramento', 'H2N'))
story.append(P('Norvia Solutions é tecnologia com estrutura, clareza e intenção. Este sistema transforma a marca em uma experiência consistente para clientes, equipes, produtos e parceiros. A próxima versão deve nascer das decisões reais que o negócio continuar tomando.', 'QuoteN'))
story.append(P('NORVIA SOLUTIONS  /  ESTÚDIO DE SOFTWARE  //  v1.0', 'MonoN'))

doc = Book(PDF)
doc.handle_nextPageTemplate('cover')
doc.build(story)
print(PDF)
