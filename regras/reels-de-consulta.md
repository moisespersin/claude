# Regras — Reels a partir de gravação de consulta

Padrão fixo para transformar a gravação de uma consulta com paciente em até 4 Reels
separados por tópico. Vale para todas as consultas enviadas. A base de estilo vem da
sessão "[Vídeo] Narrado".

## Objetivo

- Vídeos de **identificação total** para outros pacientes: o foco é a **dor do paciente**,
  a queixa, o que incomoda, como afeta o dia a dia.
- Destacar a **fala de queixa pura do paciente**, mas também mostrar a fala do dentista.
- Cada vídeo abre com o **melhor gancho** para reter o público.

## 1. Privacidade (prioridade máxima)

- **Rosto do paciente nunca aparece.** Se entrar no quadro, recortar ou desfocar.
- Nada de closes ou detalhes que identifiquem (tatuagem, joia marcante, crachá, etc.).
- **Cortar do áudio e do vídeo:** nome do paciente, idade, cidade, valores e qualquer
  outro dado confidencial. Esses trechos também **não aparecem na legenda**.
- Antes de entregar, revisar cada corte procurando dado que tenha escapado.

## 2. Enquadramento

- Vertical **9:16 (1080×1920)**.
- O dentista fica **no centro**.
- Mostrar **um detalhe neutro do paciente** (mãos, ombro, nuca, de costas), só para
  mostrar que há alguém ali, sem permitir identificação.
- Se não houver nenhum trecho do paciente que possa aparecer, avisar. Não inventar imagem.

## 3. Seleção dos momentos

1. Transcrever a consulta inteira (Whisper, português), identificando quem fala.
2. Mapear as falas de queixa: o que incomoda, desde quando, impacto no dia a dia
   (foto, trabalho, relacionamentos, autoestima), o que já tentou, medos.
3. Montar **até 4 tópicos**. Estrutura de cada vídeo:
   gancho (frase mais forte do paciente) → contexto da queixa → fala do dentista →
   fechamento de impacto.
4. **Propor os tópicos antes de cortar.** Para cada um: título, frase-gancho, trechos
   com tempos (início–fim) e duração estimada. Só cortar após aprovação.

## 4. Cortes

- **Cortes brutos (secos)**: sem transições, zooms ou efeitos.
- Final do vídeo **termina seco** na última fala, sem CTA (salvo pedido).
- Sem texto fixo de gancho no topo (salvo pedido): o gancho é a própria fala.

## 5. Áudio

- Limpar ao máximo: **remover ruídos externos** (ar-condicionado, eco, fundo),
  deixando só a voz.
- Igualar o volume entre dentista e paciente (o paciente costuma estar mais longe do microfone).
- Ponto de partida (ffmpeg), ajustar de ouvido por gravação:
  `highpass=f=80,lowpass=f=12000,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3,loudnorm=I=-14:TP=-1.5:LRA=7`
- Fade-out curto no final (~0,3 s).

## 6. Legendas dinâmicas

**Base do estilo (não muda):**

- Fonte **Manrope Light** (peso 300), sem negrito.
- Texto **cinza `#C7CDD3`**, palavra sendo falada em **branco `#FFFFFF`** (karaokê).
- Caixa **grafite `#1F2228` translúcida** (~65% de opacidade).
- Blocos curtos (2 a 5 palavras), quebrados no ritmo da fala.
- Corrigir erros da transcrição automática (nomes próprios, termos técnicos).

**Dinamismo adicionado para esta série:**

- **(A) Palavras-chave em destaque:** palavras de dor/emoção (ex.: "vergonha",
  "incomoda", "escondo", "não sorrio") aparecem **maiores** e com um **leve "pulo"**
  (escala) no momento em que são faladas.
- **(E) Posição por quem fala:** a legenda do **paciente** fica numa altura e a do
  **dentista** em outra, para que se perceba quem fala e para dar ritmo.
- Sempre acima dos botões do Instagram (zona segura).

## 7. Exportação e entrega

- 1080×1920, **60 fps**, H.264 (`-preset slow -crf 18 -profile:v high`), áudio AAC 192k,
  `-movflags +faststart`, sem metadados (`-map_metadata -1`).
- Vídeo do iPhone pode vir em HDR (HLG/BT.2020): exportar em HDR é ~4× mais lento.
- Para **cada tópico**, entregar **duas versões**: **com legenda** e **sem legenda**.
- Conferir um quadro de cada bloco de legenda antes de enviar.

## Recebimento do vídeo

- Por **WeTransfer** (já liberado no ambiente) ou **Dropbox** (pode exigir liberar o
  host de download na primeira vez).
- Vídeos grandes: espaço em disco na nuvem é limitado; apagar arquivos intermediários
  ao longo do processo.
