from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether
)
from reportlab.platypus import Flowable
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
        self.addPageTemplates([PageTemplate(id='cover', frames=frame, onPage=cover_bg, autoNextPageTemplate='normal'), PageTemplate(id='normal', frames=frame, onPage=page_bg)])

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

class VisualBoard(Flowable):
    def __init__(self, kind, width=168*mm, height=92*mm):
        Flowable.__init__(self)
        self.kind = kind
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return min(self.width, availWidth), self.height

    def _label(self, c, text, x, y, color=MUTED, size=7.2, font='Consolas'):
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawString(x, y, text)

    def _swatch(self, c, x, y, w, h, color, name, value, text_color=BONE):
        c.setFillColor(color)
        c.roundRect(x, y, w, h, 5, fill=1, stroke=0)
        self._label(c, name, x+6, y+16, text_color, 8, 'Arial-Bold')
        self._label(c, value, x+6, y+6, text_color, 6.5)

    def _icon(self, c, x, y, kind, color=LINE, scale=1):
        c.saveState()
        c.setStrokeColor(color); c.setLineWidth(1.4*scale); c.setLineCap(1); c.setLineJoin(1)
        if kind == 'code':
            c.line(x+4*scale,y+10*scale,x+11*scale,y+17*scale); c.line(x+4*scale,y+10*scale,x+11*scale,y+3*scale)
            c.line(x+22*scale,y+10*scale,x+15*scale,y+17*scale); c.line(x+22*scale,y+10*scale,x+15*scale,y+3*scale)
        elif kind == 'data':
            c.ellipse(x+5*scale,y+14*scale,x+21*scale,y+19*scale,fill=0,stroke=1); c.line(x+5*scale,y+16*scale,x+5*scale,y+4*scale); c.line(x+21*scale,y+16*scale,x+21*scale,y+4*scale); c.arc(x+5*scale,y+1*scale,x+21*scale,y+7*scale,0,180); c.arc(x+5*scale,y+7*scale,x+21*scale,y+13*scale,0,180)
        elif kind == 'cloud':
            c.arc(x+3*scale,y+7*scale,x+14*scale,y+18*scale,30,220); c.arc(x+10*scale,y+7*scale,x+23*scale,y+20*scale,40,210); c.line(x+7*scale,y+7*scale,x+21*scale,y+7*scale); c.arc(x+7*scale,y+3*scale,x+22*scale,y+11*scale,180,360)
        elif kind == 'shield':
            p=c.beginPath(); p.moveTo(x+13*scale,y+21*scale); p.lineTo(x+22*scale,y+17*scale); p.lineTo(x+21*scale,y+7*scale); p.lineTo(x+13*scale,y+2*scale); p.lineTo(x+5*scale,y+7*scale); p.lineTo(x+4*scale,y+17*scale); p.close(); c.drawPath(p,fill=0,stroke=1); c.line(x+8*scale,y+11*scale,x+12*scale,y+7*scale); c.line(x+12*scale,y+7*scale,x+19*scale,y+15*scale)
        elif kind == 'chart':
            c.line(x+4*scale,y+4*scale,x+4*scale,y+20*scale); c.line(x+4*scale,y+4*scale,x+23*scale,y+4*scale); c.line(x+7*scale,y+9*scale,x+12*scale,y+13*scale); c.line(x+12*scale,y+13*scale,x+16*scale,y+10*scale); c.line(x+16*scale,y+10*scale,x+22*scale,y+18*scale)
        elif kind == 'users':
            c.circle(x+9*scale,y+16*scale,4*scale,fill=0,stroke=1); c.circle(x+19*scale,y+16*scale,3*scale,fill=0,stroke=1); c.arc(x+3*scale,y+2*scale,x+15*scale,y+13*scale,0,180); c.arc(x+14*scale,y+3*scale,x+24*scale,y+12*scale,0,180)
        elif kind == 'gear':
            c.circle(x+13*scale,y+11*scale,6*scale,fill=0,stroke=1); c.circle(x+13*scale,y+11*scale,2*scale,fill=0,stroke=1)
            for dx,dy in [(0,9),(0,-9),(9,0),(-9,0),(6,6),(-6,6),(6,-6),(-6,-6)]: c.line(x+13*scale,y+11*scale,x+(13+dx)*scale,y+(11+dy)*scale)
        c.restoreState()

    def draw(self):
        c = self.canv; w = self.width; h = self.height
        c.setFillColor(PANEL); c.roundRect(0, 0, w, h, 8, fill=1, stroke=0)
        c.setStrokeColor(HexColor('#385344')); c.setLineWidth(.5); c.roundRect(0, 0, w, h, 8, fill=0, stroke=1)
        if self.kind == 'colors':
            gap=6; sw=(w-5*gap)/4; sh=35
            items=[(INK,'INK','#0F1D18'),(PANEL,'PANEL','#15251E'),(PANEL2,'PANEL 2','#1A2C24'),(BONE,'BONE','#EDEBE3'),(GREEN,'CAMPO','#7FCB8F'),(GOLD,'SOL','#F0D179'),(BLUE,'CEU','#8FB8E8'),(PINK,'ROSA','#F2A0B6')]
            for i,(col,n,v) in enumerate(items): self._swatch(c, gap+(i%4)*(sw+gap), h-46-(i//4)*(sh+8), sw, sh, col, n, v, INK if n in ('BONE','CAMPO','SOL','CEU','ROSA') else BONE)
            self._label(c,'TOKENS DE COR  /  BASE + ACENTOS',gap,8,LIME,7)
        elif self.kind == 'type':
            self._label(c,'ARCHIVO  /  DISPLAY + BODY',12,h-18,LIME,7)
            c.setFillColor(BONE); c.setFont('Arial-Bold',25); c.drawString(12,h-48,'Norvia Solutions')
            c.setFont('Arial',12); c.drawString(12,h-67,'Tecnologia com clareza, estrutura e intencao.')
            self._label(c,'ABCDEFGHIJKLMNOPQRSTUVWXYZ  abcdefghijklmnopqrstuvwxyz  0123456789',12,h-83,MUTED,6.5,'Arial')
            c.setStrokeColor(HexColor('#385344')); c.line(w/2,10,w/2,h-10)
            self._label(c,'SPLINE SANS MONO  /  LABELS + DATA',w/2+12,h-18,LIME,7)
            c.setFillColor(GREEN); c.setFont('Consolas-Bold',18); c.drawString(w/2+12,h-48,'SYSTEM_READY')
            c.setFont('Consolas',10); c.drawString(w/2+12,h-65,'space.4  /  #0F1D18  /  v1.0')
            self._label(c,'ABCDEFGHIJKLMNOPQRSTUVWXYZ  abcdefghijklmnopqrstuvwxyz  0123456789',w/2+12,h-83,MUTED,6.5,'Consolas')
        elif self.kind == 'icons':
            kinds=[('code','Code'),('data','Data'),('cloud','Cloud'),('shield','Trust'),('chart','Growth'),('users','People'),('gear','Settings')]
            x=14
            for kind,name in kinds:
                c.setFillColor(PANEL2); c.roundRect(x,27,44,44,7,fill=1,stroke=0); self._icon(c,x+8,38,kind,GREEN,1.1); self._label(c,name,x+5,15,MUTED,6.2); x+=50
            self._label(c,'ICON SET  /  24 PX GRID  /  1.5 PX STROKE  /  ROUND CAPS',14,h-14,LIME,7)
        elif self.kind == 'components':
            self._label(c,'BUTTONS',12,h-14,LIME,7)
            c.setFillColor(GREEN); c.roundRect(12,h-42,70,18,6,fill=1,stroke=0); self._label(c,'Primary  ->',21,h-36,INK,7,'Arial-Bold')
            c.setFillColor(PANEL2); c.setStrokeColor(LINE); c.roundRect(90,h-42,70,18,6,fill=1,stroke=1); self._label(c,'Secondary',103,h-36,BONE,7,'Arial')
            self._label(c,'INPUT + BADGE + ALERT',12,h-61,LIME,7)
            c.setFillColor(PANEL2); c.setStrokeColor(LINE); c.roundRect(12,h-88,86,18,5,fill=1,stroke=1); self._label(c,'Project name',20,h-82,MUTED,7,'Arial')
            c.setFillColor(HexColor('#243A2F')); c.roundRect(108,h-88,52,18,9,fill=1,stroke=0); self._label(c,'Active',119,h-82,GREEN,7,'Arial-Bold')
            c.setFillColor(HexColor('#20382A')); c.roundRect(12,16,148,23,6,fill=1,stroke=0); self._icon(c,19,17,'shield',GREEN,.65); self._label(c,'Projeto salvo com sucesso',43,25,GREEN,7,'Arial-Bold')
            self._label(c,'STATES  /  DEFAULT  HOVER  FOCUS  DISABLED  LOADING',12,6,MUTED,6.5)
        elif self.kind == 'spacing':
            self._label(c,'SPACING SCALE  /  4 PX BASE UNIT',12,h-14,LIME,7)
            values=[('1',4),('2',8),('3',12),('4',16),('6',24),('8',32),('12',48),('16',64)]
            x=14
            for name,val in values:
                c.setFillColor(GREEN); c.rect(x,24,val*1.15,20,fill=1,stroke=0); self._label(c,name,x,14,MUTED,6.5); self._label(c,str(val)+' px',x,50,BONE,6.5); x+=val*1.15+14
        elif self.kind == 'dashboard':
            # Reference board inspired by the supplied Figma file: same information in light and dark surfaces.
            for ox, surface, text, sub in [(12, HexColor('#F7F8FA'), HexColor('#15251E'), HexColor('#6B7770')), (w/2+4, INK, BONE, MUTED)]:
                c.setFillColor(surface); c.roundRect(ox, 10, w/2-20, h-20, 6, fill=1, stroke=0)
                self._label(c,'Dashboard',ox+10,h-28,text,8,'Arial-Bold'); self._label(c,'Overview  /  Projects  /  Settings',ox+10,h-40,sub,5.5,'Consolas')
                cardw=(w/2-42)/3
                for j,(value,label) in enumerate([('24','Projects'),('86%','Progress'),('12','Alerts')]):
                    xx=ox+8+j*(cardw+4); c.setFillColor(HexColor('#FFFFFF') if surface != INK else PANEL); c.roundRect(xx,h-75,cardw,24,4,fill=1,stroke=0); self._label(c,value,xx+5,h-63,text if surface != INK else BONE,9,'Arial-Bold'); self._label(c,label,xx+5,h-71,sub if surface != INK else MUTED,5.5,'Arial')
                c.setStrokeColor(HexColor('#D9E0DB') if surface != INK else HexColor('#385344')); c.line(ox+10,27,ox+w/2-30,27); c.line(ox+10,27,ox+25,42); c.line(ox+25,42,ox+42,36); c.line(ox+42,36,ox+57,50); c.line(ox+57,50,ox+80,45)
            self._label(c,'SAME COMPONENTS  /  LIGHT THEME + DARK THEME',12,2,LIME,6.5)

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

# Design System standalone opening: structured like a Figma library file.
story.append(PageBreak())
story += [P('NORVIA DESIGN SYSTEM', 'CoverTitle'), P('Biblioteca visual e de componentes', 'H1N'), Spacer(1, 14*mm), P('FOUNDATIONS  /  COMPONENTS  /  PATTERNS', 'Kicker'), P('Uma referencia para designers, desenvolvedores e equipes de produto.', 'QuoteN'), P('Versao 1.0  |  Light + Dark  |  Desktop + Mobile', 'SmallN'), Spacer(1, 52*mm), P('Organizado por pranchas visuais, tokens e exemplos de uso.', 'BodyN')]
story.append(PageBreak())
story += [P('NAVEGACAO', 'Kicker'), P('Indice do Design System', 'H1N'), P('Cada secao corresponde a uma biblioteca que pode ser usada no dia a dia do produto.', 'BodyN')]
story.append(table([[cell('01', 'TableHead'), cell('Foundations'), cell('Cores, fontes, espacamento, grid, raio, sombra e motion.')], [cell('02', 'TableHead'), cell('Iconografia'), cell('Grade, espessura, paths e aplicacao dos icones.')], [cell('03', 'TableHead'), cell('Components'), cell('Buttons, inputs, cards, badges, alerts e data display.')], [cell('04', 'TableHead'), cell('Patterns'), cell('Navbar, sidebar, dashboard, landing e estados.')], [cell('05', 'TableHead'), cell('Quality bar'), cell('Acessibilidade, conteudo e governanca.')]], [18*mm, 48*mm, 94*mm]))
story.append(PageBreak())

# Visual asset sheets: usable references, not only prose.
story.append(PageBreak())
story += [P('PALETA VISUAL', 'Kicker'), P('A paleta abaixo e a referencia visual para interfaces, apresentacoes e materiais de marca.', 'BodyN'), VisualBoard('colors')]
story.append(PageBreak())
story += [P('TIPOGRAFIA EM USO', 'Kicker'), P('Estas sao as fontes e suas funcoes. Arquivo e a voz principal; Spline Sans Mono organiza a camada tecnica.', 'BodyN'), VisualBoard('type')]
story.append(PageBreak())
story += [P('ICONOGRAFIA', 'Kicker'), P('Icones vetoriais de apoio com grade de 24 px, traco de 1.5 px e terminais arredondados.', 'BodyN'), VisualBoard('icons')]
story.append(PageBreak())
story += [P('COMPONENTES VISUAIS', 'Kicker'), P('Exemplos de componentes renderizados com os tokens da Norvia. A documentacao define o comportamento; esta prancha mostra a linguagem.', 'BodyN'), VisualBoard('components')]
story.append(PageBreak())
story += [P('ESCALA DE ESPACAMENTO', 'Kicker'), P('A unidade de 4 px organiza o ritmo de todas as interfaces. Use a escala, nao valores improvisados.', 'BodyN'), VisualBoard('spacing')]
story.append(PageBreak())
story += [P('PADRAO DE DASHBOARD', 'Kicker'), P('Uma mesma linguagem em claro e escuro', 'H1N'), P('O arquivo de referencia usa telas de produto como biblioteca. A Norvia deve manter os mesmos componentes entre temas, mudando apenas superficie, contraste e semantica.', 'BodyN'), VisualBoard('dashboard')]

# Design system expansion: reference documentation for product teams.
story.append(PageBreak())
story += [P('DESIGN SYSTEM', 'Kicker'), P('Foundations: a base que sustenta tudo', 'H1N'), P('Foundations sao as decisoes mais reutilizadas do sistema. Devem ser aplicadas antes de qualquer componente novo.', 'BodyN')]
story.append(card_grid([
('Cor', 'Use tokens semanticos em vez de hex espalhado. Cor de produto identifica contexto; cor semantica comunica estado.', GREEN),
('Espaco', 'A escala de 4 px organiza padding, gap e margem. Componentes respiram em multiplos previsiveis.', GREEN),
('Tipo', 'Archivo cria a voz editorial. Spline Sans Mono cria a camada tecnica para labels, numeros e dados.', GREEN),
('Forma', 'Raios medios e superficies escuras criam um sistema contemporaneo sem parecer generico.', GREEN),
('Profundidade', 'Bordas sutis primeiro; sombras apenas quando existe uma relacao de camada.', GREEN),
('Movimento', 'Animar ajuda a entender mudanca de estado. Nunca use movimento como decoracao obrigatoria.', GREEN),
], 2))
story.append(PageBreak())
story += [P('TOKENS', 'Kicker'), P('Tokens sao nomes de decisao. O produto usa o nome; a marca controla o valor.', 'BodyN')]
story.append(table([[cell('GRUPO', 'TableHead'), cell('EXEMPLOS', 'TableHead'), cell('REGRA', 'TableHead')], [cell('Color'), cell('color.text.primary, color.brand, color.semantic.success'), cell('Nao usar valores diretos quando existir token.')], [cell('Space'), cell('space.1 ate space.24'), cell('Usar a escala para padding, gap, margin e layout.')], [cell('Radius'), cell('radius.sm, md, lg, xl, pill'), cell('Raio pequeno para controle; medio para superficies; pill para tags.')], [cell('Type'), cell('font.display, font.body, font.mono'), cell('Escolher pela funcao, nao pela preferencia individual.')], [cell('Motion'), cell('motion.fast, base, slow'), cell('Respeitar prefers-reduced-motion.')]], [31*mm, 67*mm, 64*mm]))
story.append(PageBreak())
story += [P('GRID E RESPONSIVIDADE', 'Kicker'), P('O grid e invisivel quando funciona. Ele cria ritmo, alinhamento e uma leitura consistente em qualquer tela.', 'BodyN')]
story.append(card_grid([
('Container', 'Mobile: 100% menos 20 px de cada lado. Tablet: maximo 832 px. Desktop: maximo 1152 px.', GREEN),
('Colunas', 'Desktop usa 12 colunas; tablet 8; mobile 4. O gap deve seguir space.4 ou space.6.', GREEN),
('Breakpoint sm', 'A partir de 640 px, navegação e cards podem ganhar mais respiro.', BLUE),
('Breakpoint md', 'A partir de 832 px, layouts de duas colunas e sidebars ficam confortaveis.', BLUE),
('Breakpoint lg', 'A partir de 1152 px, use a largura total do container e areas de apoio.', BLUE),
('Regra mobile', 'Empilhe antes de comprimir. Preserve hierarquia, toque e leitura.', GREEN),
], 2))
story.append(PageBreak())
story += [P('BUTTONS E LINKS', 'Kicker'), P('Acoes devem ter uma hierarquia obvia e estados que expliquem o que esta acontecendo.', 'BodyN')]
story.append(table([[cell('VARIANTE', 'TableHead'), cell('QUANDO USAR', 'TableHead'), cell('ESTADOS OBRIGATORIOS', 'TableHead')], [cell('Primary'), cell('Acao principal da tela ou fluxo.'), cell('Default, hover, pressed, focus, disabled, loading.')], [cell('Secondary'), cell('Acao alternativa sem competir com a principal.'), cell('Default, hover, pressed, focus, disabled.')], [cell('Tertiary'), cell('Acao discreta, contextual ou em toolbar.'), cell('Default, hover, focus, disabled.')], [cell('Destructive'), cell('Excluir, cancelar perda ou remover dado.'), cell('Default, hover, focus, disabled, confirmacao.')], [cell('Text link'), cell('Navegacao dentro de texto ou lista.'), cell('Default, hover, visited quando aplicavel, focus.')]], [32*mm, 63*mm, 67*mm]))
story.append(Spacer(1, 12))
story.append(P('Anatomia', 'H2N'))
story.append(P('Label curto + icone opcional + area de toque minima de 44 px. O texto deve descrever o resultado: Salvar projeto e melhor que Enviar.', 'BodyN'))
story.append(PageBreak())
story += [P('FORMULARIOS', 'Kicker'), P('Formularios devem reduzir duvida, nao apenas coletar informacao.', 'BodyN')]
story.append(table([[cell('ELEMENTO', 'TableHead'), cell('REGRA DE CONTEUDO', 'TableHead'), cell('VALIDACAO', 'TableHead')], [cell('Label'), cell('Sempre visivel e escrito como tarefa ou dado.'), cell('Nao depende apenas de placeholder.')], [cell('Helper text'), cell('Explica formato, limite ou consequencia.'), cell('Permanece proximo do campo.')], [cell('Error'), cell('Diz o que aconteceu e como corrigir.'), cell('Cor + texto + foco no primeiro erro.')], [cell('Select'), cell('Usar quando ha opcoes conhecidas e limitadas.'), cell('Mostra valor atual e opcao de limpar quando necessario.')], [cell('Checkbox'), cell('Usar para escolhas independentes.'), cell('Nunca usar so cor para indicar marcado.')], [cell('Radio'), cell('Usar para escolha unica em conjunto pequeno.'), cell('Uma opcao deve estar selecionada quando obrigatorio.')]], [29*mm, 72*mm, 61*mm]))
story.append(PageBreak())
story += [P('CARDS, BADGES E ALERTAS', 'Kicker'), P('Superficies ajudam a agrupar informacao. O agrupamento deve ter uma razao de uso.', 'BodyN')]
story.append(card_grid([
('Card de produto', 'Topo com acento, titulo, resumo, metadados e acao. Nao esconder o objetivo no hover.', GREEN),
('Card de metrica', 'Numero grande, label curto, periodo e variacao. Mostrar unidade e contexto.', BLUE),
('Badge', 'Categoria ou estado curto. Nunca usar badge como paragrafo ou unica explicacao.', LIME),
('Alert', 'Titulo opcional, explicacao, acao e icone semantico. Pode ser success, info, warning ou danger.', GOLD),
('Toast', 'Feedback breve de uma acao recente. Nao usar para erros que exigem leitura longa.', PINK),
('Empty state', 'Explica por que esta vazio, o que fazer agora e o que acontecera depois.', PURPLE),
], 2))
story.append(PageBreak())
story += [P('DATA DISPLAY', 'Kicker'), P('Dados precisam ser comparaveis, escaneaveis e honestos sobre seu contexto.', 'BodyN')]
story.append(table([[cell('PADRAO', 'TableHead'), cell('USO', 'TableHead'), cell('CUIDADOS', 'TableHead')], [cell('Metric'), cell('Valor principal e variacao.'), cell('Mostrar periodo, unidade e direcao.')], [cell('Table'), cell('Listas operacionais e comparacoes.'), cell('Cabecalho fixo, alinhamento por tipo, overflow no mobile.')], [cell('Chart'), cell('Tendencia, distribuicao ou comparacao.'), cell('Nao distorcer escala; legenda acessivel; cor redundante.')], [cell('Progress'), cell('Avanco para um objetivo conhecido.'), cell('Mostrar valor atual e total quando possivel.')], [cell('Timeline'), cell('Historico e etapas.'), cell('Ordenacao e estado atual devem ser explicitos.')]], [34*mm, 55*mm, 73*mm]))
story.append(Spacer(1, 10))
story.append(P('Regra de cor', 'H2N'))
story.append(P('Use cor para destacar uma conclusao, nao para pintar toda a informacao. Em graficos, combine cor com label, forma, padrao ou texto.', 'BodyN'))
story.append(PageBreak())
story += [P('NAVBAR, SIDEBAR E NAVEGACAO', 'Kicker'), P('Navegacao deve orientar o usuario sem disputar com a tarefa principal.', 'BodyN')]
story.append(card_grid([
('Navbar institucional', 'Marca, links principais, acao de contato. Sticky apenas quando ajuda o retorno.', GREEN),
('Sidebar de produto', 'Logo do produto, grupos de navegacao, estado ativo, suporte e perfil. Pode colapsar.', BLUE),
('Breadcrumb', 'Usar em hierarquias profundas; o ultimo item e o contexto atual, nao um link redundante.', GREEN),
('Tabs', 'Trocar visoes do mesmo nivel. Nao usar tabs para etapas que precisam de sequencia.', GOLD),
('Pagination', 'Para conjuntos extensos; manter pagina atual, proximos passos e quantidade total.', PURPLE),
('Mobile navigation', 'Prioriza as 3 a 5 acoes mais frequentes. O restante vai para menu contextual.', PINK),
], 2))
story.append(PageBreak())
story += [P('DASHBOARD E OPERACAO', 'Kicker'), P('Dashboards Norvia devem transformar informacao em proxima decisao.', 'BodyN')]
story.append(table([[cell('FAIXA', 'TableHead'), cell('CONTEUDO', 'TableHead'), cell('DECISAO ESPERADA', 'TableHead')], [cell('Header'), cell('Titulo, periodo, filtros e acao primaria.'), cell('O que estou vendo e o que posso fazer?')], [cell('Overview'), cell('3 a 5 metricas de alto nivel.'), cell('Algo mudou? A tendencia e positiva?')], [cell('Main work'), cell('Tabela, fila, grafico ou calendario.'), cell('Qual item exige atencao agora?')], [cell('Context'), cell('Ajuda, historico, filtros salvos.'), cell('De onde veio este dado?')], [cell('Feedback'), cell('Toast, alert, empty ou erro.'), cell('O sistema confirmou ou precisa de acao?')]], [29*mm, 71*mm, 62*mm]))
story.append(PageBreak())
story += [P('ACESSIBILIDADE', 'Kicker'), P('Acessibilidade e parte da qualidade Norvia, nao uma etapa opcional.', 'BodyN')]
story.append(card_grid([
('Contraste', 'Texto principal deve ser legivel sobre a superficie. Nunca depender apenas de cor para transmitir estado.', GREEN),
('Foco', 'Todo elemento interativo recebe foco visivel. O anel usa o token focus-ring.', GOLD),
('Toque', 'Alvos interativos devem ter pelo menos 44 px em mobile.', BLUE),
('Teclado', 'Fluxo logico, sem armadilhas de foco, escape para fechar overlays.', PURPLE),
('Leitura', 'Hierarquia semantica, labels claros, texto alternativo e linguagem direta.', PINK),
('Movimento', 'Reduzir transicoes para usuarios que preferem menos movimento.', GREEN),
], 2))
story.append(PageBreak())
story += [P('CONTEUDO E VOZ DE INTERFACE', 'Kicker'), P('O produto fala como a Norvia: direto, humano, preciso e sem promessa vazia.', 'BodyN')]
story.append(table([[cell('SITUACAO', 'TableHead'), cell('EVITAR', 'TableHead'), cell('PREFERIR', 'TableHead')], [cell('Sucesso'), cell('Tudo certo!'), cell('Projeto salvo. Voce pode continuar editando.')], [cell('Erro'), cell('Algo deu errado.'), cell('Nao foi possivel salvar. Verifique a conexao e tente novamente.')], [cell('Vazio'), cell('Nenhum resultado.'), cell('Ainda nao ha clientes cadastrados. Adicione o primeiro para comecar.')], [cell('Confirmacao'), cell('Tem certeza?'), cell('Excluir este cliente? Esta acao nao pode ser desfeita.')], [cell('Loading'), cell('Aguarde...'), cell('Carregando dados do projeto.')]], [32*mm, 58*mm, 72*mm]))
story.append(PageBreak())
story += [P('GOVERNANCA DO SISTEMA', 'Kicker'), P('Um sistema profissional precisa de criterio para crescer sem virar uma colecao de excecoes.', 'BodyN')]
story.append(card_grid([
('Novo componente', 'Antes de criar, procure um padrao existente. Se a necessidade for recorrente, documente anatomia, props e estados.', GREEN),
('Nomeacao', 'Use nomes funcionais e previsiveis. Button, Card, Input, Alert. Variantes descrevem comportamento.', BLUE),
('Review', 'Toda mudanca deve incluir exemplo visual, responsividade, acessibilidade e impacto nos tokens.', GOLD),
('Versionamento', 'Atualize versao, changelog e migration note quando houver breaking change.', PURPLE),
('Deprecacao', 'Marque o componente, ofereca substituto e mantenha o periodo de transicao documentado.', PINK),
('Ownership', 'Design define linguagem; engenharia define implementacao; produto valida contexto e resultado.', GREEN),
], 2))
story.append(Spacer(1, 12))
story.append(P('Definition of done', 'H2N'))
story.append(P('Um componente so esta pronto quando possui tokens, estados, exemplos desktop e mobile, comportamento de teclado, texto de acessibilidade, teste visual e documentacao de uso.', 'BodyN'))

doc = Book(PDF)
doc.build(story)
print(PDF)
