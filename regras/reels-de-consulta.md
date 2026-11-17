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
- Câmera fixa com paciente à esquerda: usar **zoom** (não desfoque).
  - Falas do dentista: recorte 810×1440 (x=270, y=300) → mostra braço/mãos/pernas do paciente.
  - Falas do paciente, quando ela se inclina e o perfil aparece: recorte mais fechado
    700×1244 (x=380, y=330). Conferir quadro a quadro antes de exportar.

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
- Redução de ruído com o modelo RNN de voz `sh.rnnn` (arnndn) + afftdn.
- O loudnorm de passada única fica abaixo do alvo: fazer **segunda passada** (medição + ganho
  com limitador) até ~−14 LUFS.

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

- 1080×1920, **mesma taxa de quadros do original** (gravação de consulta veio em 30 fps; não inventar 60), H.264 (`-preset slow -crf 18 -profile:v high`), áudio AAC 192k,
  `-movflags +faststart`, sem metadados (`-map_metadata -1`).
- Vídeo do iPhone pode vir em HDR (HLG/BT.2020): exportar em HDR é ~4× mais lento.
- Para **cada tópico**, entregar **duas versões**: **com legenda** e **sem legenda**.
- Conferir um quadro de cada bloco de legenda antes de enviar.

## Recebimento do vídeo

- Por **WeTransfer** (já liberado no ambiente) ou **Dropbox**. O Dropbox usa um endereço de
  download diferente a cada link (`<código>.dl.dropboxusercontent.com`), então cada vídeo novo
  pede uma aprovação de rede.
- Transcrição: Whisper `large-v3-turbo` (melhor que o `medium`). Não usar frase-guia longa
  no `initial_prompt` sem `condition_on_previous_text=False` — o modelo repete a frase.
- Vídeos grandes: espaço em disco na nuvem é limitado; apagar arquivos intermediários
  ao longo do processo.
