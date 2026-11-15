# Checklist: validar um achado do scanner antes de chamar de bug

Pra cada achado crítico/alto:

## 1. Ver a prova crua
- [ ] Rodei **só aquele template** com `-debug` (`nuclei -u <alvo> -id <template> -debug`).
- [ ] Li a **requisição** e a **resposta** inteiras, não só a linha do resumo.

## 2. Entender o que o template considera "vulnerável"
- [ ] Abri o `.yaml` e li o bloco `matchers`.
- [ ] Sei se o match é por **palavra no corpo**, **status**, **cabeçalho**, **regex** ou
      **callback** (OAST/interactsh).

## 3. Desconfiar do sinal
- [ ] A resposta só **devolveu o que eu mandei** (eco/reflexão)? Se sim, palavra no corpo não
      prova nada.
- [ ] O servidor parece mesmo o **produto** que o template procura (cabeçalhos, versão,
      páginas, favicon)?
- [ ] Se casou por **callback**, o callback faz sentido pra aquele produto (origem, cliente,
      momento)?
- [ ] O mesmo host acendeu um monte de produtos que não convivem juntos? Sinal de isca/WAF/eco.

## 4. Refazer na mão (só em alvo autorizado)
- [ ] Reproduzi com `curl`/navegador, fora do scanner.
- [ ] Busquei uma prova que **só** um sistema vulnerável daria (a saída do comando, não o
      comando refletido; um dado que só existe lá dentro; versão confirmada).
- [ ] Anotei a evidência (request, response, horário, versão) pro laudo.

## Resultado
- [ ] **Validado** → vai pro laudo com evidência e impacto.
- [ ] **Não validado** → registra como "indício não confirmado" ou descarta. Não vai como bug.

---
Lab pra treinar isso sem tocar em ninguém: [`../lab`](../lab). Feito pela
[CHDEVSEC](https://chdevsec.com.br).
