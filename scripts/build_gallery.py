#!/usr/bin/env python3
"""Build editable research diagrams, PNG previews, and the A3 proposal PDF.

Requires ReportLab, a Korean regular/bold TTF pair, and pdftoppm.
See docs/assets/README.md for reproduction and source records.
"""
from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import shutil
import subprocess

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
PAPER = '#f8f7f2'
INK = '#192f34'
MUTED = '#596c6d'
LINE = '#c8d2cb'
GREEN = '#246b53'
SAGE = '#e6eee6'
BLUE = '#466788'
PALE_BLUE = '#eaf0f6'
RUST = '#a55335'
SAND = '#f2e8d9'
WHITE = '#ffffff'


class Figure:
    def __init__(self, width, height, title, description, name, a3=False):
        self.w, self.h, self.name = width, height, name
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>']
        self.qa = ROOT / 'eval-runs/gallery-2026-10-08'
        self.qa.mkdir(parents=True, exist_ok=True)
        self.pdf = self.qa / f'{name}.pdf'
        pagesize = landscape(A3) if a3 else (width, height)
        self.c = canvas.Canvas(str(self.pdf), pagesize=pagesize, invariant=1)
        self.c.setTitle(title)
        self.c.setAuthor('Human Researcher')
        self.c.scale(pagesize[0] / width, pagesize[1] / height)
        self.rect(0, 0, width, height, PAPER)

    def rect(self, x, y, w, h, fill=WHITE, stroke=None, radius=0, dashed=False):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill or "none"}" stroke="{stroke or "none"}" stroke-width="1.6"' + (' stroke-dasharray="7 5"' if dashed else '') + '/>')
        self.c.saveState()
        self.c.setLineWidth(1.6)
        if dashed:
            self.c.setDash(7, 5)
        if fill:
            self.c.setFillColor(HexColor(fill))
        if stroke:
            self.c.setStrokeColor(HexColor(stroke))
        self.c.roundRect(x, self.h-y-h, w, h, radius, fill=bool(fill), stroke=bool(stroke))
        self.c.restoreState()

    def text(self, x, y, text, size=24, color=INK, bold=False, serif=False, anchor='start', max_width=None):
        font = 'Times-Roman' if serif else ('KRBold' if bold else 'KR')
        width = pdfmetrics.stringWidth(text, font, size)
        if max_width and width > max_width:
            raise ValueError(f'{self.name}: text exceeds its column ({width:.1f} > {max_width}): {text}')
        family = "'Times New Roman',Times,serif" if serif else "NanumSquare,'Apple SD Gothic Neo','Noto Sans KR',sans-serif"
        self.parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(text)}</text>')
        self.c.setFillColor(HexColor(color))
        self.c.setFont(font, size)
        draw = {'start': self.c.drawString, 'middle': self.c.drawCentredString, 'end': self.c.drawRightString}[anchor]
        draw(x, self.h-y, text)

    def lines(self, x, y, lines, size=24, leading=35, **kwargs):
        for i, text in enumerate(lines):
            self.text(x, y+i*leading, text, size, **kwargs)

    def path(self, points, color=LINE, width=2, dashed=False, arrow=False):
        value = ' '.join(f'{x},{y}' for x,y in points)
        self.parts.append(f'<polyline points="{value}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"' + (' stroke-dasharray="7 5"' if dashed else '') + '/>')
        self.c.saveState()
        self.c.setStrokeColor(HexColor(color))
        self.c.setLineWidth(width)
        if dashed:
            self.c.setDash(7, 5)
        p = self.c.beginPath()
        p.moveTo(points[0][0], self.h-points[0][1])
        for x,y in points[1:]:
            p.lineTo(x,self.h-y)
        self.c.drawPath(p)
        self.c.restoreState()
        if arrow:
            import math
            a,b = points[-2:]
            angle = math.atan2(b[1]-a[1],b[0]-a[0])
            tips=[(b[0]-10*math.cos(angle-d), b[1]-10*math.sin(angle-d)) for d in [-.45,.45]]
            self.path([tips[0],b,tips[1]],color,width)

    def dot(self, x,y,r=4,color=GREEN):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
        self.c.setFillColor(HexColor(color))
        self.c.circle(x,self.h-y,r,stroke=0,fill=1)

    def label(self,x,y,value,color=GREEN):
        self.text(x,y,value,17,color,bold=True)

    def link(self,x,y,w,h,url):
        self.parts.append(f'<a href="{escape(url,quote=True)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="transparent"/></a>')
        self.c.linkURL(url,(x,self.h-y-h,x+w,self.h-y),relative=1)

    def footer(self, text, edition):
        self.path([(64,self.h-71),(self.w-64,self.h-71)])
        self.text(64,self.h-35,text,17,MUTED,max_width=self.w-350)
        self.text(self.w-64,self.h-35,f'HUMAN RESEARCHER / {edition}',16,GREEN,anchor='end')

    def save(self, source, preview, pdf=None, html=None):
        self.parts.append('</svg>')
        svg='\n'.join(self.parts)+'\n'
        path=ROOT/source
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(svg,encoding='utf-8')
        self.c.showPage()
        self.c.save()
        if pdf:
            shutil.copyfile(self.pdf,ROOT/pdf)
        preview=ROOT/preview
        preview.parent.mkdir(parents=True,exist_ok=True)
        subprocess.run(['pdftoppm','-singlefile','-scale-to',str(self.w),'-png',str(self.pdf),str(preview.with_suffix(''))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        if html:
            # One source geometry is shared by SVG, PDF, PNG, and the printable HTML.
            (ROOT/html).write_text('''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>긴 입력에서도 4-bit는 유리할까요? | Human Researcher</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#dfe5e0;color:#192f34;font:16px/1.6 system-ui,sans-serif}
.toolbar{max-width:1600px;margin:20px auto;padding:0 24px;display:flex;gap:24px;align-items:center;flex-wrap:wrap}
a{color:#246b53}button{padding:9px 18px;border:0;border-radius:4px;background:#192f34;color:white;cursor:pointer}
.poster{width:min(1600px,100%);margin:0 auto 24px;background:#f8f7f2}.poster svg{display:block;width:100%;height:auto}
@page{size:A3 landscape;margin:0}@media print{.toolbar{display:none}body{background:white}.poster{width:420mm;height:297mm;margin:0}.poster svg{width:100%;height:100%}*{print-color-adjust:exact;-webkit-print-color-adjust:exact}}
</style></head><body><nav class="toolbar"><button onclick="window.print()">인쇄 / PDF 저장</button><a href="poster.pdf">검수한 PDF</a><a href="proposal.md">전체 proposal</a><a href="sources.md">문헌 근거</a><span>A3 가로 · 연구계획 예제 · 실험 미실행</span></nav><main class="poster">
'''+svg+'</main></body></html>\n',encoding='utf-8')
        print(f'Built {source} and {preview.relative_to(ROOT)}')


def taxonomy():
    f=Figure(1600,1100,'PEFT: 무엇을 학습하고 무엇을 고정할까요?',
             '선택한 일곱 논문의 주요 적응 메커니즘을 분류합니다. BitFit, Prefix-Tuning, Adapters, IA3, LoRA, DoRA를 학습 대상에 따라 배치하고 QLoRA의 기반 양자화는 별도 축으로 표시합니다. 분류선은 인용이나 성능 순위가 아닙니다.', 'peft-taxonomy')
    f.label(64,49,'01 / LITERATURE TAXONOMY')
    f.text(64,124,'A field, made legible.',67,serif=True)
    f.text(64,170,'무엇을 학습하고, 무엇을 고정할까요?',30,bold=True)
    f.text(1536,60,'SELECTED PEFT PAPERS',18,MUTED,anchor='end')
    f.text(1536,95,'2019-2024 / 7 SOURCES',18,MUTED,anchor='end')
    for x,label in [(64,'SCOPE'),(390,'MAIN INTERVENTION'),(715,'LEARNED OBJECT'),(1060,'REPRESENTATIVE WORK')]:
        f.label(x,221,label,MUTED)
    f.path([(64,238),(1536,238)])
    # Every solid edge encodes category membership, never citation or chronology.
    f.path([(314,543),(346,543),(346,300),(390,300)],GREEN)
    f.path([(346,543),(390,546)],GREEN)
    f.path([(346,543),(346,811),(390,811)],GREEN)
    f.rect(64,483,250,120,INK,radius=5)
    f.text(88,532,'PEFT',42,WHITE,serif=True)
    f.text(88,569,'언어 모델 적응',23,'#dce7de')
    groups=[(260,'선택해 갱신','기존 파라미터의 일부',SAND,RUST),(506,'추가해 학습','새 모듈·벡터',SAGE,GREEN),(771,'다르게 표현','가중치 업데이트',PALE_BLUE,BLUE)]
    for y,title,subtitle,fill,color in groups:
        f.rect(390,y,250,80,fill,radius=5)
        f.text(410,y+34,title,28,color,bold=True)
        f.text(410,y+62,subtitle,20,MUTED)
    rows=[
        (260,'Bias terms','편향 파라미터','BitFit','[01] Ben-Zaken et al. / 2021',RUST,'https://arxiv.org/abs/2106.10199v5'),
        (406,'Prefix vectors','연속적인 prefix','Prefix-Tuning','[02] Li & Liang / 2021',GREEN,'https://arxiv.org/abs/2101.00190v1'),
        (506,'Adapter modules','추가 적응 모듈','Adapters','[03] Houlsby et al. / 2019',GREEN,'https://arxiv.org/abs/1902.00751v2'),
        (606,'Activation scales','학습하는 스케일 벡터','(IA)³','[04] Liu et al. / 2022',GREEN,'https://arxiv.org/abs/2205.05638v2'),
        (731,'Low-rank updates','고정 기반 + 저랭크 갱신','LoRA','[05] Hu et al. / 2021',BLUE,'https://arxiv.org/abs/2106.09685v2'),
        (831,'Magnitude + direction','크기·방향 분해 / 방향에 LoRA','DoRA','[06] Liu et al. / 2024',BLUE,'https://arxiv.org/abs/2402.09353v6')]
    for y,title,subtitle,paper,cite,color,url in rows:
        parent=300 if y==260 else (546 if y<700 else 811)
        f.path([(640,parent),(677,parent),(677,y+40),(715,y+40)],color)
        f.rect(715,y,286,80,WHITE,LINE,4)
        f.text(733,y+33,title,23,bold=True,max_width=251)
        f.text(733,y+62,subtitle,17,MUTED,max_width=251)
        f.path([(1001,y+40),(1060,y+40)],color)
        f.dot(1060,y+40,4,color)
        f.text(1080,y+33,paper,32,color,bold=True)
        f.text(1080,y+64,cite,19,MUTED)
        f.link(1070,y,450,80,url)
    f.rect(64,943,1472,68,INK,radius=5)
    f.label(84,972,'ANOTHER AXIS', '#b5d4bd')
    f.text(84,996,'고정 기반의 저장 정밀도',18,WHITE)
    f.text(357,985,'QLoRA [07]',31,WHITE,serif=True)
    f.text(589,985,'4-bit 고정 기반 + LoRA  /  학습 메커니즘과 별도로 보는 선택',23,WHITE,max_width=900)
    f.link(350,947,1120,59,'https://arxiv.org/abs/2305.14314v1')
    f.footer('실선 = 분류 관계 · 주요 메커니즘 기준의 잠정 지도 · 성능 순위·전체 분야 조사가 아닙니다.', '01')
    f.save('examples/peft-taxonomy/taxonomy.svg','docs/assets/peft-taxonomy-preview.png')


def poster():
    f=Figure(1600,1131,'긴 입력에서도 4-bit는 유리할까요?',
             'LoRA와 QLoRA를 출발점으로 설계한 미실행 연구계획입니다. 같은 설정의 16-bit와 4-bit 고정 기반을 각 길이 안에서 비교하며 메모리, 품질, 처리량과 OOM을 함께 측정합니다.', 'proposal-poster',a3=True)
    f.rect(0,0,1600,245,INK)
    f.label(64,46,'02 / RESEARCH PROPOSAL','#aacdb6')
    f.text(64,129,'Same adapters. Different memory.',65,WHITE,serif=True,max_width=1400)
    f.text(64,198,'긴 입력에서도, 4-bit는 유리할까요?',37,WHITE,bold=True)
    f.text(1536,43,'PLANNED STUDY / NO RESULTS',17,'#d7e3da',anchor='end')
    f.text(1536,199,'한 모델 · 한 데이터 파이프라인',21,'#d7e3da',anchor='end')
    f.label(64,289,'01 / EVIDENCE')
    f.text(64,337,'출발점은 두 논문',29,bold=True)
    f.text(64,392,'LoRA [1]',31,serif=True)
    f.lines(64,425,['기반 가중치는 고정합니다.','저랭크 갱신을 학습합니다.'],22,32,color=MUTED)
    f.path([(64,482),(366,482)])
    f.text(64,521,'QLoRA [2]',31,serif=True)
    f.lines(64,554,['고정 기반을 4-bit로 저장하고','저랭크 어댑터를 학습합니다.'],22,32,color=MUTED)
    f.rect(64,613,302,98,SAGE,radius=4)
    f.label(80,642,'HYPOTHESIS / 미검증')
    f.lines(80,671,['긴 입력의 다른 메모리 성분이','상대적 절감 폭을 줄일까요?'],20,27)
    f.label(422,289,'02 / THE CONTROLLED CONTRAST')
    f.rect(422,319,678,63,SAGE,radius=4)
    f.text(761,359,'동일 체크포인트 · 데이터 · 어댑터 설정',25,GREEN,bold=True,anchor='middle')
    f.path([(761,382),(761,403),(583,403),(583,428)],GREEN,arrow=True)
    f.path([(761,403),(938,403),(938,428)],GREEN,arrow=True)
    for x,label in [(422,'16-bit'),(777,'4-bit')]:
        f.rect(x,428,323,194,WHITE,BLUE,5,dashed=True)
        f.text(x+161,466,label,36,BLUE,bold=True,anchor='middle')
        f.rect(x+24,482,275,59,PALE_BLUE,radius=3)
        f.text(x+161,519,'FROZEN BASE',21,BLUE,bold=True,anchor='middle')
        f.text(x+46,587,'+',31,GREEN,bold=True)
        f.rect(x+83,560,216,43,SAGE,radius=3)
        f.text(x+191,589,'학습하는 어댑터',22,GREEN,bold=True,anchor='middle')
    f.path([(583,622),(583,646),(761,646),(761,665)],BLUE,arrow=True)
    f.path([(938,622),(938,646),(761,646)],BLUE)
    f.text(761,700,'각 길이 안에서 두 조건을 비교합니다.',25,BLUE,bold=True,anchor='middle')
    f.label(1154,289,'03 / KEEP FIXED')
    for i,(title,detail) in enumerate([('모델과 데이터','체크포인트·토크나이저·분할'),('학습 조건','어댑터·토큰 예산·선택 규칙'),('실행과 측정','장비·버전·측정 구간')]):
        y=349+i*111
        f.text(1154,y,str(i+1).zfill(2),22,GREEN,bold=True)
        f.text(1203,y,title,24,bold=True)
        f.text(1154,y+36,detail,21,MUTED,max_width=383)
        f.path([(1154,y+60),(1536,y+60)])
    f.lines(1154,687,['정밀도별 커널 차이는 기록합니다.'],20,color=MUTED)
    f.path([(64,742),(1536,742)],INK)
    f.label(64,781,'04 / EVALUATION PLAN')
    f.text(64,828,'256 / 512 / 1,024 tokens',31,bold=True)
    f.text(64,863,'후보 길이입니다. 지원 범위와 파일럿 후 확정합니다.',21,MUTED)
    f.text(64,911,'Peak allocated / reserved memory',24,GREEN,bold=True)
    f.text(64,946,'Held-out NLL · 처리량 · OOM도 함께 기록합니다.',22)
    f.text(64,982,'품질 허용폭과 반복 수는 독립 확인 전에 정합니다.',21,MUTED)
    f.label(820,781,'05 / WHAT WOULD CHANGE OUR MIND?')
    decisions=[('절감 + 품질 기준 충족','평가한 설정에서 채택을 검토합니다.',GREEN),('절감 + 품질 기준 미달','메모리만으로 유용성을 결론 내리지 않습니다.',RUST),('불확실 / 한 조건이 OOM','결론을 유보하거나 실행 경계를 보고합니다.',BLUE)]
    for i,(title,detail,color) in enumerate(decisions):
        y=826+i*67
        f.rect(820,y-23,4,49,color)
        f.text(838,y,title,24,color,bold=True)
        f.text(838,y+28,detail,20,MUTED,max_width=697)
    f.path([(64,1015),(1536,1015)])
    f.text(64,1048,'미정인 입력  /  모델·데이터·장비·품질 허용폭·반복 수  ·  논의 가능한 초안이며 실행 전 확인이 필요합니다.',20,MUTED)
    f.text(64,1083,'[1] Hu et al. / LoRA v2, abstract (2021)     [2] Dettmers et al. / QLoRA v1, abstract & §2 (2023)',17,MUTED)
    f.text(64,1110,'점선 = 계획 조건 · 화살표 = 비교 절차 · 도형 크기는 메모리 비율이 아닙니다. 자세한 조건은 proposal.md를 확인해 주세요.',16,MUTED)
    f.link(64,1066,400,26,'https://arxiv.org/abs/2106.09685v2')
    f.link(505,1066,660,26,'https://arxiv.org/pdf/2305.14314v1')
    f.text(1536,1083,'HUMAN RESEARCHER / 02',16,GREEN,anchor='end')
    f.save('examples/quantized-adaptation/poster.svg','docs/assets/adaptation-proposal-preview.png','examples/quantized-adaptation/poster.pdf','examples/quantized-adaptation/poster.html')


def decision_map():
    f=Figure(1600,930,'실험이 끝나면 무엇을 결정할까요?',
             '미실행 정밀도 비교에서 측정할 값과 결과별 다음 결정을 연결한 계획도입니다. 품질을 충족하는 메모리 절감, 품질 미달, 큰 불확실성, OOM을 구분합니다.', 'evaluation-map')
    f.label(64,50,'03 / EXPERIMENT TO DECISION')
    f.text(64,124,'Every test should change a decision.',64,serif=True)
    f.text(64,177,'실험이 끝나면 무엇을 결정할까요?',31,bold=True)
    f.text(1536,50,'PLANNED / 미실행',18,BLUE,anchor='end')
    f.label(64,262,'COMPARE')
    f.rect(64,291,333,305,INK,radius=5)
    f.text(89,344,'16-bit vs 4-bit',36,WHITE,serif=True)
    f.lines(89,389,['같은 입력 길이 안에서','같은 어댑터·데이터·예산으로'],23,38,color='#deeadf',max_width=285)
    f.path([(89,469),(370,469)],'#53696a')
    f.lines(89,512,['길이 간 품질 차이를','양자화 효과로 해석하지 않습니다.'],20,32,color='#deeadf',max_width=285)
    f.path([(397,441),(458,441)],GREEN,arrow=True)
    f.label(477,262,'MEASURE')
    f.rect(477,291,350,305,WHITE,LINE,5)
    for i,(a,b) in enumerate([('MEMORY','allocated / reserved 구분'),('QUALITY','동일 평가 예시의 held-out NLL'),('FEASIBILITY','처리량·실패·OOM 기록')]):
        y=339+i*94
        f.label(501,y,a)
        f.text(501,y+35,b,21,MUTED,max_width=303)
    f.path([(827,441),(884,441)],GREEN)
    f.path([(884,328),(884,751)],GREEN)
    f.label(952,262,'INTERPRET → ACT')
    outcomes=[(291,'메모리 감소 + 품질 허용폭 충족','측정한 설정에서 채택을 검토합니다.',GREEN,SAGE),
              (432,'메모리 감소 + 품질 기준 미달','품질 비용을 분석하고 채택을 보류합니다.',RUST,SAND),
              (573,'추정의 불확실성이 큼','계산 예산 안에서 추가 확인 여부를 정합니다.',BLUE,PALE_BLUE),
              (714,'한 비교 조건이 OOM','실행 경계를 보고하고 품질 비교는 유보합니다.',MUTED,'#edf0ed')]
    for y,title,detail,color,fill in outcomes:
        f.path([(884,y+37),(952,y+37)],color,arrow=True)
        f.rect(952,y,584,110,fill,radius=4)
        f.text(974,y+39,title,27,color,bold=True,max_width=540)
        f.text(974,y+78,detail,22,MUTED,max_width=540)
    f.label(64,671,'BEFORE CONFIRMATION')
    f.lines(64,712,['파일럿으로 실행성과 변동을 확인한 뒤,','품질 허용폭·반복 수·계산 상한을 고정합니다.','파일럿 결과와 독립 확인 결과는 구분합니다.'],25,43,max_width=761)
    f.footer('출처: LoRA·QLoRA proposal / 계획된 판단 규칙 · 실제 측정값이나 성능 그래프가 아닙니다.', '03')
    f.save('examples/quantized-adaptation/evaluation.svg','docs/assets/evaluation-map-preview.png')


def meeting():
    f=Figure(1600,1060,'좋은 미팅은 구체적인 질문에서 시작됩니다.',
             '가상의 도서관 안내 문구 연구를 지도교수 미팅용 초안으로 정리한 예제입니다. 문구의 효과는 미확인이고, 결과 변수와 비교 설계, 모집 가능성을 질문으로 연결합니다.', 'meeting-brief')
    f.rect(0,0,20,1060,BLUE)
    f.label(64,50,'04 / RESEARCH MEETING BRIEF',BLUE)
    f.text(64,124,'A draft worth discussing.',68,serif=True)
    f.text(64,179,'답이 없는 부분도, 좋은 질문이 될 수 있습니다.',31,bold=True)
    f.text(1536,50,'FICTIONAL EXAMPLE / 가상 연구',18,BLUE,anchor='end')
    f.path([(64,221),(1536,221)],INK)
    f.label(64,272,'THE QUESTION',BLUE)
    f.lines(64,326,['쉬운 서가 안내 문구가','처음 온 이용자의','책 찾기를 도울까요?'],38,54,bold=True,max_width=590)
    f.text(64,492,'연구자가 선택한 방향',23,BLUE,bold=True)
    f.lines(64,531,['안내 문구만 바꿉니다.','서가 위치·글자 크기·배치는 유지합니다.'],24,36,max_width=600)
    f.path([(64,604),(649,604)])
    f.label(64,647,'WHAT WE KNOW / WHAT WE DO NOT',BLUE)
    f.lines(64,686,['L1에서는 문구와 위치가 함께 바뀌었습니다.','참여 집단도 달라 문구의 효과는 분리되지 않습니다.'],22,35,max_width=600)
    f.rect(64,757,585,97,PALE_BLUE,radius=4)
    f.text(84,795,'현재 상태: 피드백받을 초안',25,BLUE,bold=True)
    f.text(84,832,'평가 설계·장소·참여자 확보는 미정입니다.',21,MUTED)
    f.path([(711,256),(711,854)])
    questions=[(278,'무엇을 주된 결과로 볼까요?','제한 시간 내 성공 여부 / 완료 시간','답이 바꾸는 것: 과제·실패 처리·분석 기준'),
               (474,'문구의 효과를 어떻게 분리할까요?','배치·노출·과제 순서가 만드는 차이','답이 바꾸는 것: 배정 방식과 첫 파일럿'),
               (670,'이 범위로 첫 검증이 가능할까요?','장소 허가·모집 가능성·관련 기관 요건','답이 바꾸는 것: 가능한 규모와 진행 조건')]
    for i,(y,title,issue,decision) in enumerate(questions):
        f.text(760,y+7,f'0{i+1}',40,BLUE,serif=True)
        f.text(832,y,title,28,bold=True,max_width=700)
        f.text(832,y+43,issue,23,MUTED,max_width=695)
        f.text(832,y+85,decision,22,BLUE,max_width=695)
        if i<2:
            f.path([(760,y+136),(1536,y+136)])
    f.rect(64,894,1472,66,INK,radius=4)
    f.text(86,934,'NEXT CHECK',20,'#b6d0be',bold=True)
    f.text(268,934,'허가·모집 가능성을 확인하고 작은 실행성 파일럿을 설계합니다. / 아직 실행하지 않았습니다.',22,WHITE,max_width=1240)
    f.footer('자료: 공개된 합성 평가 입력 meeting-notes.md · 실제 미팅·사용자 연구·지도교수 피드백이 아닙니다.', '04')
    f.save('examples/research-meeting/brief.svg','docs/assets/meeting-brief-preview.png')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    fonts=Path.home()/'Library/Fonts'
    parser.add_argument('--font-regular',type=Path,default=fonts/'NanumSquareR.ttf')
    parser.add_argument('--font-bold',type=Path,default=fonts/'NanumSquareB.ttf')
    args=parser.parse_args()
    if not shutil.which('pdftoppm'):
        parser.error('pdftoppm is required to render and inspect the preview images.')
    for name,path in [('KR',args.font_regular),('KRBold',args.font_bold)]:
        if not path.is_file():
            parser.error(f'Missing font: {path}. Pass a Korean TrueType font with --font-regular and --font-bold.')
        pdfmetrics.registerFont(TTFont(name,str(path)))
    taxonomy()
    poster()
    decision_map()
    meeting()


if __name__=='__main__':
    main()
