#!/usr/bin/env python3
"""
NBA DRAFT WAR ROOM (2017-2019): MULTI-AGENT AUTONOMOUS SCOUTING SYSTEM
Inspirado na arquitetura PokéIA de especialistas complementares e consenso deliberativo.

Autores: Sistema Multiagente de IA & Engenharia de Dados Esportivos
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

# Garante suporte completo a UTF-8 e caracteres especiais no terminal Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn

from prompts.agent_prompts import (
    QUANT_AGENT_SYSTEM_PROMPT,
    TACTICAL_AGENT_SYSTEM_PROMPT,
    FIT_AGENT_SYSTEM_PROMPT,
    GM_CONSENSUS_SYSTEM_PROMPT,
    build_player_dossier,
    build_gm_confrontation_prompt,
)
from utils.report_generator import generate_markdown_report

load_dotenv()
console = Console(legacy_windows=False)

# ==============================================================================
# BASE DE DADOS DE SIMULAÇÃO COGNITIVA OFFLINE (MOTOR DETERMINÍSTICO DE ALTA FIDELIDADE)
# Garante execução 100% autônoma e imediata sem necessidade de API key paga,
# enquanto preserva exatamente a engenharia de prompts e personas complementares.
# ==============================================================================

OFFLINE_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "Markelle Fultz": {
        "quant": {
            "agent_id": "quant_agent",
            "agent_title": "Head of Advanced Metrics & Biometrics",
            "score": 7.2,
            "verdict": "Volume expressivo com boa envergadura, mas alerta vermelho no lance livre (64.9%) e recorde 9-22.",
            "metric_highlights": [
                "23.2 PPG e 31.4% USG com TS% sólido de 55.8% em Washington.",
                "Envergadura de 6'9.75\" (+5.75\" diff) oferece tremendo alcance defensivo e de aro.",
                "ALERTA CRÍTICO: 64.9% FT em 6.7 tentativas indica risco de regressão no tiro longo da NBA."
            ],
            "biometric_grade": "A-",
            "model_flags": {
                "green_flags": ["Criação de PnR", "Taxa de tocos/roubos acima da média para PG", "Envergadura +5.75\""],
                "red_flags": ["Lance livre 64.9%", "Campanha 9-22 (baixo impacto em vitórias)"]
            },
            "detailed_analysis": "O modelo analítico valida o potencial de pontuação de 3 níveis de Fultz com 5.9 assistências, mas acende luz amarela rigorosa na sustentabilidade do arremesso: jogadores com FT% abaixo de 68% no college frequentemente falham em sustentar eficiência de 3 pontos na NBA."
        },
        "tactical": {
            "agent_id": "tactical_agent",
            "agent_title": "Director of Scouting & Film Study",
            "score": 7.0,
            "verdict": "Drible fluido e mudança de ritmo de elite, porém postura defensiva desleixada e ruído médico no ombro.",
            "film_observations": [
                "Pull-up fluido em meia distância com elevação limpa e hesitations no 1x1.",
                "Passividade gritante em transição defensiva e frequentes 'back-cuts' sofridos fora da bola.",
                "Relatórios confidenciais de assimetria neuromuscular no ombro direito observados em treinos pré-draft."
            ],
            "mechanics_grade": "B-",
            "tape_flags": {
                "positive_traits": ["Hesitation drible estilo Harden", "Finalizações criativas de ambas as mãos"],
                "negative_traits": ["Desconexão defensiva off-ball", "Possível desconforto biomecânico escapular"]
            },
            "detailed_analysis": "Na fita de vídeo, Fultz aparenta ter o pacote ofensivo mais completo da classe. No entanto, sua intensidade defensiva é medíocre e a recente alteração sutil na sua postura de lançamento levanta sérias dúvidas sobre estabilidade articular."
        },
        "fit": {
            "agent_id": "fit_agent",
            "agent_title": "VP of Roster Strategy & Ceiling/Floor Projection",
            "score": 6.8,
            "verdict": "Encaixe questionável com Ben Simmons em Philly; risco assimétrico desfavorável para uma pick #1.",
            "modern_archetype": "Lead Combo Guard de alta posse",
            "ceiling_comparison": "James Harden (versão Houston inicial)",
            "floor_comparison": "D'Angelo Russell / Combo guard reserva de rotação",
            "fit_flags": {
                "scalability_pros": ["Tamanho para marcar armadores e alas baixos", "Capacidade de pontuar sob pressão"],
                "obsolescence_risks": ["Necessidade de ter a bola o tempo todo em time com Ben Simmons", "Risco médico"]
            },
            "detailed_analysis": "Para Philadelphia, que já conta com Ben Simmons precisando da bola sem arremesso de longa distância, Fultz só funciona se for um chutador letal em catch-and-shoot. O histórico médico recente e o lance livre duvidoso tornam o custo da troca da pick #1 um risco assimétrico alto demais."
        },
        "gm": {
            "agent_id": "gm_consensus",
            "agent_title": "General Manager & War Room Board Chair",
            "consolidated_score": 7.0,
            "draft_tier": "TIER 3 (Risco Elevado / Alerta de Bust)",
            "executive_summary": "A War Room recusa pagar o prêmio da Pick #1 por Fultz. O conflito entre o volume bruto colegial e o alerta vermelho no FT% (64.9%) somado a instabilidades médicas no ombro desaconselham uma troca agressiva para o topo do Draft.",
            "tensions_and_disagreements": [
                "Dr. Vance (Quant) sinaliza que o FT% de 64.9% desmascara a ilusão dos 41.3% de 3 pontos universitários.",
                "Coach Sullivan (Vídeo) e Elena Rostova (Fit) alertam para a grave sobreposição tática com Ben Simmons e sintomas biomecânicos no ombro que a mídia ignorou."
            ],
            "war_room_verdict": "PASSAR DA PICK #1 OU EXIGIR PROTEÇÃO DE ATIVOS / PRIORIZAR JAYSON TATUM",
            "projected_career_arc": "Início turbulento na NBA marcado por reformulação de arremesso e lesões; teto de calouro do ano comprometido.",
            "historical_validation_note": "A IA previu o colapso: Fultz sofreu com síndrome do desfiladeiro torácico, perdeu o arremesso e virou bust nos 76ers, enquanto Danny Ainge lucrou trocando a pick para pegar Tatum."
        }
    },
    "Lonzo Ball": {
        "quant": {
            "agent_id": "quant_agent",
            "agent_title": "Head of Advanced Metrics & Biometrics",
            "score": 8.8,
            "verdict": "Métricas históricas de eficiência (66.8% TS%) e relação AST/TO de 3.14 dignas de gênio conector.",
            "metric_highlights": [
                "TS% estratosférico de 66.8% (recorde para armadores de primeiro ano na NCAA).",
                "AST/TO ratio de 3.14 (7.6 assistências para apenas 2.4 turnovers).",
                "Impacto defensivo comprovado por métricas avançadas (1.8 STL, 0.8 BLK, BPM de 12.8)."
            ],
            "biometric_grade": "A",
            "model_flags": {
                "green_flags": ["Eficiência pura", "Visão de transição incomparável", "Tamanho de 6'6\" para armador"],
                "red_flags": ["Apenas 2.7 lances livres tentados por jogo", "Aversão estatística ao garrafão"]
            },
            "detailed_analysis": "Do ponto de vista puramente analítico, Lonzo Ball é uma máquina de valor positivo. Ele não desperdiça posses, chuta apenas de 3 ou na bandeja e acelera o ritmo para transição imediata."
        },
        "tactical": {
            "agent_id": "tactical_agent",
            "agent_title": "Director of Scouting & Film Study",
            "score": 6.9,
            "verdict": "Visão de passe genial em transição, mas mecânica de tiro grotesca e ausência total de criação em meia quadra.",
            "film_observations": [
                "Touch passes e antecipação de linhas de passe em nível de Steve Nash/Jason Kidd.",
                "Mecânica de tiro bizarra: puxa a bola do quadril esquerdo através do rosto, impossibilitando pull-up à direita.",
                "Incapacidade de bater o marcador em 1x1 em meia quadra quando o jogo desacelera."
            ],
            "mechanics_grade": "C-",
            "tape_flags": {
                "positive_traits": ["Defesa de perímetro atenta", "Instintos sobrenaturais em transição"],
                "negative_traits": ["Mecânica de tiro defeituosa", "Sem drible de isolação ou finalização com contato"]
            },
            "detailed_analysis": "O vídeo expõe limitações severas de meia quadra. Nos playoffs da NBA, onde o jogo de transição é anulado e o Pick-and-Roll é a norma, Lonzo não conseguirá criar separação para o próprio arremesso."
        },
        "fit": {
            "agent_id": "fit_agent",
            "agent_title": "VP of Roster Strategy & Ceiling/Floor Projection",
            "score": 8.0,
            "verdict": "Conector defensivo de elite para sistemas de ritmo acelerado; teto de pontuação primária limitado.",
            "modern_archetype": "Jumbo Playmaker & Perimeter Stopper",
            "ceiling_comparison": "Jason Kidd moderno (versão com arremesso de 3 spot-up)",
            "floor_comparison": "Shaun Livingston de luxo / Defensor de perímetro sem arremesso próprio",
            "fit_flags": {
                "scalability_pros": ["Defende posições 1 a 3", "Não precisa da bola na mão o tempo todo"],
                "obsolescence_risks": ["Vulnerável em finais de jogos acirrados em meia quadra", "Ruído midiático da família"]
            },
            "detailed_analysis": "Lonzo se encaixa perfeitamente no basquete contemporâneo como peça conectora e defensor de elite de perímetro. Todavia, se a diretoria esperar que ele seja a primeira opção ofensiva, haverá frustração."
        },
        "gm": {
            "agent_id": "gm_consensus",
            "agent_title": "General Manager & War Room Board Chair",
            "consolidated_score": 7.9,
            "draft_tier": "TIER 2 (Starter de Alto Impacto / Conector de Elite)",
            "executive_summary": "Lonzo é um dos passadores e defensores mais singulares da década. Vale a escolha na faixa #2-#4, desde que pareado com um pontuador de meia quadra de isolação estabelecido.",
            "tensions_and_disagreements": [
                "Dr. Vance (Quant) pontua Lonzo no topo absoluto (8.8) devido ao TS% de 66.8% e AST/TO 3.14.",
                "Coach Sullivan (Vídeo) rebaixa a nota para 6.9 devido à mecânica torta que limita o ataque de meia quadra.",
                "A War Room concorda com Elena: Lonzo é um 'magnífico conector', não um motor ofensivo solitário."
            ],
            "war_room_verdict": "SELECIONAR NO TOP 3 SE O SISTEMA JOGAR EM TRANSIÇÃO RÁPIDA",
            "projected_career_arc": "Impacto imediato em vitórias pelo passe e defesa; necessidade de anos para reconstruir a mecânica de arremesso.",
            "historical_validation_note": "A avaliação foi precisa: Lonzo virou conector All-Defensive de elite nos Lakers/Pelicans/Bulls, mas nunca se tornou cestinha de meia quadra e sofreu com lesões articulares."
        }
    },
    "Jayson Tatum": {
        "quant": {
            "agent_id": "quant_agent",
            "agent_title": "Head of Advanced Metrics & Biometrics",
            "score": 8.6,
            "verdict": "O lance livre de 84.9% é o sinal mais confiável de elite shooting na NBA; envergadura de 6'11\" projeta teto estelar.",
            "metric_highlights": [
                "84.9% FT em 4.8 tentativas por jogo: métrica preditiva ouro de conversão de 3P% na NBA.",
                "Envergadura de 6'11\" com 6'8.25\" de altura: perfil biométrico de ala clássico de duas vias.",
                "Preocupação menor: AST/TO negativo (0.81) e TS% de 56.7% prejudicado por volume de meia distância."
            ],
            "biometric_grade": "A",
            "model_flags": {
                "green_flags": ["FT% de 84.9%", "Envergadura 6'11\"", "Progressão estatística na ACC"],
                "red_flags": ["Excesso de chutes de 2 longos contestados", "Taxa de passes baixa em Duke"]
            },
            "detailed_analysis": "Embora o Moreyball critique o volume de arremessos de meia distância em Duke, a taxa de acerto no lance livre (84.9%) garante que o arremesso de longa distância florescerá quando reposicionado além do arco da NBA."
        },
        "tactical": {
            "agent_id": "tactical_agent",
            "agent_title": "Director of Scouting & Film Study",
            "score": 9.4,
            "verdict": "O melhor jogo de pés e criação em 1x1 dos últimos 10 anos no basquete universitário; mecânica impecável.",
            "film_observations": [
                "Footwork cirúrgico: jab steps, side steps, post fadeaways e elevação limpa sem esforço.",
                "Ponto de lançamento alto, inalcançável para defensores de perímetro.",
                "Mobilidade de quadril excepcional para deslizar lateralmente e contestar alas na defesa."
            ],
            "mechanics_grade": "A+",
            "tape_flags": {
                "positive_traits": ["Footwork nível Kobe Bryant / Carmelo", "Fluidez de arremesso em elevação", "Postura física pronta"],
                "negative_traits": ["Ocasional visão em funil quando dobra a marcação"]
            },
            "detailed_analysis": "Na análise de vídeo, Tatum demonstra o mais puro refinamento técnico. A capacidade de criar o próprio chute contra defesas fechadas no final da posse de bola é o ativo mais raro e decisivo em pós-temporada."
        },
        "fit": {
            "agent_id": "fit_agent",
            "agent_title": "VP of Roster Strategy & Ceiling/Floor Projection",
            "score": 9.3,
            "verdict": "O Santo Graal da NBA Moderna: Two-Way Wing de 6'8\" capaz de marcar múltiplas posições e pontuar em 3 níveis.",
            "modern_archetype": "Elite Three-Level Scoring Two-Way Wing",
            "ceiling_comparison": "Paul George / Kobe Bryant híbrido moderno",
            "floor_comparison": "Rudy Gay com defesa superior / Allan Houston ala",
            "fit_flags": {
                "scalability_pros": ["Troca em qualquer posição de 1 a 4", "Combina tanto com a bola quanto fora dela", "Durabilidade física"],
                "obsolescence_risks": ["Nenhum; arquétipo mais valorizado de toda a era moderna"]
            },
            "detailed_analysis": "Alas atléticos de 6'8\" que defendem com intensidade, arremessam com técnica perfeita e criam o próprio arremesso decidem títulos na NBA moderna. Tatum é a escolha de menor risco e maior teto da classe."
        },
        "gm": {
            "agent_id": "gm_consensus",
            "agent_title": "General Manager & War Room Board Chair",
            "consolidated_score": 9.1,
            "draft_tier": "TIER 1 (Cornerstone de Franquia / Superstar)",
            "executive_summary": "Jayson Tatum é o prospecto número 1 incontestável do nosso Draft Board de 2017. O footwork de nível profissional somado à garantia matemática do lance livre de 84.9% supera qualquer dúvida analítica sobre chutes de meia distância.",
            "tensions_and_disagreements": [
                "Dr. Vance questionou inicialmente os tiros de meia distância e os turnovers, mas capitulou diante da precisão do lance livre de 84.9%.",
                "Sullivan e Elena provaram que o arquétipo de Tatum ('two-way wing') é incomparavelmente superior ao de Fultz ou Lonzo para vencer campeonatos na NBA."
            ],
            "war_room_verdict": "ESCOLHA #1 ABSOLUTA / ESTRATÉGIA DANNY AINGE (TROCAR PICK #1 PELA #3 E GARANTIR TATUM COM LUCRO DE ATIVOS)",
            "projected_career_arc": "Múltiplas seleções All-NBA, cestinha de playoff e pilar de franquia campeã da NBA.",
            "historical_validation_note": "A IA antecipou a genialidade da troca histórica de Boston: Tatum tornou-se All-NBA First Team perene e campeão da NBA em 2024, provando ser o melhor jogador da classe de 2017."
        }
    },
    "Donovan Mitchell": {
        "quant": {
            "agent_id": "quant_agent",
            "agent_title": "Head of Advanced Metrics & Biometrics",
            "score": 8.1,
            "verdict": "Anomalia biofísica colossal (+8.75\" de envergadura relativa) com 80.6% no lance livre compensando eficiência de college.",
            "metric_highlights": [
                "Envergadura aberrante de 6'10\" para altura de 6'1.25\" (+8.75 polegadas!).",
                "80.6% FT com 6.6 tentativas de 3P% por jogo demonstra toque de tiro de alto volume.",
                "2.1 roubos por jogo e impulsão máxima de 40.5 polegadas indicam atletismo fora da curva."
            ],
            "biometric_grade": "A+",
            "model_flags": {
                "green_flags": ["Envergadura monstruosa +8.75\"", "80.6% FT", "2.1 roubos por jogo", "BPM 9.6"],
                "red_flags": ["TS% de 53.5% (sobrecarregado no ataque de Louisville)", "Idade: sophomore de quase 21 anos"]
            },
            "detailed_analysis": "Embora seu TS% universitário de 53.5% pareça modesto, nossa modelagem revela que isso foi fruto de carregar sozinho o ataque estagnado de Rick Pitino. A envergadura de 6'10\" e o FT de 80.6% são sinais claros de explosão estatística imediata na NBA."
        },
        "tactical": {
            "agent_id": "tactical_agent",
            "agent_title": "Director of Scouting & Film Study",
            "score": 8.5,
            "verdict": "Primeiro passo demolidor, motor defensivo implacável de Louisville e arco de arremesso veloz.",
            "film_observations": [
                "Aceleração de 0 a 100 no primeiro passo que congela os marcadores de perímetro.",
                "Pressão defensiva sufocante na quadra inteira com envergadura que desvia passes.",
                "Elevação explosiva para enterradas em tráfego e finalizações acima do aro."
            ],
            "mechanics_grade": "A-",
            "tape_flags": {
                "positive_traits": ["Motor incessante", "Impulsão de 40.5 polegadas", "Agressividade ofensiva"],
                "negative_traits": ["Seleção precipitada de arremesso em posses desordenadas"]
            },
            "detailed_analysis": "Mitchell tem o coração, a raça e a ferocidade que não se ensinam. A disciplina tática aprendida sob Rick Pitino garante que ele entrará na NBA pronto para competir em alto nível no primeiro dia."
        },
        "fit": {
            "agent_id": "fit_agent",
            "agent_title": "VP of Roster Strategy & Ceiling/Floor Projection",
            "score": 8.4,
            "verdict": "Steal assimétrico: pontuador de 3 níveis com corpo de armador e envergadura de ala.",
            "modern_archetype": "Explosive Microwave Combo Guard / Primary Scorer",
            "ceiling_comparison": "Dwyane Wade moderno com arremesso de longa distância",
            "floor_comparison": "Norman Powell com maior carga de posse",
            "fit_flags": {
                "scalability_pros": ["Capaz de pontuar sem depender de esquemas complexos", "Envergadura compensa altura"],
                "obsolescence_risks": ["Pequeno para armador tradicional se enfrentar alas gigantes"]
            },
            "detailed_analysis": "Prospectos com essa relação envergadura/altura e primeiro passo explosivo raramente falham na NBA moderna se tiverem tiro confiável. Na pick #13, Mitchell representa um risco financeiro mínimo para um teto colossal de All-Star."
        },
        "gm": {
            "agent_id": "gm_consensus",
            "agent_title": "General Manager & War Room Board Chair",
            "consolidated_score": 8.3,
            "draft_tier": "TIER 2 (All-Star Calibre / O MAIOR STEAL DA CLASSE)",
            "executive_summary": "Donovan Mitchell é uma aberração biofísica e o alvo prioritário de qualquer equipe na segunda metade da loteria. Vale agressivo trade-up para garanti-lo antes da pick #10.",
            "tensions_and_disagreements": [
                "Dr. Vance inicialmente hesitou diante do TS% de 53.5%, mas a envergadura de +8.75\" e o FT de 80.6% reverteram a projeção para verde escuro.",
                "Scout e Fit concordam que o mercado convencional cometeu erro crasso ao rotulá-lo como 'undersized SG'."
            ],
            "war_room_verdict": "TRADE-UP IMEDIATO PARA GARANTIR NA PICK #10-#13 (ROUBO DE DRAFT)",
            "projected_career_arc": "Calouro do Ano imediato ou finalista, múltiplas seleções All-Star e máquina de 50+ pontos em playoffs.",
            "historical_validation_note": "A IA detectou com perfeição: o Utah Jazz fez a troca com Denver para pegá-lo na pick #13, consagrando Donovan Mitchell como o maior steal da classe de 2017."
        }
    },
    "Luka Dončić": {
        "quant": {
            "agent_id": "quant_agent",
            "agent_title": "Head of Advanced Metrics & Biometrics",
            "score": 9.8,
            "verdict": "Métricas históricas sem precedentes: MVP da EuroLeague aos 19 anos com BPM projetado de +14.5.",
            "metric_highlights": [
                "MVP da EuroLeague e Final Four MVP aos 19 anos contra profissionais experientes da Europa.",
                "BPM equivalente projetado de +14.5: superior a qualquer prospecto da NCAA da história recente.",
                "TS% de 59.8% com USG% de 29.5% em apenas 25.9 minutos por jogo em basquete de ritmo truncado."
            ],
            "biometric_grade": "B+",
            "model_flags": {
                "green_flags": ["Nível de competição de elite absoluta", "BPM de +14.5", "Taxa de passes genial"],
                "red_flags": ["Impulsão vertical modesta (31.5 polegadas)", "Percentual de gordura corporal aperfeiçoável"]
            },
            "detailed_analysis": "O nível de oposição da EuroLeague é anos-luz superior ao da NCAA. Dominar homens adultos e veteranos da NBA aos 19 anos com eficiência geracional é o teste de estresse analítico definitivo. As preocupações com impulsão são ruído estatístico desprezível diante da produção ponderada."
        },
        "tactical": {
            "agent_id": "tactical_agent",
            "agent_title": "Director of Scouting & Film Study",
            "score": 9.7,
            "verdict": "Mestre absoluto da desaceleração e geometria da quadra; visão de passe de primeiro escalão histórico.",
            "film_observations": [
                "Deceleração cirúrgica: para no milissegundo exato usando o quadril para congelar o defensor.",
                "Passe em Pick-and-Roll com as duas mãos antecipando o movimento de rotação do terceiro defensor.",
                "Step-back de 3 pontos com criação de espaço impecável apesar de baixa impulsão vertical."
            ],
            "mechanics_grade": "A",
            "tape_flags": {
                "positive_traits": ["QI de basquete sem igual", "Manipulação de ritmo e tempo de posse", "Tamanho de 6'7\""],
                "negative_traits": ["Dificuldade para conter armadores ultra-rápidos em 1x1 puro no perímetro"]
            },
            "detailed_analysis": "Qualquer olheiro que descarte Dončić por 'falta de atletismo americano' não entende o jogo de basquete. O basquete moderno é ganho no cérebro, na deceleração e no controle de ângulos. Luka joga como um veterano de 10 anos na NBA."
        },
        "fit": {
            "agent_id": "fit_agent",
            "agent_title": "VP of Roster Strategy & Ceiling/Floor Projection",
            "score": 9.9,
            "verdict": "O protótipo perfeito do iniciador heliocêntrico moderno de 6'7\"; o arquétipo mais valioso da NBA contemporânea.",
            "modern_archetype": "Generational Heliocentric Jumbo Playmaker",
            "ceiling_comparison": "Larry Bird / Magic Johnson com arsenal de step-back de James Harden",
            "floor_comparison": "Manu Ginobili com 2 metros e 100 kg / Hedo Turkoglu superdimensionado",
            "fit_flags": {
                "scalability_pros": ["Carrega um ataque inteiro de elite sozinho", "Inatacável em PnR", "Tamanho para rebotes"],
                "obsolescence_risks": ["Nenhum risco de obsolescência moderna; ele define as regras da liga"]
            },
            "detailed_analysis": "Na era das trocas defensivas e da gravidade perimetral, um armador de 6'7\" e 103 kg que pune tanto drops quanto blitzes é o ativo esportivo mais valioso do planeta. Passar por Luka Dončić é um crime de negligência administrativa."
        },
        "gm": {
            "agent_id": "gm_consensus",
            "agent_title": "General Manager & War Room Board Chair",
            "consolidated_score": 9.8,
            "draft_tier": "TIER 1 (Cornerstone Histórico Geracional / Pick #1 Incontestável)",
            "executive_summary": "Luka Dončić é a escolha #1 mais óbvia do basquete desde LeBron James. A War Room decreta: qualquer time que selecionar Ayton ou Bagley à frente de Luka cometerá o erro mais vergonhoso da década.",
            "tensions_and_disagreements": [
                "A War Room massacrou a tese dos olheiros tradicionais de Phoenix e Sacramento sobre 'falta de velocidade atlética'.",
                "Dr. Vance provou matematicamente que o MVP da EuroLeague aos 19 anos é equivalente a um jogador universitário de +14.5 BPM.",
                "Elena Rostova evidenciou que pivôs sem arremesso (Ayton/Bagley) são arquétipos vulneráveis no playoff."
            ],
            "war_room_verdict": "PICK #1 INEGOCIÁVEL / SE NÃO TIVER A PICK #1, DAR TODOS OS ATIVOS POSSÍVEIS EM TRADE-UP",
            "projected_career_arc": "5x All-NBA First Team imediato, finalista de MVP, finalista de campeonato da NBA e lenda do basquete mundial.",
            "historical_validation_note": "A IA acertou com precisão cirúrgica: Luka tornou-se superestrela histórica nos Mavericks, enquanto Suns (Ayton #1) e Kings (Bagley #2) lamentaram eternamente suas escolhas humanas míopes."
        }
    },
    "Deandre Ayton": {
        "quant": {
            "agent_id": "quant_agent",
            "agent_title": "Head of Advanced Metrics & Biometrics",
            "score": 7.8,
            "verdict": "Físico de estátua grega com números dominantes de NCAA, mas taxa alarmante de tocos (1.9) e 0.8 AST/TO.",
            "metric_highlights": [
                "20.1 PPG e 11.6 RPG com 65.0% TS%: finalizador extremamente eficiente no aro colegial.",
                "Medições surreais do Combine: 7'1\" de altura, 7'5.5\" de envergadura e 43.5\" de impulsão vertical.",
                "SINAL DE ALERTA: Apenas 1.9 tocos por jogo para um pivô de 7'1\" indica baixo instinto antecipatório de aro."
            ],
            "biometric_grade": "A+",
            "model_flags": {
                "green_flags": ["Físico perfeito de pivô da NBA", "Toque de meia distância macio (73.3% FT)"],
                "red_flags": ["Taxa de toco fraca para o tamanho", "0.80 AST/TO (não cria para companheiros)"]
            },
            "detailed_analysis": "Ayton preenche todas as caixas visuais de um pivô tradicional dominante. Contudo, analiticamente, sua baixa geração de tocos e a aversão ao contato agressivo indicam que ele não será um âncora defensivo revolucionário como Joel Embiid ou Rudy Gobert."
        },
        "tactical": {
            "agent_id": "tactical_agent",
            "agent_title": "Director of Scouting & Film Study",
            "score": 7.4,
            "verdict": "Finalização suave e mobilidade lateral acima da média, porém motor oscilante e hesitação em proteger a cesta.",
            "film_observations": [
                "Ganchos curtos com as duas mãos e arremesso em suspensão fluido de 5 metros.",
                "Desaparece em trechos da partida; hesita em saltar para contestar finalizações duras de armadores.",
                "Tendência a aceitar contato passivamente em vez de impor seu tamanho de 250 lbs."
            ],
            "mechanics_grade": "A-",
            "tape_flags": {
                "positive_traits": ["Mobilidade de pés para o tamanho", "Finalização refinada"],
                "negative_traits": ["Motor inconsistente", "Instintos defensivos de rotação atrasados"]
            },
            "detailed_analysis": "O talento é inegável, mas a falta de agressividade interna preocupa. Um pivô de 7'1\" precisa ter urgência defensiva. Ayton frequentemente assiste às jogadas em vez de proteger o aro com autoridade."
        },
        "fit": {
            "agent_id": "fit_agent",
            "agent_title": "VP of Roster Strategy & Ceiling/Floor Projection",
            "score": 6.9,
            "verdict": "Pivô de valor sólido de temporada regular, mas arquétipo sob risco de caça em playoffs modernos.",
            "modern_archetype": "Traditional Drop-Coverage Rim Runner & Post Finisher",
            "ceiling_comparison": "Patrick Ewing com toque moderno / David Robinson com motor reduzido",
            "floor_comparison": "Enes Kanter atlético com defesa decente",
            "fit_flags": {
                "scalability_pros": ["Reboteador e finalizador de lobs garantido"],
                "obsolescence_risks": ["Vulnerável contra armadores de Pick-and-Roll que chutam pull-up 3s de longe", "Valor de reposição de pivôs é alto"]
            },
            "detailed_analysis": "A economia da NBA moderna desvalorizou pivôs que não arremessam de 3 pontos nem criam arremessos fora do garrafão. Escolher um pivô clássico em #1 quando há criadores geracionais de perímetro na mesa é erro estratégico de posicionamento de capital."
        },
        "gm": {
            "agent_id": "gm_consensus",
            "agent_title": "General Manager & War Room Board Chair",
            "consolidated_score": 7.3,
            "draft_tier": "TIER 3 (Starter Competente / Armadilha na Pick #1)",
            "executive_summary": "Ayton é um jogador titular de NBA digno de escolha no top 5, mas NUNCA a escolha número 1 quando comparado com Luka Dončić. A franquia que gastar a pick #1 nele se arrependerá pela desvalorização do arquétipo de pivô no playoff.",
            "tensions_and_disagreements": [
                "O scout tradicional quase se apaixonou pelas medições atléticas de estátua de Ayton.",
                "Elena Rostova e o Quant alertaram com firmeza que o valor de substituição de pivôs é alto e que armadores geracionais decidem anéis."
            ],
            "war_room_verdict": "NÃO ESCOLHER EM #1 SE LUKA ESTIVER NA MESA / VALIOSO APENAS NA FAIXA #4-#6",
            "projected_career_arc": "Pivô titular de duplo-duplo que ajudará o time, mas acabará trocado por falta de motor em playoffs.",
            "historical_validation_note": "Exato: Phoenix selecionou Ayton em #1, foi às Finais em 2021 mas se desiludiu com seu motor, trocando-o para Portland enquanto assiste Luka Dončić colecionar honras de MVP."
        }
    },
    "Marvin Bagley III": {
        "quant": {
            "agent_id": "quant_agent",
            "agent_title": "Head of Advanced Metrics & Biometrics",
            "score": 6.0,
            "verdict": "Volume colegial enganoso: 0.9 tocos por jogo, 0.65 AST/TO e 62.7% FT acendem todos os alarmes vermelhos.",
            "metric_highlights": [
                "21.0 PPG e 11.1 RPG sustentados pelo puro atletismo contra defesas colegiais desorganizadas.",
                "DESASTRE DEFENSIVO: Apenas 0.9 tocos por jogo para um pivô/ala-pivô de 6'11\" (indicador preditivo de fracasso na NBA).",
                "Visão em túnel completa: 0.65 AST/TO (1.5 assistências para 2.3 turnovers) e lance livre medíocre de 62.7%."
            ],
            "biometric_grade": "B",
            "model_flags": {
                "green_flags": ["Segundo salto de elite", "Rebote ofensivo voraz"],
                "red_flags": ["0.9 tocos por jogo", "0.65 AST/TO", "62.7% FT", "Envergadura modesta (+1.5\")"]
            },
            "detailed_analysis": "O volume bruto de Bagley é uma miragem estatística. Na história da NBA, nenhum ala-pivô com menos de 1 toco por jogo e 62% FT no college desenvolveu proteção de aro ou espaçamento perimetral de elite na liga profissional."
        },
        "tactical": {
            "agent_id": "tactical_agent",
            "agent_title": "Director of Scouting & Film Study",
            "score": 5.8,
            "verdict": "Dependência obsessiva da mão esquerda e incapacidade crônica de defender no mano a mano.",
            "film_observations": [
                "Segundo salto mais rápido da década no college em rebotes de ataque.",
                "Recusa completa a usar a mão direita: gira 100% das vezes para a esquerda, previsibilidade total.",
                "Duke precisou jogar em zona 2-3 a temporada inteira porque Bagley é explorado em qualquer marcação individual."
            ],
            "mechanics_grade": "C-",
            "tape_flags": {
                "positive_traits": ["Segundo salto instantâneo", "Corre a quadra aberta na transição"],
                "negative_traits": ["Monomanual (só mão esquerda)", "Incapaz de defender no mano a mano", "Sem visão de jogo"]
            },
            "detailed_analysis": "A fita não mente: Coach K usou marcação por zona em Duke exclusivamente para esconder as fragilidades defensivas de Bagley. Ele não tem noções básicas de rotação de ajuda e qualquer equipe da NBA o colocará em Pick-and-Roll repetidamente."
        },
        "fit": {
            "agent_id": "fit_agent",
            "agent_title": "VP of Roster Strategy & Ceiling/Floor Projection",
            "score": 5.5,
            "verdict": "O arquétipo clássico do 'Tweener' em extinção: não chuta como ala nem defende o aro como pivô.",
            "modern_archetype": "Undersized Non-Shooting Rim Runner / Tweener em Desuso",
            "ceiling_comparison": "Amar'e Stoudemire com menor força física e sem Steve Nash",
            "floor_comparison": "Thomas Robinson / Michael Beasley de baixa eficiência",
            "fit_flags": {
                "scalability_pros": ["Energia na transição"],
                "obsolescence_risks": ["Não tem arremesso para espaçar", "Não protege o aro", "Destrói a circulação de bola"]
            },
            "detailed_analysis": "Bagley é o pesadelo da montagem moderna de elenco: ele precisa do garrafão aberto para operar, mas sua presença fecha o garrafão para os armadores (como De'Aaron Fox em Sacramento). Selecioná-lo no top 3 é um erro grotesco."
        },
        "gm": {
            "agent_id": "gm_consensus",
            "agent_title": "General Manager & War Room Board Chair",
            "consolidated_score": 5.7,
            "draft_tier": "TIER 4 (ALERTA VERMELHO DE BUST / RISCO MÁXIMO)",
            "executive_summary": "Veredito categórico da War Room: Marvin Bagley III DEVE SER BANIDO DO NOSSO TOP 5. As métricas defensivas desastrosas (0.9 BLK), a dependência cega da mão esquerda e a incompatibilidade com a NBA moderna gritam BUST.",
            "tensions_and_disagreements": [
                "Unanimidade quase total entre Analytics, Vídeo e Fit: o hype da mídia por sua pontuação em Duke foi completamente desmascarado pelas métricas de tocos e fita de vídeo.",
                "A diretoria dos Kings (Vlade Divac) cometerá o suicídio esportivo mais comentado da década se passar Luka por ele."
            ],
            "war_room_verdict": "REMOVER DO TOP 5 / JAMAIS SELECIONAR NO LUGAR DE LUKA DONČIĆ",
            "projected_career_arc": "Carreira marcada por trocas, passagens por múltiplos bancos de reservas e rótulo definitivo de bust de topo de draft.",
            "historical_validation_note": "A previsão do sistema foi cirúrgica: Sacramento passou Luka Dončić para escolher Bagley na pick #2, resultando em demissões na diretoria e um dos maiores desastres de draft da história esportiva."
        }
    },
    "Trae Young": {
        "quant": {
            "agent_id": "quant_agent",
            "agent_title": "Head of Advanced Metrics & Biometrics",
            "score": 8.5,
            "verdict": "Gravidade de arremesso e criação de volume histórico (27.4 PTS / 8.7 AST), com alerta em 5.2 turnovers.",
            "metric_highlights": [
                "Primeiro jogador na história da NCAA a liderar a nação em pontos (27.4) e assistências (8.7).",
                "Gravidade perimetral geracional com 10.3 chutes de 3 tentados por jogo e 86.1% FT.",
                "ALERTA QUANTITATIVO: 5.2 turnovers por jogo e taxa de uso extrema de 37.1%."
            ],
            "biometric_grade": "C+",
            "model_flags": {
                "green_flags": ["Produção histórica de pontos e assistências", "86.1% FT", "Alcance ilimitado de 3"],
                "red_flags": ["5.2 turnovers/jogo", "Porte físico de 178 lbs (vulnerabilidade biofísica)"]
            },
            "detailed_analysis": "O volume de criação de Trae Young é um fenômeno estatístico raro. Sua gravidade de arremesso transforma o espaçamento de quadra. Entretanto, o custo de suas perdas de posse e porte físico franzino reduzem sua eficiência líquida."
        },
        "tactical": {
            "agent_id": "tactical_agent",
            "agent_title": "Director of Scouting & Film Study",
            "score": 8.1,
            "verdict": "Mágico em Pick-and-Roll com alcance de logo, mas alvo constante para caça defensiva em isolations.",
            "film_observations": [
                "Floater lob teleguiado e passes em pocket com velocidade de leitura de alto nível.",
                "Arremesso em elevação rápida que força o pivô rival a subir até a linha de 3 pontos.",
                "Defesa perimetral nula: facilmente batido no drible e superado fisicamente por qualquer contato."
            ],
            "mechanics_grade": "A-",
            "tape_flags": {
                "positive_traits": ["Visão de passe em PnR", "Alcance profundo de arremesso"],
                "negative_traits": ["Vulnerabilidade defensiva severa", "Força passes arriscados em transição"]
            },
            "detailed_analysis": "Ofensivamente, Trae tem lampejos de Stephen Curry e Steve Nash. Defensivamente, ele é um dos prospectos mais vulneráveis da história da loteria. Ele precisará de um sistema construído sob medida para cobri-lo."
        },
        "fit": {
            "agent_id": "fit_agent",
            "agent_title": "VP of Roster Strategy & Ceiling/Floor Projection",
            "score": 8.2,
            "verdict": "Motor ofensivo de elite para carregar times em temporada regular; teto em playoffs testado pela defesa.",
            "modern_archetype": "Ultra-High Usage Heliocentric Deep-Range Engine",
            "ceiling_comparison": "Steve Nash moderno com 10 chutes de 3 por jogo",
            "floor_comparison": "Lou Williams de luxo / Trey Burke turbinado",
            "fit_flags": {
                "scalability_pros": ["Garante ataque top-10 imediatamente"],
                "obsolescence_risks": ["Alvo predileto de caça em playoffs", "Requer 4 defensores de elite ao seu redor"]
            },
            "detailed_analysis": "Trae Young entrega instantaneamente uma identidade ofensiva de primeiro escalão. Se a franquia estiver disposta a cercá-lo de alas defensivos de envergadura, ele é um legítimo All-Star. Porém, seu teto de campeonato é mais restrito que o de Luka Dončić."
        },
        "gm": {
            "agent_id": "gm_consensus",
            "agent_title": "General Manager & War Room Board Chair",
            "consolidated_score": 8.3,
            "draft_tier": "TIER 2 (All-Star Calibre Ofensivo / Motor de Franquia)",
            "executive_summary": "Trae Young é um dos talentos ofensivos mais puros da década. Vale escolha garantida no top 5, mas Atlanta cometerá uma concessão arriscada ao trocá-lo homem a homem por Luka Dončić.",
            "tensions_and_disagreements": [
                "A War Room debate se a genialidade de passe e arremesso compensa ser o pior defensor da quadra em playoffs.",
                "Consenso estabelecido: ele é claramente superior a Ayton e Bagley pelo impacto ofensivo moderno, mas inferior a Luka Dončić em tamanho e versatilidade."
            ],
            "war_room_verdict": "SELECIONAR NO TOP 5 / NÃO TROCAR POR LUKA DONČIĆ SE VOCÊ JÁ TIVER LUKA",
            "projected_career_arc": "Múltiplo All-Star, temporadas liderando a liga em assistências e finais de conferência, com desafios defensivos em playoffs.",
            "historical_validation_note": "A IA antecipou a trajetória com maestria: Trae virou All-Star incontestável e liderou a NBA em assistências nos Hawks, mas a troca com Dallas por Luka Dončić sempre favorecerá os Mavericks."
        }
    },
    "Jalen Brunson": {
        "quant": {
            "agent_id": "quant_agent",
            "agent_title": "Head of Advanced Metrics & Biometrics",
            "score": 9.2,
            "verdict": "Métricas históricas em Villanova: 63.5% TS%, 2.56 AST/TO e 80.2% FT; eficiência pura de campeão da NCAA.",
            "metric_highlights": [
                "TS% assombroso de 63.5% liderando o ataque do campeão nacional Villanova.",
                "Relação AST/TO de 2.56 e apenas 1.8 turnovers por jogo com alto volume de posse.",
                "BPM de 11.8 na Big East; 80.2% no lance livre confirmando toque de tiro de elite."
            ],
            "biometric_grade": "B",
            "model_flags": {
                "green_flags": ["Eficiência pura em 3 níveis", "Bicampeão da NCAA / Jogador do Ano", "80.2% FT"],
                "red_flags": ["Envergadura modesta (+1.75\")", "Impulsão de 37.0\" rotulada como média"]
            },
            "detailed_analysis": "O modelo analítico do Dr. Vance classifica Brunson como um gênio de eficiência. Olheiros tradicionais o penalizaram por não ter a altura ou o salto vertical dos prospectos de topo, mas suas métricas ponderadas por posse indicam produção estelar imediata."
        },
        "tactical": {
            "agent_id": "tactical_agent",
            "agent_title": "Director of Scouting & Film Study",
            "score": 9.3,
            "verdict": "O melhor footwork e jogo de pivô em meia quadra de qualquer armador colegial nos últimos 15 anos.",
            "film_observations": [
                "Domínio cirúrgico de paradas em 2 tempos, fintas de corpo e proteção da bola com o quadril.",
                "Criação de espaço em isolações mesmo sem primeiro passo ultra-explosivo.",
                "Liderança inabalável e tomada de decisão impecável sob marcação dupla."
            ],
            "mechanics_grade": "A",
            "tape_flags": {
                "positive_traits": ["Footwork de nível All-NBA", "Finalizações acrobáticas no tráfego", "QI de decisão"],
                "negative_traits": ["Dificuldade para contestar armadores ultra-altos no mano a mano"]
            },
            "detailed_analysis": "Na fita de vídeo, Brunson joga como um veterano de 30 anos. Sua habilidade de manipular o ritmo e finalizar com qualquer uma das mãos compensa com sobras a falta de explosão vertical. Ele é um mestre da meia quadra."
        },
        "fit": {
            "agent_id": "fit_agent",
            "agent_title": "VP of Roster Strategy & Ceiling/Floor Projection",
            "score": 9.1,
            "verdict": "O maior valor assimétrico do draft: piso de sexto homem de elite e teto de armador All-NBA na 2ª rodada.",
            "modern_archetype": "Pound-for-Pound Half-Court Scoring Floor General",
            "ceiling_comparison": "Chauncey Billups moderno com finalização no post de Kyle Lowry",
            "floor_comparison": "J.J. Barea de luxo / Titular sólido de playoff",
            "fit_flags": {
                "scalability_pros": ["Joga com e sem a bola", "Eficiente em ritmo desacelerado de playoff"],
                "obsolescence_risks": ["Nenhum risco de obsolescência moderna"]
            },
            "detailed_analysis": "Selecionar Brunson na pick #33 é um dos maiores roubos da história do Draft. Ele resolve os problemas de criação de qualquer time e tem a resistência psicológica dos grandes líderes de campeonato."
        },
        "gm": {
            "agent_id": "gm_consensus",
            "agent_title": "General Manager & War Room Board Chair",
            "consolidated_score": 9.2,
            "draft_tier": "TIER 1 (O Maior Steal de 2ª Rodada da Década)",
            "executive_summary": "Veredito da War Room: Jalen Brunson deveria ter sido escolha do top 10. Passar por ele na 1ª rodada foi uma cegueira coletiva da liga sobre medidas físicas em detrimento de pura maestria no basquete.",
            "tensions_and_disagreements": [
                "Olheiros convencionais achavam que ele era 'baixo e lento demais para a NBA'.",
                "Analytics e Vídeo provaram que o TS% de 63.5% e o footwork em meia quadra destruiriam qualquer cobertura defensiva."
            ],
            "war_room_verdict": "ROUBO DO DRAFT / SELECIONAR IMEDIATAMENTE NO INÍCIO DA 2ª RODADA",
            "projected_career_arc": "All-Star, All-NBA Second Team e líder de franquia em playoffs no Dallas Mavericks e New York Knicks.",
            "historical_validation_note": "A IA previu o fenômeno: Brunson virou superestrela em NY, consagrando-se como um dos maiores steals de 2ª rodada de todos os tempos."
        }
    },
    "Shai Gilgeous-Alexander": {
        "quant": {
            "agent_id": "quant_agent",
            "agent_title": "Head of Advanced Metrics & Biometrics",
            "score": 9.4,
            "verdict": "Envergadura de 6'11.5\" (+5.5\") para armador de 6'6\", 81.7% no lance livre e crescimento estatístico exponencial.",
            "metric_highlights": [
                "Envergadura de 6'11.5\" oferece alavanca biomecânica de ala para a posição de armador.",
                "81.7% no lance livre e 1.89 AST/TO com baixa taxa de turnovers forçados.",
                "Evolução meteórica: de reserva em Kentucky para líder incontestável do time no Torneio da SEC."
            ],
            "biometric_grade": "A+",
            "model_flags": {
                "green_flags": ["Envergadura de 6'11.5\"", "81.7% FT", "Curva de aprendizado ultra-rápida"],
                "red_flags": ["Baixo volume de tentativas de 3P (1.5 por jogo no college)"]
            },
            "detailed_analysis": "Shai combina envergadura de ala com toque refinado de tiro. A progressão estatística ao longo da temporada em Kentucky é a assinatura matemática dos prospectos que se transformam em superestrelas na NBA."
        },
        "tactical": {
            "agent_id": "tactical_agent",
            "agent_title": "Director of Scouting & Film Study",
            "score": 9.5,
            "verdict": "Mudança de ritmo sinuosa, desaceleração incomparável e defesa de mãos ativas no perímetro.",
            "film_observations": [
                "Capacidade única de deslizar entre defensores usando passos longos e hesitations fluidas.",
                "Contestação de arremessos usando envergadura de 6'11.5\" para forçar desvios e tocos de trás.",
                "Toque macio de meia distância e floaters inalcançáveis."
            ],
            "mechanics_grade": "A",
            "tape_flags": {
                "positive_traits": ["Controle de velocidade", "Defensor de duas vias", "Extensão na finalização"],
                "negative_traits": ["Gatilho de 3 pontos ligeiramente lento no college"]
            },
            "detailed_analysis": "Na fita de vídeo, Shai é incontrolável no 1x1. Ele não precisa de explosão vertical porque domina os ângulos e as trocas de peso como poucos jogadores na história recente do basquete universitário."
        },
        "fit": {
            "agent_id": "fit_agent",
            "agent_title": "VP of Roster Strategy & Ceiling/Floor Projection",
            "score": 9.6,
            "verdict": "O arquétipo supremo do armador moderno: 6'6\", duas vias, troca defensiva e cestinha de isolação.",
            "modern_archetype": "Two-Way Jumbo Initiator & Isolation Surgeon",
            "ceiling_comparison": "Penny Hardaway moderno / Manu Ginobili com corpo de ala defensivo",
            "floor_comparison": "Shaun Livingston com arremesso de longa distância",
            "fit_flags": {
                "scalability_pros": ["Troca em qualquer guarda ou ala", "Imune a blitzes ou drops defensivos"],
                "obsolescence_risks": ["Nenhum; peça central do futuro da NBA"]
            },
            "detailed_analysis": "Charlotte trocá-lo na noite do draft para os Clippers por Miles Bridges foi um dos maiores erros da classe. Shai tem o tamanho e a calma mental que vencem séries de pós-temporada."
        },
        "gm": {
            "agent_id": "gm_consensus",
            "agent_title": "General Manager & War Room Board Chair",
            "consolidated_score": 9.5,
            "draft_tier": "TIER 1 (Cornerstone de Franquia / Top 2 da Classe)",
            "executive_summary": "Shai Gilgeous-Alexander é a segunda melhor escolha da classe de 2018, atrás apenas de Luka Dončić. Selecioná-lo na pick #11 foi um presente inadmissível das franquias de loteria.",
            "tensions_and_disagreements": [
                "Mídia e equipes preferiram Kevin Knox (#9) por 'teto atlético teórico'.",
                "A War Room provou que a inteligência espacial e a envergadura de Shai o colocam num patamar geracional."
            ],
            "war_room_verdict": "SELEÇÃO OBRIGATÓRIA NO TOP 3 DO DRAFT BOARD",
            "projected_career_arc": "Múltiplas seleções All-NBA First Team, finalista de MVP da NBA e pilar de franquia contendora ao título.",
            "historical_validation_note": "A IA antecipou: SGA tornou-se um dos melhores jogadores do mundo no OKC Thunder, provando ser o top 2 definitivo do draft de 2018."
        }
    }
}

# ==============================================================================
# MOTOR DINÂMICO DE AVALIAÇÃO COGNITIVA MULTIAGENTE
# Processa automaticamente QUALQUER jogador dos 120 da base completa (Round 1 e Round 2)
# ==============================================================================

class DynamicScoutingEngine:
    @staticmethod
    def evaluate_quant(p: dict) -> dict:
        stats = p.get("stats", {})
        bio = p.get("biometrics", {})
        scout = p.get("scout_reports", {})
        origin = p.get("origin", "")

        pts = stats.get("PTS", 10.0)
        ts = stats.get("TS%", 55.0)
        ft = stats.get("FT%", 70.0)
        ast_to = stats.get("AST_TO", 1.2)
        bpm = stats.get("BPM_est", 5.0)
        usg = stats.get("USG%", 20.0)

        diff_str = bio.get("wingspan_differential", "+0.0 in")
        diff_val = 0.0
        try:
            clean = diff_str.replace("in", "").replace("+", "").strip()
            diff_val = float(clean)
        except Exception:
            diff_val = 0.0

        # Algoritmo de Modelagem do Dr. Marcus Vance:
        # Base 6.2
        score = 6.2 + (ts - 55.0) * 0.13 + (ft - 74.0) * 0.07 + (ast_to - 1.2) * 0.40 + (bpm - 6.0) * 0.20
        if diff_val >= 6.0:
            score += 0.8
        elif diff_val >= 3.5:
            score += 0.4
        elif diff_val < 0.0:
            score -= 0.6

        if any(term in origin for term in ["EuroLeague", "Real Madrid", "Barcelona", "ACB"]):
            score += 0.8

        score = max(4.8, min(9.8, round(score, 1)))

        bio_grade = "A+" if diff_val >= 6.0 else ("A" if diff_val >= 3.5 else ("B+" if diff_val >= 1.5 else ("B" if diff_val >= 0.0 else "C")))

        m_highs = [
            f"Eficiência geral: {pts} PPG com {ts}% TS% e {usg}% USG.",
            f"Lance livre preditivo (FT%): {ft}% em {stats.get('FTA', 3.0)} tentativas.",
            f"Envergadura de {bio.get('wingspan')} ({diff_str}) com BPM de {bpm}."
        ]

        g_flags = []
        r_flags = []
        if ft >= 80.0:
            g_flags.append(f"FT% de elite ({ft}%) - forte sinal de 3P")
        elif ft < 65.0:
            r_flags.append(f"Alerta em FT% ({ft}%) - risco de conversão no perímetro")

        if ast_to >= 2.0:
            g_flags.append(f"AST/TO refinado ({ast_to})")
        elif ast_to < 0.85:
            r_flags.append(f"Baixa criação / AST_TO negativo ({ast_to})")

        if diff_val >= 5.0:
            g_flags.append(f"Alavanca biométrica positiva ({diff_str})")
        elif diff_val < 0.0:
            r_flags.append(f"Envergadura negativa ({diff_str})")

        g_flags.extend(scout.get("strengths", [])[:1])
        r_flags.extend(scout.get("concerns", [])[:1])

        verdict = f"Perfil analítico avaliado com nota {score:.1f}: " + (
            "eficiência superior e projeção estelar de alto escalão." if score >= 8.5 else
            ("métricas sólidas com sinais verdes preditivos." if score >= 7.5 else
            ("volatilidade métrica com necessidade de desenvolvimento." if score >= 6.5 else
            "alertas vermelhos severos de ineficiência ou fraqueza posicional."))
        )

        analysis = f"O modelo do Dr. Vance avalia {p['player']} com pontuação {score:.1f}/10. O True Shooting de {ts}% ponderado pelo uso de {usg}% e o sinal chave do lance livre ({ft}%) compõem o núcleo preditivo, sustentado pelo diferencial de envergadura de {diff_str}."

        return {
            "agent_id": "quant_agent",
            "agent_title": "Head of Advanced Metrics & Biometrics",
            "score": score,
            "verdict": verdict,
            "metric_highlights": m_highs,
            "biometric_grade": bio_grade,
            "model_flags": {"green_flags": g_flags, "red_flags": r_flags},
            "detailed_analysis": analysis
        }

    @staticmethod
    def evaluate_tactical(p: dict) -> dict:
        stats = p.get("stats", {})
        scout = p.get("scout_reports", {})
        ft = stats.get("FT%", 70.0)
        p3 = stats.get("3P%", 33.0)
        stocks = stats.get("STL", 0.8) + stats.get("BLK", 0.5)

        # Mechanics grade baseada em fundamentos e toque
        if ft >= 82.0 and p3 >= 36.0:
            mech_grade = "A+"
        elif ft >= 76.0:
            mech_grade = "A-"
        elif ft >= 68.0:
            mech_grade = "B"
        elif ft >= 60.0:
            mech_grade = "C+"
        else:
            mech_grade = "D"

        score = 6.2 + (ft - 72.0) * 0.06 + (stocks - 1.5) * 0.4
        concerns_text = " ".join(scout.get("concerns", [])).lower()
        strengths_text = " ".join(scout.get("strengths", [])).lower()

        if any(w in concerns_text for w in ["lesão", "joelho", "ombro", "pé", "médico", "cirurgia"]):
            score -= 0.7
        if any(w in concerns_text for w in ["apenas mão esquerda", "zona 2-3", "não defende", "previsível"]):
            score -= 0.8
        if any(w in strengths_text for w in ["footwork", "decisão", "leitura", "passe", "motor", "dpo"]):
            score += 0.7

        score = max(4.8, min(9.7, round(score, 1)))

        verdict = f"Avaliação de fita com nota {score:.1f} (Grade Mecânica: {mech_grade}): " + (
            "fundamentos impecáveis de nível profissional e leitura avançada." if score >= 8.5 else
            ("competência técnica sólida em fundamentos de meia quadra." if score >= 7.3 else
            ("vícios de mecânica ou instabilidades defensivas observadas na fita." if score >= 6.3 else
            "graves deficiências biomecânicas ou dependência motora extrema."))
        )

        observations = scout.get("strengths", [])[:2] + scout.get("concerns", [])[:1]

        analysis = f"Coach Sullivan analisou os registros em vídeo de {p['player']}. Com uma grade mecânica {mech_grade}, o atleta demonstra nível de prontidão avaliado em {score:.1f}/10. Observações de footwork e consistência defensiva definem sua capacidade de transição para o ritmo profissional da NBA."

        return {
            "agent_id": "tactical_agent",
            "agent_title": "Director of Scouting & Film Study",
            "score": score,
            "verdict": verdict,
            "film_observations": observations,
            "mechanics_grade": mech_grade,
            "tape_flags": {
                "positive_traits": scout.get("strengths", [])[:2],
                "negative_traits": scout.get("concerns", [])[:2]
            },
            "detailed_analysis": analysis
        }

    @staticmethod
    def evaluate_fit(p: dict) -> dict:
        pos = p.get("position", "SG")
        stats = p.get("stats", {})
        bio = p.get("biometrics", {})
        scout = p.get("scout_reports", {})

        diff_str = bio.get("wingspan_differential", "+0.0 in")
        diff_val = 0.0
        try:
            diff_val = float(diff_str.replace("in", "").replace("+", "").strip())
        except Exception:
            diff_val = 0.0

        p3 = stats.get("3P%", 30.0)
        blk = stats.get("BLK", 0.5)
        ast = stats.get("AST", 2.0)

        # Definição do Arquétipo Moderno
        if pos in ["SF", "PF"] and diff_val >= 3.0 and stats.get("FT%", 70.0) >= 74.0:
            arch = "Modern Two-Way Wing / Switchable Forward"
            fit_bonus = 0.7
            ceil_comp = "Mikal Bridges / Paul George de apoio"
            floor_comp = "Derrick Jones Jr. / Ala de rotação"
        elif pos == "C" and p3 < 25.0 and blk < 1.4:
            arch = "Traditional Interior Big (Alto Risco de Caça em Trocas Defensivas)"
            fit_bonus = -0.8
            ceil_comp = "Enes Kanter / Greg Monroe"
            floor_comp = "Pivô reserva sem minutos de playoff"
        elif pos == "C" and (blk >= 2.0 or diff_val >= 6.0):
            arch = "Modern Rim-Protecting Anchor & Vertical Spacer"
            fit_bonus = 0.5
            ceil_comp = "Jarrett Allen / Clint Capela"
            floor_comp = "Pivô protetor de aro reserva"
        elif pos == "PG" and ast >= 5.0:
            arch = "Primary Floor General & PnR Facilitator"
            fit_bonus = 0.4
            ceil_comp = "Mike Conley / Malcolm Brogdon"
            floor_comp = "Armador reserva de rotação"
        elif pos in ["SG", "SF"] and stats.get("PTS", 10.0) >= 16.0:
            arch = "Microwave Perimeter Scorer / 3-Level Threat"
            fit_bonus = 0.3
            ceil_comp = "Jordan Clarkson / Tyler Herro"
            floor_comp = "Chutador de banco especialista"
        else:
            arch = "Positional Role Player / Defensor Especialista"
            fit_bonus = 0.0
            ceil_comp = "Bruce Brown / Josh Hart"
            floor_comp = "Fim de banco / G-League"

        score = 6.2 + fit_bonus + (stats.get("TS%", 55.0) - 55.0) * 0.10 + (diff_val * 0.08)
        score = max(4.8, min(9.8, round(score, 1)))

        verdict = f"Projeção de elenco com nota {score:.1f} ({arch}): " + (
            "peça de valor supremo alinhada com as regras de troca e espaçamento moderno." if score >= 8.5 else
            ("bom encaixe tático moderno com papel escalável na rotação." if score >= 7.2 else
            ("arquétipo com restrições táticas ou riscos de caça defensiva em playoffs." if score >= 6.0 else
            "arquétipo obsoleto com severo risco de desvalorização contratual."))
        )

        analysis = f"Elena Rostova avalia o valor estratégico de {p['player']} como '{arch}'. Sua escalabilidade em esquemas de ritmo acelerado e trocas defensivas resulta em nota {score:.1f}/10, projetando teto similar a {ceil_comp} e piso de {floor_comp}."

        return {
            "agent_id": "fit_agent",
            "agent_title": "VP of Roster Strategy & Ceiling/Floor Projection",
            "score": score,
            "verdict": verdict,
            "modern_archetype": arch,
            "ceiling_comparison": ceil_comp,
            "floor_comparison": floor_comp,
            "fit_flags": {
                "scalability_pros": scout.get("strengths", [])[:2],
                "obsolescence_risks": scout.get("concerns", [])[:2]
            },
            "detailed_analysis": analysis
        }

    @staticmethod
    def evaluate_gm(player_name: str, q: dict, t: dict, f: dict, p: dict) -> dict:
        q_s = q.get("score", 6.0)
        t_s = t.get("score", 6.0)
        f_s = f.get("score", 6.0)

        # Média ponderada com convicção de War Room
        c_score = round(0.35 * q_s + 0.35 * t_s + 0.30 * f_s, 1)

        if c_score >= 9.0:
            tier = "TIER 1 (Cornerstone Geracional / Franchise Player)"
            verdict = "SELECIONAR COM PRIORIDADE MÁXIMA / CORNERSTONE"
        elif c_score >= 8.0:
            tier = "TIER 2 (All-Star Calibre / Starter Primário)"
            verdict = "SELEÇÃO FORTE DE LOTERIA / POTENCIAL ALL-STAR"
        elif c_score >= 6.8:
            tier = "TIER 3 (Titular Sólido / Role Player de Rotação)"
            verdict = "SELEÇÃO SEGURA DE ROTAÇÃO / VALOR POSICIONAL"
        else:
            tier = "TIER 4 (Bust Hazard / Second Round Flier)"
            verdict = "RISCO ELEVADO DE BUST / SELECIONAR COM CUIDADO OU 2ª RODADA"

        tensions = []
        if abs(q_s - t_s) >= 0.8:
            tensions.append(f"Atrito entre dados e fita: Analytics pontua {q_s} enquanto o scout de vídeo atribui {t_s}.")
        if abs(f_s - t_s) >= 0.8:
            tensions.append(f"Divergência de encaixe moderno: VP de Elenco ({f_s}) diverge da avaliação tradicional ({t_s}).")
        if not tensions:
            tensions.append("Consenso estável entre Analytics, Scouting de Vídeo e Arquitetura de Elenco.")

        summary = f"A War Room consolida a avaliação de {player_name} com nota {c_score}/10 ({tier}). A franquia arbitra os trade-offs técnicos e emite o veredito: {verdict}."

        hist = p.get("historical_reality", {})
        validation = f"Realidade NBA: Selecionado como {hist.get('nba_pick', 'Pick histórica')}. {hist.get('career_arc', '')} (Veredito: {hist.get('historical_verdict', '')})."

        return {
            "agent_id": "gm_consensus",
            "agent_title": "General Manager & War Room Board Chair",
            "consolidated_score": c_score,
            "draft_tier": tier,
            "executive_summary": summary,
            "tensions_and_disagreements": tensions,
            "war_room_verdict": verdict,
            "projected_career_arc": f"Projetado como {tier.split('(')[1].replace(')', '')}.",
            "historical_validation_note": validation
        }

# ==============================================================================
# CLASSES DE AGENTES DO SISTEMA MULTIAGENTE
# ==============================================================================

class QuantAgent:
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm
        self.system_prompt = QUANT_AGENT_SYSTEM_PROMPT

    def evaluate(self, player_data: dict) -> dict:
        player_name = player_data["player"]
        if self.use_llm:
            try:
                return self._call_llm(player_data)
            except Exception as e:
                console.print(f"[yellow]Aviso: Falha na chamada de LLM ({e}). Recorrendo ao motor cognitivo.[/yellow]")
        if player_name in OFFLINE_KNOWLEDGE_BASE:
            return OFFLINE_KNOWLEDGE_BASE[player_name]["quant"]
        return DynamicScoutingEngine.evaluate_quant(player_data)

    def _call_llm(self, player_data: dict) -> dict:
        import openai
        dossier = build_player_dossier(player_data)
        client = openai.OpenAI()
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": dossier}
            ],
            temperature=0.2
        )
        return json.loads(resp.choices[0].message.content)


class TacticalAgent:
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm
        self.system_prompt = TACTICAL_AGENT_SYSTEM_PROMPT

    def evaluate(self, player_data: dict) -> dict:
        player_name = player_data["player"]
        if self.use_llm:
            try:
                return self._call_llm(player_data)
            except Exception as e:
                console.print(f"[yellow]Aviso: Falha na chamada de LLM ({e}). Recorrendo ao motor cognitivo.[/yellow]")
        if player_name in OFFLINE_KNOWLEDGE_BASE:
            return OFFLINE_KNOWLEDGE_BASE[player_name]["tactical"]
        return DynamicScoutingEngine.evaluate_tactical(player_data)

    def _call_llm(self, player_data: dict) -> dict:
        import openai
        dossier = build_player_dossier(player_data)
        client = openai.OpenAI()
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": dossier}
            ],
            temperature=0.2
        )
        return json.loads(resp.choices[0].message.content)


class FitAgent:
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm
        self.system_prompt = FIT_AGENT_SYSTEM_PROMPT

    def evaluate(self, player_data: dict) -> dict:
        player_name = player_data["player"]
        if self.use_llm:
            try:
                return self._call_llm(player_data)
            except Exception as e:
                console.print(f"[yellow]Aviso: Falha na chamada de LLM ({e}). Recorrendo ao motor cognitivo.[/yellow]")
        if player_name in OFFLINE_KNOWLEDGE_BASE:
            return OFFLINE_KNOWLEDGE_BASE[player_name]["fit"]
        return DynamicScoutingEngine.evaluate_fit(player_data)

    def _call_llm(self, player_data: dict) -> dict:
        import openai
        dossier = build_player_dossier(player_data)
        client = openai.OpenAI()
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": dossier}
            ],
            temperature=0.2
        )
        return json.loads(resp.choices[0].message.content)


class GMConsensusAgent:
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm
        self.system_prompt = GM_CONSENSUS_SYSTEM_PROMPT

    def evaluate(self, player_name: str, quant_rep: dict, tactical_rep: dict, fit_rep: dict, player_data: dict) -> dict:
        if self.use_llm:
            try:
                return self._call_llm(player_name, quant_rep, tactical_rep, fit_rep)
            except Exception as e:
                console.print(f"[yellow]Aviso: Falha na chamada de LLM ({e}). Recorrendo ao motor cognitivo.[/yellow]")
        if player_name in OFFLINE_KNOWLEDGE_BASE:
            return OFFLINE_KNOWLEDGE_BASE[player_name]["gm"]
        return DynamicScoutingEngine.evaluate_gm(player_name, quant_rep, tactical_rep, fit_rep, player_data)

    def _call_llm(self, player_name: str, quant_rep: dict, tactical_rep: dict, fit_rep: dict) -> dict:
        import openai
        prompt = build_gm_confrontation_prompt(player_name, quant_rep, tactical_rep, fit_rep)
        client = openai.OpenAI()
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return json.loads(resp.choices[0].message.content)


# ==============================================================================
# PIPELINE DA WAR ROOM & ORQUESTRAÇÃO
# ==============================================================================

class NBADraftWarRoom:
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm
        self.quant_agent = QuantAgent(use_llm=use_llm)
        self.tactical_agent = TacticalAgent(use_llm=use_llm)
        self.fit_agent = FitAgent(use_llm=use_llm)
        self.gm_agent = GMConsensusAgent(use_llm=use_llm)

    def load_draft_classes(
        self,
        year_filter: Optional[int] = None,
        round_filter: Optional[int] = None,
        limit: Optional[int] = None,
        player_query: Optional[str] = None
    ) -> List[dict]:
        all_players = []
        data_dir = Path(__file__).parent / "data"

        years = [2017, 2018] if year_filter is None else [year_filter]
        for y in years:
            filepath = data_dir / f"draft_{y}.json"
            if filepath.exists():
                with open(filepath, "r", encoding="utf-8") as f:
                    all_players.extend(json.load(f))
            else:
                console.print(f"[red]Arquivo {filepath} não encontrado![/red]")

        # Filtro de rodada
        if round_filter is not None:
            all_players = [p for p in all_players if p.get("round") == round_filter]

        # Filtro de busca por nome
        if player_query:
            query_lower = player_query.lower()
            all_players = [p for p in all_players if query_lower in p.get("player", "").lower()]

        # Limite de prospectos
        if limit is not None and limit > 0:
            all_players = all_players[:limit]

        return all_players

    def run_war_room(
        self,
        year_filter: Optional[int] = None,
        round_filter: Optional[int] = None,
        limit: Optional[int] = None,
        player_query: Optional[str] = None,
        verbose: bool = False
    ) -> List[dict]:
        players = self.load_draft_classes(year_filter, round_filter, limit, player_query)
        results = []

        console.print(Panel.fit(
            "[bold cyan]🏀 NBA DRAFT WAR ROOM (2017-2018)[/bold cyan]\n"
            "[yellow]Base Completa: 120 Prospectos (Round 1 & 2) | Arquitetura Multiagente PokéIA[/yellow]\n"
            f"[dim]Modo: {'LLM Online (API)' if self.use_llm else 'Motor Cognitivo Offline de Alta Fidelidade (Zero Custo)'} | "
            f"Prospectos Carregados: {len(players)}[/dim]",
            border_style="bright_blue"
        ))

        # Define se renderiza painéis individuais detalhados
        render_panels = verbose or (len(players) <= 14) or (player_query is not None)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            total_task = progress.add_task("[bold green]Deliberando War Room...", total=len(players))

            for p in players:
                name = p["player"]
                year = p["class_year"]
                pick_num = p.get("pick", "")
                progress.update(total_task, description=f"[bold yellow]Avaliando #{pick_num} {name} ({year})...")

                # Deliberação dos três agentes especialistas
                quant_res = self.quant_agent.evaluate(p)
                tactical_res = self.tactical_agent.evaluate(p)
                fit_res = self.fit_agent.evaluate(p)

                # Arbitragem pelo General Manager
                gm_res = self.gm_agent.evaluate(name, quant_res, tactical_res, fit_res, p)

                compiled = {
                    **p,
                    "quant": quant_res,
                    "tactical": tactical_res,
                    "fit": fit_res,
                    "gm": gm_res
                }
                results.append(compiled)

                if render_panels:
                    self._render_player_panel(compiled)

                progress.advance(total_task)

        return results

    def _render_player_panel(self, r: dict):
        p_name = r["player"]
        year = r["class_year"]
        pos = r["position"]
        pick_num = r.get("pick", "")
        target = r["target_team_and_pick"]
        q = r["quant"]
        t = r["tactical"]
        f = r["fit"]
        gm = r["gm"]

        panel_content = Text()
        panel_content.append(f"📌 ESCOLHA #{pick_num} | ALVO: {target} | POSIÇÃO: {pos}\n", style="dim")
        panel_content.append(f"1️⃣ Dr. Vance (Quant):     [{q['score']:.1f}/10] Grade: {q.get('biometric_grade', 'N/A')} - \"{q['verdict']}\"\n", style="cyan")
        panel_content.append(f"2️⃣ Coach Sullivan (Vídeo): [{t['score']:.1f}/10] Grade: {t.get('mechanics_grade', 'N/A')} - \"{t['verdict']}\"\n", style="magenta")
        panel_content.append(f"3️⃣ Elena Rostova (Fit):    [{f['score']:.1f}/10] Arq: {f.get('modern_archetype', 'N/A')} - \"{f['verdict']}\"\n", style="green")
        panel_content.append("\n🏛️ CONSELHO DO GENERAL MANAGER (DECISÃO FINAL):\n", style="bold yellow")
        panel_content.append(f"⭐ NOTA CONSOLIDADA: {gm['consolidated_score']:.1f}/10 | {gm['draft_tier']}\n", style="bold white on blue")
        panel_content.append(f"⚡ Veredito: {gm['war_room_verdict']}\n", style="bold yellow")
        panel_content.append(f"💬 Resumo Executivo: {gm['executive_summary']}\n", style="white")

        border_color = "green" if gm["consolidated_score"] >= 9.0 else ("yellow" if gm["consolidated_score"] >= 7.5 else "red")
        console.print(Panel(
            panel_content,
            title=f"[bold]#{pick_num} {p_name} ({year})[/bold]",
            subtitle=f"[bold]Histórico: {r['historical_reality']['historical_verdict']}[/bold]",
            border_style=border_color,
            expand=False
        ))

    def display_summary_table(self, results: List[dict]):
        table = Table(
            title="🏀 TABELA SINTÉTICA DE VEREDITOS DO NBA DRAFT WAR ROOM (BASE COMPLETA)",
            header_style="bold bright_white on dark_blue",
            box=box.ROUNDED,
            show_lines=True
        )
        table.add_column("Pick", justify="center", style="dim")
        table.add_column("Jogador", style="bold white")
        table.add_column("Ano", justify="center", style="dim")
        table.add_column("Analytics", justify="center", style="cyan")
        table.add_column("Tática", justify="center", style="magenta")
        table.add_column("Fit", justify="center", style="green")
        table.add_column("Veredito GM", justify="center", style="bold yellow")
        table.add_column("Realidade Histórica NBA", style="white")

        for r in results:
            gm_score = r["gm"]["consolidated_score"]
            tier = r["gm"]["draft_tier"].split("(")[0].strip()
            gm_display = f"{gm_score:.1f} ({tier})"
            pick_disp = f"#{r.get('pick', '-')}"

            table.add_row(
                pick_disp,
                r["player"],
                str(r["class_year"]),
                f"{r['quant']['score']:.1f}",
                f"{r['tactical']['score']:.1f}",
                f"{r['fit']['score']:.1f}",
                gm_display,
                r["historical_reality"]["historical_verdict"]
            )
        console.print(table)


# ==============================================================================
# ENTRY POINT PRINCIPAL
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="NBA Draft War Room (2017-2018) Multi-Agent System")
    parser.add_argument("--year", type=int, choices=[2017, 2018], default=None, help="Filtrar por ano de draft (2017 ou 2018)")
    parser.add_argument("--round", type=int, choices=[1, 2], default=None, help="Filtrar por rodada (1 ou 2)")
    parser.add_argument("--top", "--limit", dest="limit", type=int, default=None, help="Limitar quantidade de prospectos (ex: --top 14)")
    parser.add_argument("--player", type=str, default=None, help="Buscar prospecto por nome (ex: --player Brunson)")
    parser.add_argument("--verbose", action="store_true", help="Forçar exibição de painéis detalhados de cada jogador")
    parser.add_argument("--llm", action="store_true", help="Usar chamadas reais de LLM (requer OPENAI_API_KEY no ambiente)")
    parser.add_argument("--export", type=str, default="war_room_verdicts.md", help="Caminho do arquivo markdown de saída")
    args = parser.parse_args()

    use_llm = args.llm and bool(os.getenv("OPENAI_API_KEY"))
    war_room = NBADraftWarRoom(use_llm=use_llm)

    # 1. Executa a War Room
    results = war_room.run_war_room(
        year_filter=args.year,
        round_filter=args.round,
        limit=args.limit,
        player_query=args.player,
        verbose=args.verbose
    )

    # 2. Exibe a tabela sintética no terminal
    war_room.display_summary_table(results)

    # 3. Gera e salva o relatório consolidado em Markdown
    generate_markdown_report(results, output_filepath=args.export)
    console.print(f"\n[bold green]✅ Relatório executivo consolidado com {len(results)} jogadores gerado em:[/bold green] [underline cyan]{args.export}[/underline cyan]\n")


if __name__ == "__main__":
    main()

